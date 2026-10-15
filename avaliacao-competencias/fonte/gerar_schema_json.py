# -*- coding: utf-8 -*-
"""Gera dados/pacote.schema.json (JSON Schema 2020-12) a partir de uma descrição das tabelas de dados/schema.sql.

O pacote é o formato de importação e exportação: uma chave por tabela, cada objeto com os nomes das colunas.
Uso: python3 gerar_schema_json.py [caminho_de_saida]
"""
import json
import os
import sys

UUID = {"type": "string", "format": "uuid"}
UUID_N = {"type": ["string", "null"], "format": "uuid"}
TXT = {"type": "string", "minLength": 1}
TXT_N = {"type": ["string", "null"]}
DATA = {"type": "string", "format": "date"}
DATA_N = {"type": ["string", "null"], "format": "date"}
BOOL = {"type": "boolean"}
INT = {"type": "integer"}
NUM_N = {"type": ["number", "null"]}
NOTA_N = {"type": ["integer", "null"], "minimum": 1, "maximum": 5}
NOTA_DEC_N = {"type": ["number", "null"], "minimum": 1, "maximum": 5}


def enum(*v, nulo=False):
    return {"enum": list(v) + ([None] if nulo else [])}


def faixas(chave_extra=None):
    props = {"a_partir_de": {"type": "number"}, "nota": {"type": "integer", "minimum": 1, "maximum": 5}}
    req = ["a_partir_de", "nota"]
    if chave_extra:
        props = {"a_partir_de": {"type": "number"}, "percentual": {"type": "number", "minimum": 0},
                 "faixa": TXT}
        req = ["a_partir_de", "percentual", "faixa"]
    return {"type": "array", "minItems": 1,
            "items": {"type": "object", "properties": props, "required": req, "additionalProperties": False}}


# tabela -> (descrição, {coluna: tipo}, obrigatórias)
T = {
    "usuario": ("Login no site.", {"id": UUID, "email": {"type": "string", "format": "email"}, "nome": TXT},
                ["id", "email", "nome"]),
    "empresa": ("Escritório cliente (inquilino).", {"id": UUID, "nome": TXT, "cnpj": TXT_N, "ramo": TXT_N},
                ["id", "nome"]),
    "membro_empresa": ("Papel de um usuário numa empresa.",
                       {"empresa_id": UUID, "usuario_id": UUID,
                        "papel": enum("admin", "avaliador", "colaborador")},
                       ["empresa_id", "usuario_id", "papel"]),
    "area": ("Área ou setor.", {"id": UUID, "empresa_id": UUID, "nome": TXT, "area_pai_id": UUID_N, "ordem": INT},
             ["id", "empresa_id", "nome"]),
    "cargo": ("Cargo ou função.", {"id": UUID, "empresa_id": UUID, "area_id": UUID_N, "nome": TXT,
                                   "missao": TXT_N, "responsabilidades": TXT_N, "ativo": BOOL},
              ["id", "empresa_id", "nome"]),
    "pessoa": ("Funcionário. Sem CPF, salário ou dados de saúde.",
               {"id": UUID, "empresa_id": UUID, "usuario_id": UUID_N, "nome": TXT,
                "email": {"type": ["string", "null"]}, "ativo": BOOL, "observacoes": TXT_N},
               ["id", "empresa_id", "nome"]),
    "vinculo": ("Ocupação de cargo e subordinação; organograma = vínculos sem data_fim.",
                {"id": UUID, "empresa_id": UUID, "pessoa_id": UUID, "cargo_id": UUID, "gestor_pessoa_id": UUID_N,
                 "tipo": enum("clt", "estagio", "pj", "socio", "outro", "nao_informado"), "jornada": TXT_N,
                 "data_inicio": DATA_N, "data_fim": DATA_N},
                ["id", "empresa_id", "pessoa_id", "cargo_id", "tipo"]),
    "competencia": ("Competência. empresa_id nulo = biblioteca R2 Tech.",
                    {"id": UUID, "empresa_id": UUID_N, "tipo": enum("comportamental", "tecnica", "lideranca"),
                     "area_biblioteca": TXT_N, "codigo": TXT_N, "nome": TXT, "definicao": TXT_N, "nivel_1": TXT_N,
                     "nivel_3": TXT, "nivel_5": TXT_N, "evidencia_sugerida": TXT_N, "origem": TXT_N, "ativo": BOOL},
                    ["id", "tipo", "nome", "nivel_3"]),
    "cargo_competencia": ("Competências técnicas de um cargo.",
                          {"cargo_id": UUID, "competencia_id": UUID, "codigo": TXT, "ordem": INT,
                           "texto_atender": TXT_N, "evidencia": TXT_N},
                          ["cargo_id", "competencia_id", "codigo"]),
    "indicador": ("Indicador objetivo. empresa_id nulo = padrão R2 Tech.",
                  {"id": UUID, "empresa_id": UUID_N, "tipo": enum("faltas_injustificadas", "atrasos", "percentual"),
                   "nome": TXT, "fonte": TXT_N, "tabela_conversao": {"oneOf": [{"type": "null"}, faixas()]}},
                  ["id", "tipo", "nome"]),
    "cargo_indicador": ("Indicadores de resultado de um cargo.",
                        {"cargo_id": UUID, "indicador_id": UUID, "ordem": INT}, ["cargo_id", "indicador_id"]),
    "politica_avaliacao": ("Regras de cálculo. empresa_id nulo = padrão R2 Tech.",
                           {"id": UUID, "empresa_id": UUID_N, "nome": TXT,
                            "peso_comportamental": {"type": "number", "minimum": 0, "maximum": 1},
                            "peso_tecnico": {"type": "number", "minimum": 0, "maximum": 1},
                            "peso_indicadores": {"type": "number", "minimum": 0, "maximum": 1},
                            "conversao_faltas": faixas(), "conversao_atrasos": faixas(),
                            "conversao_percentual": faixas(), "faixas_gratificacao": faixas(True),
                            "periodicidade": enum("semestral", "anual", "trimestral"),
                            "atestado_reduz_nota": BOOL, "validada_em": DATA_N},
                           ["id", "nome", "peso_comportamental", "peso_tecnico", "peso_indicadores",
                            "conversao_faltas", "conversao_atrasos", "conversao_percentual", "faixas_gratificacao"]),
    "ciclo_avaliacao": ("Período de avaliação.",
                        {"id": UUID, "empresa_id": UUID, "politica_id": UUID, "nome": TXT,
                         "tipo": enum("piloto", "regular"), "data_inicio": DATA, "data_fim": DATA,
                         "status": enum("planejado", "aberto", "em_avaliacao", "fechado"),
                         "efeito_financeiro": BOOL},
                        ["id", "empresa_id", "politica_id", "nome", "data_inicio", "data_fim"]),
    "avaliacao": ("Avaliação de uma pessoa num ciclo.",
                  {"id": UUID, "empresa_id": UUID, "ciclo_id": UUID, "pessoa_id": UUID, "cargo_id": UUID,
                   "avaliador_pessoa_id": UUID_N,
                   "status": enum("nao_iniciada", "autoavaliacao", "avaliacao_gestor", "conversa", "fechada"),
                   "inclui_trilha_lideranca": BOOL, "data_conversa": DATA_N, "comentario_geral": TXT_N,
                   "nota_comportamental": NOTA_DEC_N, "nota_tecnica": NOTA_DEC_N,
                   "nota_indicadores": NOTA_DEC_N, "nota_final": NOTA_DEC_N},
                  ["id", "empresa_id", "ciclo_id", "pessoa_id", "cargo_id"]),
    "avaliacao_item": ("Nota de uma competência numa avaliação.",
                       {"avaliacao_id": UUID, "competencia_id": UUID, "nota_auto": NOTA_N, "nota_gestor": NOTA_N,
                        "nota_final": NOTA_N, "evidencias": TXT_N},
                       ["avaliacao_id", "competencia_id"]),
    "avaliacao_indicador": ("Valor de um indicador de resultado (fração: 0.96 = 96%).",
                            {"avaliacao_id": UUID, "indicador_id": UUID, "valor": NUM_N, "observacao": TXT_N},
                            ["avaliacao_id", "indicador_id"]),
    "registro_assiduidade": ("Contagens do mês. Sem atestado, CID ou motivo de saúde.",
                             {"id": UUID, "empresa_id": UUID, "pessoa_id": UUID,
                              "mes": {"type": "string", "format": "date", "pattern": "^\\d{4}-\\d{2}-01$"},
                              "faltas_injustificadas": {"type": "integer", "minimum": 0},
                              "atrasos": {"type": "integer", "minimum": 0},
                              "faltas_justificadas": {"type": "integer", "minimum": 0}, "observacao": TXT_N},
                             ["id", "empresa_id", "pessoa_id", "mes"]),
    "pdi_acao": ("Ação do plano de desenvolvimento.",
                 {"id": UUID, "avaliacao_id": UUID, "competencia_id": UUID_N, "acao": TXT, "apoio_empresa": TXT_N,
                  "prazo": DATA_N, "status": enum("nao_iniciada", "em_andamento", "concluida"), "comentario": TXT_N},
                 ["id", "avaliacao_id", "acao"]),
    "gratificacao_apuracao": ("Apuração anual da gratificação (fundo = reserva_mensal x meses_reserva).",
                              {"id": UUID, "empresa_id": UUID, "ano": INT, "reserva_mensal": NUM_N,
                               "meses_reserva": INT, "status": enum("aberta", "fechada", "paga")},
                              ["id", "empresa_id", "ano"]),
    "gratificacao_item": ("Gratificação de uma pessoa no ano.",
                          {"apuracao_id": UUID, "pessoa_id": UUID, "participa": enum("sim", "nao", "a_definir"),
                           "valor_referencia": NUM_N, "nota_ano": NOTA_DEC_N, "percentual": NUM_N,
                           "valor_calculado": NUM_N, "valor_ajustado": NUM_N},
                          ["apuracao_id", "pessoa_id", "participa"]),
}

# chave do pacote -> tabela
LISTAS = {
    "usuarios": "usuario", "membros_empresa": "membro_empresa", "areas": "area", "cargos": "cargo",
    "pessoas": "pessoa", "vinculos": "vinculo", "competencias": "competencia",
    "cargo_competencias": "cargo_competencia", "indicadores": "indicador", "cargo_indicadores": "cargo_indicador",
    "politicas_avaliacao": "politica_avaliacao", "ciclos_avaliacao": "ciclo_avaliacao", "avaliacoes": "avaliacao",
    "avaliacao_itens": "avaliacao_item", "avaliacao_indicadores": "avaliacao_indicador",
    "registros_assiduidade": "registro_assiduidade", "pdi_acoes": "pdi_acao",
    "gratificacao_apuracoes": "gratificacao_apuracao", "gratificacao_itens": "gratificacao_item",
}


def schema():
    defs = {nome: {"description": d, "type": "object", "properties": p, "required": r,
                   "additionalProperties": False} for nome, (d, p, r) in T.items()}
    props = {"versao_schema": {"const": "1.0"}, "tipo": enum("biblioteca", "empresa"), "descricao": TXT_N,
             "empresa": {"$ref": "#/$defs/empresa"}}
    props.update({k: {"type": "array", "items": {"$ref": f"#/$defs/{t}"}} for k, t in LISTAS.items()})
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://r2tech.consultoria/schemas/avaliacao-competencias/pacote-1.0.json",
        "title": "Pacote de avaliação por competências (R2 Tech Consultoria)",
        "description": "Formato de importação/exportação. Uma chave por tabela de schema.sql; cada objeto usa os "
                       "nomes das colunas. tipo=biblioteca traz os registros padrão (empresa_id nulo); "
                       "tipo=empresa traz um escritório completo.",
        "type": "object",
        "properties": props,
        "required": ["versao_schema", "tipo"],
        "additionalProperties": False,
        "if": {"properties": {"tipo": {"const": "empresa"}}},
        "then": {"required": ["empresa"]},
        "$defs": defs,
    }


if __name__ == "__main__":
    padrao = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados", "pacote.schema.json")
    caminho = sys.argv[1] if len(sys.argv) > 1 else padrao
    with open(caminho, "w", encoding="utf-8") as fh:
        json.dump(schema(), fh, ensure_ascii=False, indent=2)
    print(caminho)
