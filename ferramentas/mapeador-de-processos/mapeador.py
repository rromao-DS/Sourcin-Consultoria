#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mapeador de processos
=====================

Lê a descrição de um processo de negócio em um arquivo TOML e gera:

  1. um diagrama **BPMN 2.0** (`.bpmn`), que abre no bpmn.io, Camunda Modeler,
     Bizagi ou qualquer ferramenta compatível;
  2. um **relatório de análise** (`.md`) com tempos, gargalos e oportunidades
     de automação;
  3. um **painel de indicadores** (`.html`) para abrir no navegador.

A ideia é tirar o processo do papel: a mesma descrição que serve de ata de
reunião vira diagrama e indicadores, sem desenhar nada à mão.

Uso
---
    python mapeador.py processos/chamado-suporte-ti.toml
    python mapeador.py processos/*.toml --saida saida

Requer Python 3.11 ou superior (usa `tomllib` da biblioteca padrão).
"""

from __future__ import annotations

import argparse
import glob
import html
import sys
import tomllib
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

# ---------------------------------------------------------------------------
# BPMN 2.0 — namespaces e dimensões do desenho
# ---------------------------------------------------------------------------

NS = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
    "dc": "http://www.omg.org/spec/DD/20100524/DC",
    "di": "http://www.omg.org/spec/DD/20100524/DI",
}

# Tamanho dos elementos no diagrama (px)
TAMANHOS = {
    "inicio": (36, 36),
    "fim": (36, 36),
    "tarefa": (140, 80),
    "decisao": (50, 50),
}

# Geometria do desenho
X_PISCINA = 160
Y_PISCINA = 80
LARGURA_FAIXA_ROTULO = 30
PRIMEIRO_ELEMENTO_X = 250
PASSO_X = 190
ALTURA_RAIA = 150
MARGEM_DIREITA = 120

TIPOS_VALIDOS = {"inicio", "fim", "tarefa", "decisao"}


# ---------------------------------------------------------------------------
# Leitura e validação
# ---------------------------------------------------------------------------


def carregar_processo(caminho: Path) -> dict:
    with open(caminho, "rb") as f:
        return tomllib.load(f)


def validar(processo: dict, origem: str = "") -> list[str]:
    """Devolve a lista de problemas encontrados na descrição do processo."""
    erros: list[str] = []
    onde = f" ({origem})" if origem else ""

    if "processo" not in processo:
        erros.append(f"[processo] seção obrigatória ausente{onde}")
        return erros
    if not processo["processo"].get("nome"):
        erros.append(f"[processo] o campo 'nome' é obrigatório{onde}")

    etapas = processo.get("etapas") or []
    if not etapas:
        erros.append(f"o processo não tem nenhuma etapa definida{onde}")
        return erros

    raias = processo.get("raias") or []
    ids = [e.get("id") for e in etapas]
    if len(ids) != len(set(ids)):
        repetidos = sorted({i for i in ids if ids.count(i) > 1})
        erros.append(f"ids repetidos nas etapas: {', '.join(str(r) for r in repetidos)}")

    for etapa in etapas:
        ident = etapa.get("id") or "(sem id)"
        tipo = etapa.get("tipo")
        if not etapa.get("id"):
            erros.append("há uma etapa sem 'id'")
        if tipo not in TIPOS_VALIDOS:
            erros.append(
                f"etapa '{ident}': tipo inválido '{tipo}' "
                f"(use: {', '.join(sorted(TIPOS_VALIDOS))})"
            )
        if not etapa.get("nome"):
            erros.append(f"etapa '{ident}': o campo 'nome' é obrigatório")
        raia = etapa.get("raia")
        if raias and raia not in raias:
            erros.append(f"etapa '{ident}': raia '{raia}' não está declarada em [raias]")
        for campo in ("tempo_min", "espera_min"):
            valor = etapa.get(campo, 0)
            if not isinstance(valor, (int, float)) or valor < 0:
                erros.append(f"etapa '{ident}': '{campo}' deve ser um número ≥ 0")
        for destino in etapa.get("proximo", []):
            if destino not in ids:
                erros.append(f"etapa '{ident}': 'proximo' aponta para '{destino}', que não existe")

    # Deixa o próximo implícito quando não informado (ordem de declaração)
    for i, etapa in enumerate(etapas):
        if "proximo" not in etapa and etapa.get("tipo") != "fim" and i + 1 < len(etapas):
            etapa["proximo"] = [etapas[i + 1]["id"]]

    return erros


# ---------------------------------------------------------------------------
# Geração do BPMN 2.0
# ---------------------------------------------------------------------------


def _elemento_bpmn(etapa: dict) -> str:
    """Tag BPMN correspondente ao tipo da etapa.

    O detalhe que importa para a análise: uma etapa marcada como automatizável
    vira `serviceTask` (executada por sistema), em vez de `userTask`.
    """
    tipo = etapa["tipo"]
    if tipo == "tarefa":
        return "serviceTask" if etapa.get("automatizavel") else "userTask"
    return {"inicio": "startEvent", "fim": "endEvent", "decisao": "exclusiveGateway"}[tipo]


def gerar_bpmn(processo: dict) -> str:
    nome_processo = processo["processo"]["nome"]
    etapas = processo["etapas"]
    raias = processo.get("raias") or []
    if not raias:
        # Sem [raias] declarado: usa a ordem em que as áreas aparecem
        for e in etapas:
            r = e.get("raia", "Processo")
            if r not in raias:
                raias.append(r)
    indice_raia = {r: i for i, r in enumerate(raias)}

    # ---- fluxos (sequence flows)
    fluxos = []
    for etapa in etapas:
        for ordem, destino in enumerate(etapa.get("proximo", [])):
            rotulo = (etapa.get("rotulos") or {}).get(destino)
            fluxos.append({
                "id": f"fluxo_{etapa['id']}_{destino}_{ordem}",
                "origem": etapa["id"],
                "destino": destino,
                "nome": rotulo,
            })

    entradas: dict[str, list[str]] = {e["id"]: [] for e in etapas}
    saidas: dict[str, list[str]] = {e["id"]: [] for e in etapas}
    for f in fluxos:
        saidas[f["origem"]].append(f["id"])
        entradas[f["destino"]].append(f["id"])

    # ---- posições
    posicoes = {}
    for i, etapa in enumerate(etapas):
        largura, altura = TAMANHOS[etapa["tipo"]]
        y_raia = Y_PISCINA + indice_raia.get(etapa.get("raia"), 0) * ALTURA_RAIA
        x = PRIMEIRO_ELEMENTO_X + i * PASSO_X + (PASSO_X - largura) / 2
        y = y_raia + (ALTURA_RAIA - altura) / 2
        posicoes[etapa["id"]] = (x, y, largura, altura)

    largura_total = (
        PRIMEIRO_ELEMENTO_X - X_PISCINA + len(etapas) * PASSO_X + MARGEM_DIREITA
    )
    altura_total = len(raias) * ALTURA_RAIA

    partes: list[str] = []
    partes.append('<?xml version="1.0" encoding="UTF-8"?>')
    partes.append(
        '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"'
        ' xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"'
        ' xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"'
        ' xmlns:di="http://www.omg.org/spec/DD/20100524/DI"'
        ' id="Definitions_1" targetNamespace="http://bpmn.io/schema/bpmn">'
    )

    # ---- colaboração (piscina) + processo
    partes.append(
        f'  <bpmn:collaboration id="Colaboracao_1">'
        f'<bpmn:participant id="Piscina_1" name="{escape(nome_processo)}"'
        f' processRef="Processo_1" /></bpmn:collaboration>'
    )
    partes.append('  <bpmn:process id="Processo_1" isExecutable="false">')

    # raias
    partes.append('    <bpmn:laneSet id="RaiaSet_1">')
    for i, raia in enumerate(raias):
        refs = "".join(
            f"<bpmn:flowNodeRef>{e['id']}</bpmn:flowNodeRef>"
            for e in etapas if e.get("raia") == raia
        )
        partes.append(
            f'      <bpmn:lane id="Raia_{i + 1}" name="{escape(raia)}">{refs}</bpmn:lane>'
        )
    partes.append("    </bpmn:laneSet>")

    # nós
    for etapa in etapas:
        tag = _elemento_bpmn(etapa)
        ident = etapa["id"]
        nome = escape(etapa["nome"])
        filhos = ""
        if tag != "startEvent":
            filhos += "".join(f"<bpmn:incoming>{f}</bpmn:incoming>" for f in entradas[ident])
        if tag != "endEvent":
            filhos += "".join(f"<bpmn:outgoing>{f}</bpmn:outgoing>" for f in saidas[ident])
        partes.append(f'    <bpmn:{tag} id="{ident}" name="{nome}">{filhos}</bpmn:{tag}>')

    # fluxos
    for f in fluxos:
        nome = f' name="{escape(f["nome"])}"' if f["nome"] else ""
        partes.append(
            f'    <bpmn:sequenceFlow id="{f["id"]}"{nome}'
            f' sourceRef="{f["origem"]}" targetRef="{f["destino"]}" />'
        )
    partes.append("  </bpmn:process>")

    # ---- parte gráfica (DI)
    partes.append('  <bpmndi:BPMNDiagram id="Diagrama_1">')
    partes.append(
        '    <bpmndi:BPMNPlane id="Plano_1" bpmnElement="Colaboracao_1">'
    )
    partes.append(
        f'      <bpmndi:BPMNShape id="Piscina_1_di" bpmnElement="Piscina_1" isHorizontal="true">'
        f'<dc:Bounds x="{X_PISCINA}" y="{Y_PISCINA}"'
        f' width="{largura_total}" height="{altura_total}" /></bpmndi:BPMNShape>'
    )
    for i, raia in enumerate(raias):
        partes.append(
            f'      <bpmndi:BPMNShape id="Raia_{i + 1}_di" bpmnElement="Raia_{i + 1}"'
            f' isHorizontal="true"><dc:Bounds x="{X_PISCINA + LARGURA_FAIXA_ROTULO}"'
            f' y="{Y_PISCINA + i * ALTURA_RAIA}"'
            f' width="{largura_total - LARGURA_FAIXA_ROTULO}"'
            f' height="{ALTURA_RAIA}" /></bpmndi:BPMNShape>'
        )
    for etapa in etapas:
        x, y, largura, altura = posicoes[etapa["id"]]
        partes.append(
            f'      <bpmndi:BPMNShape id="{etapa["id"]}_di" bpmnElement="{etapa["id"]}">'
            f'<dc:Bounds x="{x:.0f}" y="{y:.0f}" width="{largura}" height="{altura}" />'
            f'</bpmndi:BPMNShape>'
        )
    for f in fluxos:
        xo, yo, lo, ao = posicoes[f["origem"]]
        xd, yd, ld, ad = posicoes[f["destino"]]
        partida = (xo + lo, yo + ao / 2)
        chegada = (xd, yd + ad / 2)
        if abs(partida[1] - chegada[1]) < 1:
            pontos = [partida, chegada]
        else:
            meio = partida[0] + 25
            pontos = [partida, (meio, partida[1]), (meio, chegada[1]), chegada]
        waypoints = "".join(
            f'<di:waypoint x="{px:.0f}" y="{py:.0f}" />' for px, py in pontos
        )
        partes.append(
            f'      <bpmndi:BPMNEdge id="{f["id"]}_di" bpmnElement="{f["id"]}">'
            f'{waypoints}</bpmndi:BPMNEdge>'
        )
    partes.append("    </bpmndi:BPMNPlane>")
    partes.append("  </bpmndi:BPMNDiagram>")
    partes.append("</bpmn:definitions>")

    return "\n".join(partes)


# ---------------------------------------------------------------------------
# Análise do processo
# ---------------------------------------------------------------------------


def analisar(processo: dict) -> dict:
    etapas = processo["etapas"]
    tarefas = [e for e in etapas if e["tipo"] == "tarefa"]

    tempo_execucao = sum(e.get("tempo_min", 0) for e in etapas)
    tempo_espera = sum(e.get("espera_min", 0) for e in etapas)
    lead_time = tempo_execucao + tempo_espera

    # Trocas de área: cada passagem de uma raia para outra é um handoff
    por_id = {e["id"]: e for e in etapas}
    handoffs = 0
    for e in etapas:
        for destino in e.get("proximo", []):
            alvo = por_id.get(destino)
            if alvo and alvo.get("raia") != e.get("raia"):
                handoffs += 1

    automatizaveis = [e for e in tarefas if e.get("automatizavel")]
    # Ganho conservador: 70% do tempo da etapa automatizada (execução + espera)
    ganho = sum(
        (e.get("tempo_min", 0) + e.get("espera_min", 0)) * 0.7 for e in automatizaveis
    )

    esperas = [e.get("espera_min", 0) for e in tarefas]
    media_espera = sum(esperas) / len(esperas) if esperas else 0
    gargalos = sorted(
        (e for e in tarefas if e.get("espera_min", 0) > max(media_espera, 0)),
        key=lambda e: e.get("espera_min", 0),
        reverse=True,
    )

    return {
        "etapas": len(etapas),
        "tarefas": len(tarefas),
        "tempo_execucao": tempo_execucao,
        "tempo_espera": tempo_espera,
        "lead_time": lead_time,
        "handoffs": handoffs,
        "automatizaveis": len(automatizaveis),
        "percentual_automatizavel": (100 * len(automatizaveis) / len(tarefas))
        if tarefas else 0,
        "ganho_estimado": ganho,
        "media_espera": media_espera,
        "gargalos": gargalos,
    }


def _horas(minutos: float) -> str:
    if minutos >= 1440:
        return f"{minutos / 1440:.1f} dias"
    if minutos >= 60:
        return f"{minutos / 60:.1f} h"
    return f"{minutos:.0f} min"


# ---------------------------------------------------------------------------
# Relatório em Markdown
# ---------------------------------------------------------------------------


def relatorio_markdown(processo: dict, a: dict) -> str:
    nome = processo["processo"]["nome"]
    descricao = processo["processo"].get("descricao", "")
    etapas = processo["etapas"]

    linhas = [
        f"# Análise do processo: {nome}",
        "",
    ]
    if descricao:
        linhas += [descricao, ""]
    linhas += [
        "> Relatório gerado automaticamente pelo `mapeador.py` a partir da descrição do",
        "> processo em TOML. O diagrama correspondente está no arquivo `.bpmn`.",
        "",
        "## Indicadores",
        "",
        "| Indicador | Valor |",
        "| --- | --- |",
        f"| Etapas mapeadas | {a['etapas']} |",
        f"| Tempo de execução (mão de obra) | {_horas(a['tempo_execucao'])} |",
        f"| Tempo de espera | {_horas(a['tempo_espera'])} |",
        f"| **Lead time total** | **{_horas(a['lead_time'])}** |",
        f"| Trocas de área (handoffs) | {a['handoffs']} |",
        f"| Etapas automatizáveis | {a['automatizaveis']} de {a['tarefas']}"
        f" ({a['percentual_automatizavel']:.0f}%) |",
        f"| Ganho estimado com automação | {_horas(a['ganho_estimado'])} por ciclo |",
        "",
        "## Etapas",
        "",
        "| # | Etapa | Área | Tipo | Execução | Espera | Sistema |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for i, e in enumerate(etapas, 1):
        tipo = {"tarefa": "Tarefa", "decisao": "Decisão", "inicio": "Início", "fim": "Fim"}
        marca = " (automatizável)" if e.get("automatizavel") else ""
        linhas.append(
            f"| {i} | {e['nome']} | {e.get('raia', '-')} | {tipo[e['tipo']]}{marca} | "
            f"{_horas(e.get('tempo_min', 0))} | {_horas(e.get('espera_min', 0))} | "
            f"{e.get('sistema', '-')} |"
        )

    linhas += ["", "## Oportunidades de automação", ""]
    automatizaveis = [e for e in etapas if e.get("automatizavel")]
    if automatizaveis:
        for e in automatizaveis:
            linhas.append(
                f"- **{e['nome']}** ({e.get('raia', '-')}) — "
                f"{_horas(e.get('tempo_min', 0) + e.get('espera_min', 0))} por ciclo"
            )
    else:
        linhas.append("Nenhuma etapa foi marcada como automatizável na descrição.")

    linhas += ["", "## Gargalos (maior tempo de espera)", ""]
    if a["gargalos"]:
        for e in a["gargalos"]:
            linhas.append(f"- **{e['nome']}** — espera de {_horas(e.get('espera_min', 0))}")
    else:
        linhas.append("Nenhuma etapa tem tempo de espera acima da média das tarefas.")

    linhas += [
        "",
        "## Como ler estes números",
        "",
        "- **Tempo de execução** é o trabalho efetivo; **espera** é o tempo parado em fila",
        "  ou aguardando terceiros. O lead time é a soma dos dois — e é o que o usuário",
        "  sente.",
        "- **Handoff** é cada passagem do processo de uma área para outra. Quanto mais",
        "  trocas, maior a chance de retrabalho e de perda de informação.",
        "- **Ganho estimado** é conservador: considera 70% do tempo da etapa automatizada.",
        "",
    ]
    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# Painel em HTML
# ---------------------------------------------------------------------------


def painel_html(processo: dict, a: dict) -> str:
    nome = processo["processo"]["nome"]
    etapas = processo["etapas"]
    maior = max((e.get("tempo_min", 0) + e.get("espera_min", 0)) for e in etapas) or 1

    cartoes = [
        ("Lead time", _horas(a["lead_time"])),
        ("Tempo de espera", _horas(a["tempo_espera"])),
        ("Trocas de área", str(a["handoffs"])),
        ("Automatizáveis", f"{a['automatizaveis']} de {a['tarefas']}"),
        ("Ganho estimado", _horas(a["ganho_estimado"])),
    ]

    barras = []
    for e in etapas:
        total = e.get("tempo_min", 0) + e.get("espera_min", 0)
        largura = max(1.0, 100 * total / maior)
        barras.append(
            f'<div class="linha"><span class="rotulo">{html.escape(e["nome"])}'
            f'<em>{html.escape(str(e.get("raia", "")))}</em></span>'
            f'<span class="barra" style="width:{largura:.1f}%"></span>'
            f'<span class="valor">{_horas(total)}</span></div>'
        )

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Análise do processo — {html.escape(nome)}</title>
<style>
  :root {{ color-scheme: light; }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 48px 24px; background: #f6f6f3; color: #16211f;
    font: 16px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif;
  }}
  main {{ max-width: 900px; margin: 0 auto; }}
  header {{ border-bottom: 1px solid #d9d6cd; padding-bottom: 20px; }}
  .sobre {{ font: 12px/1.4 ui-monospace, monospace; letter-spacing: .08em;
            text-transform: uppercase; color: #6b7a76; }}
  h1 {{ font-size: 28px; margin: 8px 0 0; }}
  .cartoes {{ display: grid; gap: 1px; background: #d9d6cd; border: 1px solid #d9d6cd;
              border-radius: 10px; overflow: hidden; margin: 28px 0;
              grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); }}
  .cartao {{ background: #fff; padding: 16px 18px; }}
  .cartao dt {{ font: 12px/1.4 ui-monospace, monospace; color: #6b7a76;
                text-transform: uppercase; letter-spacing: .06em; }}
  .cartao dd {{ margin: 6px 0 0; font-size: 22px; font-weight: 600; color: #0f5c55; }}
  h2 {{ font-size: 18px; margin: 36px 0 14px; }}
  .linha {{ display: grid; grid-template-columns: minmax(160px, 40%) 1fr 76px;
            align-items: center; gap: 12px; padding: 6px 0; }}
  .rotulo {{ font-size: 14px; }}
  .rotulo em {{ display: block; font-style: normal; font-size: 12px; color: #6b7a76; }}
  .barra {{ height: 12px; border-radius: 6px; background: #0f5c55; }}
  .valor {{ font: 12px/1 ui-monospace, monospace; color: #6b7a76; text-align: right; }}
  footer {{ margin-top: 40px; padding-top: 16px; border-top: 1px solid #d9d6cd;
            font-size: 13px; color: #6b7a76; }}
</style>
</head>
<body>
<main>
  <header>
    <p class="sobre">Análise de processo · gerada por mapeador.py</p>
    <h1>{html.escape(nome)}</h1>
  </header>

  <dl class="cartoes">
    {''.join(f'<div class="cartao"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in cartoes)}
  </dl>

  <h2>Tempo por etapa</h2>
  {''.join(barras)}

  <footer>
    Tempo de execução {_horas(a['tempo_execucao'])} ·
    espera {_horas(a['tempo_espera'])} ·
    lead time {_horas(a['lead_time'])}.
    O diagrama BPMN do processo está no arquivo <code>.bpmn</code>.
  </footer>
</main>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def processar(processo: dict, nome_arquivo: str, pasta_saida: Path) -> dict:
    pasta_saida.mkdir(parents=True, exist_ok=True)
    resultados = {}

    bpmn = gerar_bpmn(processo)
    # Confere se o XML gerado é válido antes de gravar
    ET.fromstring(bpmn)
    arq = pasta_saida / f"{nome_arquivo}.bpmn"
    arq.write_text(bpmn, encoding="utf-8")
    resultados["bpmn"] = arq

    analise = analisar(processo)
    arq = pasta_saida / f"{nome_arquivo}.md"
    arq.write_text(relatorio_markdown(processo, analise), encoding="utf-8")
    resultados["relatorio"] = arq

    arq = pasta_saida / f"{nome_arquivo}.html"
    arq.write_text(painel_html(processo, analise), encoding="utf-8")
    resultados["painel"] = arq

    resultados["analise"] = analise
    return resultados


def expandir_arquivos(padroes: list[Path]) -> list[Path]:
    """Aceita caminhos e também curingas (ex.: processos/*.toml).

    O Windows (PowerShell) não expande curingas sozinho, então fazemos isso aqui
    para o comando funcionar igual em qualquer sistema.
    """
    arquivos: list[Path] = []
    for padrao in padroes:
        texto = str(padrao)
        if any(c in texto for c in "*?["):
            achados = sorted(glob.glob(texto))
            if not achados:
                print(f"[aviso] nenhum arquivo corresponde a {texto}", file=sys.stderr)
            arquivos.extend(Path(a) for a in achados)
        else:
            arquivos.append(padrao)
    return arquivos


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="mapeador.py",
        description="Gera diagrama BPMN 2.0 e relatório de análise a partir de um processo em TOML.",
    )
    parser.add_argument("arquivos", nargs="+", type=Path,
                        help="arquivo(s) .toml com a descrição do processo (aceita curingas)")
    parser.add_argument("--saida", type=Path, default=Path("saida"),
                        help="pasta de destino dos arquivos gerados (padrão: saida/)")
    args = parser.parse_args(argv)

    problemas = False
    for caminho in expandir_arquivos(args.arquivos):
        if not caminho.exists():
            print(f"[erro] arquivo não encontrado: {caminho}", file=sys.stderr)
            problemas = True
            continue
        try:
            processo = carregar_processo(caminho)
        except tomllib.TOMLDecodeError as e:
            print(f"[erro] {caminho}: TOML inválido — {e}", file=sys.stderr)
            problemas = True
            continue

        erros = validar(processo, caminho.name)
        if erros:
            print(f"[erro] {caminho}:", file=sys.stderr)
            for e in erros:
                print(f"   - {e}", file=sys.stderr)
            problemas = True
            continue

        try:
            res = processar(processo, caminho.stem, args.saida)
        except ET.ParseError as e:
            print(f"[erro] {caminho}: BPMN gerado é inválido — {e}", file=sys.stderr)
            problemas = True
            continue

        a = res["analise"]
        print(f"\n{processo['processo']['nome']}")
        print(f"  lead time ............. {_horas(a['lead_time'])}")
        print(f"  trocas de área ........ {a['handoffs']}")
        print(f"  etapas automatizáveis . {a['automatizaveis']} de {a['tarefas']}")
        print(f"  ganho estimado ........ {_horas(a['ganho_estimado'])} por ciclo")
        for chave in ("bpmn", "relatorio", "painel"):
            print(f"  {chave:>21} .. {res[chave]}")

    return 1 if problemas else 0


if __name__ == "__main__":
    raise SystemExit(main())
