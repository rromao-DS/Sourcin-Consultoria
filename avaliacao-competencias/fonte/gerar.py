# -*- coding: utf-8 -*-
"""Gera o modelo genérico da R2 Tech e o caso Surcin (Word e Excel).

Uso: python3 gerar.py [pasta_de_saida]
Saída: <pasta>/modelo-r2tech/ (genérico), <pasta>/ (Surcin) e <pasta>/estrutura-dados/ (cópia de dados/).
Também regenera os JSON de dados/ (gerar_dados.py e gerar_schema_json.py).
"""
import json
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import casos  # noqa: E402
import gerar_excel  # noqa: E402
import gerar_word  # noqa: E402
import gerar_dados  # noqa: E402
import gerar_schema_json  # noqa: E402

if __name__ == "__main__":
    saida = sys.argv[1] if len(sys.argv) > 1 else "."
    pasta_modelo = os.path.join(saida, "modelo-r2tech")
    for c in (gerar_word.doc_generico(casos.GENERICO, pasta_modelo),
              gerar_excel.gerar(casos.GENERICO, pasta_modelo),
              gerar_word.doc_surcin(casos.SURCIN, saida),
              gerar_excel.gerar(casos.SURCIN, saida)):
        print(c)

    dados = os.path.join(AQUI, "..", "dados")
    for nome, conteudo in (("biblioteca-r2tech.json", gerar_dados.biblioteca()),
                           ("exemplo-surcin.json", gerar_dados.surcin()),
                           ("pacote.schema.json", gerar_schema_json.schema())):
        with open(os.path.join(dados, nome), "w", encoding="utf-8") as fh:
            json.dump(conteudo, fh, ensure_ascii=False, indent=2)
    destino = os.path.join(saida, "estrutura-dados")
    shutil.copytree(dados, destino, dirs_exist_ok=True)
    print(destino)
