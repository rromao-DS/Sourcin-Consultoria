# -*- coding: utf-8 -*-
"""Gera os dados estruturados para o site: biblioteca R2 Tech e pacote de exemplo da Surcin (JSON).

Os arquivos seguem dados/pacote.schema.json e carregam direto nas tabelas de dados/schema.sql
(as chaves de cada objeto são os nomes das colunas). IDs são UUID estáveis, derivados de um nome.
Uso: python3 gerar_dados.py [pasta_de_saida]
"""
import json
import os
import sys
import uuid

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import base as m  # noqa: E402
import casos  # noqa: E402

NS = uuid.UUID("6f1c2b0e-2d1a-4f0e-9b7a-2a7e0c1d5e10")
VERSAO_SCHEMA = "1.0"


def uid(*partes):
    return str(uuid.uuid5(NS, "/".join(partes)))


def tabela(pares):
    return [{"a_partir_de": lim, "nota": nota} for lim, nota in pares]


def politica(id_, empresa_id, nome):
    return {
        "id": id_, "empresa_id": empresa_id, "nome": nome,
        "peso_comportamental": m.PESOS[0][1], "peso_tecnico": m.PESOS[1][1], "peso_indicadores": m.PESOS[2][1],
        "conversao_faltas": tabela(m.ASSIDUIDADE[0][1]),
        "conversao_atrasos": tabela(m.ASSIDUIDADE[1][1]),
        "conversao_percentual": tabela(m.FAIXAS_PCT),
        "faixas_gratificacao": [{"a_partir_de": lim, "percentual": pct, "faixa": txt.split(":")[0]}
                                for lim, pct, txt in m.FAIXAS_GRAT],
        "periodicidade": "semestral", "atestado_reduz_nota": False, "validada_em": None,
    }


def competencia(id_, empresa_id, tipo, nome, nivel_3, codigo=None, area=None, definicao=None,
                nivel_1=None, nivel_5=None, evidencia=None, origem=None):
    return {"id": id_, "empresa_id": empresa_id, "tipo": tipo, "area_biblioteca": area, "codigo": codigo,
            "nome": nome, "definicao": definicao, "nivel_1": nivel_1, "nivel_3": nivel_3, "nivel_5": nivel_5,
            "evidencia_sugerida": evidencia, "origem": origem, "ativo": True}


# ---------------------------------------------------------------------------
def biblioteca():
    comp = []
    for cod, nome, defin, n1, n3, n5 in m.comuns(casos.GENERICO):
        comp.append(competencia(uid("comp", cod), None, "comportamental", nome, n3, codigo=cod,
                                definicao=defin, nivel_1=n1, nivel_5=n5))
    for area, itens in m.BIBLIOTECA.items():
        for nome, atende, evid in itens:
            comp.append(competencia(uid("comp", area, nome), None, "tecnica", nome, atende, area=area,
                                    evidencia=evid))
    for cod, nome, desc in m.LIDERANCA:
        comp.append(competencia(uid("comp", cod), None, "lideranca", nome, desc, codigo=cod))
    return {
        "versao_schema": VERSAO_SCHEMA,
        "tipo": "biblioteca",
        "descricao": "Biblioteca padrão R2 Tech Consultoria: competências, indicadores de assiduidade e política "
                     "padrão. Registros com empresa_id nulo, visíveis a todas as empresas.",
        "competencias": comp,
        "indicadores": [
            {"id": uid("ind", "faltas"), "empresa_id": None, "tipo": "faltas_injustificadas",
             "nome": m.ASSIDUIDADE[0][0], "fonte": "Registro de assiduidade", "tabela_conversao": None},
            {"id": uid("ind", "atrasos"), "empresa_id": None, "tipo": "atrasos",
             "nome": m.ASSIDUIDADE[1][0], "fonte": "Registro de assiduidade", "tabela_conversao": None},
        ],
        "politicas_avaliacao": [politica(uid("pol", "padrao"), None, "Padrão R2 Tech")],
    }


# ---------------------------------------------------------------------------
def surcin():
    cfg, org = casos.SURCIN, casos.ORGANOGRAMA_SURCIN
    emp = uid("emp", "surcin")
    pk = lambda *p: uid("surcin", *p)  # noqa: E731

    areas = [{"id": pk("area", a), "empresa_id": emp, "nome": a, "area_pai_id": None, "ordem": i}
             for i, a in enumerate(org["areas"])]
    cargos = [{"id": pk("cargo", c), "empresa_id": emp, "area_id": pk("area", a), "nome": c, "missao": None,
               "responsabilidades": r, "ativo": True} for c, (a, r) in org["cargos"].items()]
    pessoas, vinculos = [], []
    for nome, (cargo, gestor, tipo, jornada) in org["pessoas"].items():
        pessoas.append({"id": pk("pessoa", nome), "empresa_id": emp, "usuario_id": None, "nome": nome,
                        "email": None, "ativo": True, "observacoes": None})
        vinculos.append({"id": pk("vinculo", nome), "empresa_id": emp, "pessoa_id": pk("pessoa", nome),
                         "cargo_id": pk("cargo", cargo), "gestor_pessoa_id": pk("pessoa", gestor) if gestor else None,
                         "tipo": tipo, "jornada": jornada, "data_inicio": None, "data_fim": None})

    competencias, cargo_comp, indicadores, cargo_ind = [], [], [], []
    for nome, f in cfg["pessoas"].items():
        cargo_id = pk("cargo", f["cargo"])
        area = org["cargos"][f["cargo"]][0]
        for ordem, (cod, cnome, atende, evid) in enumerate(f["tecnicas"]):
            cid = pk("comp", f["cargo"], cnome)
            competencias.append(competencia(cid, emp, "tecnica", cnome, atende, area=area, evidencia=evid,
                                            origem=f["fonte"]))
            cargo_comp.append({"cargo_id": cargo_id, "competencia_id": cid, "codigo": cod, "ordem": ordem,
                               "texto_atender": None, "evidencia": evid})
        for ordem, (inome, fonte) in enumerate(f["indicadores"]):
            iid = pk("ind", f["cargo"], inome)
            indicadores.append({"id": iid, "empresa_id": emp, "tipo": "percentual", "nome": inome, "fonte": fonte,
                                "tabela_conversao": None})
            cargo_ind.append({"cargo_id": cargo_id, "indicador_id": iid, "ordem": ordem})

    pol = pk("politica")
    ciclos = [{"id": pk("ciclo", n), "empresa_id": emp, "politica_id": pol, "nome": n, "tipo": t,
               "data_inicio": ini, "data_fim": fim, "status": "planejado", "efeito_financeiro": ef}
              for n, t, ini, fim, ef in org["ciclos"]]

    # Avaliações do ciclo piloto já abertas, sem notas: as notas só existem depois da aplicação.
    piloto = ciclos[0]["id"]
    avaliacoes, itens = [], []
    for nome, f in cfg["pessoas"].items():
        aid = pk("aval", "piloto", nome)
        avaliacoes.append({"id": aid, "empresa_id": emp, "ciclo_id": piloto, "pessoa_id": pk("pessoa", nome),
                           "cargo_id": pk("cargo", f["cargo"]), "avaliador_pessoa_id": pk("pessoa", "Thamires"),
                           "status": "nao_iniciada", "inclui_trilha_lideranca": nome in cfg["lideranca"],
                           "data_conversa": None, "comentario_geral": None, "nota_comportamental": None,
                           "nota_tecnica": None, "nota_indicadores": None, "nota_final": None})
        ids = [uid("comp", c[0]) for c in m.COMUNS]
        ids += [pk("comp", f["cargo"], t[1]) for t in f["tecnicas"]]
        if nome in cfg["lideranca"]:
            ids += [uid("comp", c[0]) for c in m.LIDERANCA]
        itens += [{"avaliacao_id": aid, "competencia_id": c, "nota_auto": None, "nota_gestor": None,
                   "nota_final": None, "evidencias": None} for c in ids]

    apur = pk("grat", "2027")
    return {
        "versao_schema": VERSAO_SCHEMA,
        "tipo": "empresa",
        "descricao": "Exemplo: Surcin Assessoria Empresarial. Organograma atual (documento 02) e proposta de "
                     "avaliação para validação da Thamires. Sem notas, valores, e-mails ou datas não informadas.",
        "empresa": {"id": emp, "nome": cfg["empresa"], "cnpj": None, "ramo": "Assessoria empresarial: "
                    "contabilidade, financeiro e jurídico"},
        "usuarios": [], "membros_empresa": [],
        "areas": areas, "cargos": cargos, "pessoas": pessoas, "vinculos": vinculos,
        "competencias": competencias, "cargo_competencias": cargo_comp,
        "indicadores": indicadores, "cargo_indicadores": cargo_ind,
        "politicas_avaliacao": [politica(pol, emp, "Proposta inicial Surcin (a validar)")],
        "ciclos_avaliacao": ciclos, "avaliacoes": avaliacoes, "avaliacao_itens": itens,
        "avaliacao_indicadores": [], "registros_assiduidade": [], "pdi_acoes": [],
        "gratificacao_apuracoes": [{"id": apur, "empresa_id": emp, "ano": 2027, "reserva_mensal": None,
                                    "meses_reserva": 12, "status": "aberta"}],
        "gratificacao_itens": [{"apuracao_id": apur, "pessoa_id": pk("pessoa", n),
                                "participa": "a_definir",
                                "valor_referencia": None, "nota_ano": None, "percentual": None,
                                "valor_calculado": None, "valor_ajustado": None} for n in cfg["pessoas"]],
    }


if __name__ == "__main__":
    saida = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(saida, exist_ok=True)
    for nome, dados in (("biblioteca-r2tech.json", biblioteca()), ("exemplo-surcin.json", surcin())):
        with open(os.path.join(saida, nome), "w", encoding="utf-8") as fh:
            json.dump(dados, fh, ensure_ascii=False, indent=2)
        print(os.path.join(saida, nome))
