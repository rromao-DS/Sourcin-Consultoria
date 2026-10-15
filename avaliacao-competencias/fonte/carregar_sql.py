# -*- coding: utf-8 -*-
"""Converte pacotes JSON (biblioteca e empresa) em INSERTs para dados/schema.sql.

Uso: python3 carregar_sql.py pacote1.json [pacote2.json ...] > carga.sql
"""
import json
import sys

from gerar_schema_json import LISTAS

ORDEM = ["usuarios", "membros_empresa", "areas", "cargos", "pessoas", "vinculos", "competencias",
         "cargo_competencias", "indicadores", "cargo_indicadores", "politicas_avaliacao", "ciclos_avaliacao",
         "avaliacoes", "avaliacao_itens", "avaliacao_indicadores", "registros_assiduidade", "pdi_acoes",
         "gratificacao_apuracoes", "gratificacao_itens"]


def lit(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, (list, dict)):
        return "'" + json.dumps(v, ensure_ascii=False).replace("'", "''") + "'::jsonb"
    return "'" + str(v).replace("'", "''") + "'"


def inserts(tabela, linhas):
    for li in linhas:
        cols = ", ".join(li)
        vals = ", ".join(lit(v) for v in li.values())
        yield f"insert into app.{tabela} ({cols}) values ({vals});"


if __name__ == "__main__":
    print("begin;")
    for arq in sys.argv[1:]:
        with open(arq, encoding="utf-8") as fh:
            p = json.load(fh)
        if p.get("empresa"):
            print("\n".join(inserts("empresa", [p["empresa"]])))
        for chave in ORDEM:
            print("\n".join(inserts(LISTAS[chave], p.get(chave, []))))
    print("commit;")
