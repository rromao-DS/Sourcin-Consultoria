# -*- coding: utf-8 -*-
"""Gera o modelo genérico da R2 Tech e o caso Surcin (Word e Excel).

Uso: python3 gerar.py [pasta_de_saida]
Saída: <pasta>/modelo-r2tech/ (genérico) e <pasta>/ (Surcin).
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import casos  # noqa: E402
import gerar_excel  # noqa: E402
import gerar_word  # noqa: E402

if __name__ == "__main__":
    saida = sys.argv[1] if len(sys.argv) > 1 else "."
    pasta_modelo = os.path.join(saida, "modelo-r2tech")
    for c in (gerar_word.doc_generico(casos.GENERICO, pasta_modelo),
              gerar_excel.gerar(casos.GENERICO, pasta_modelo),
              gerar_word.doc_surcin(casos.SURCIN, saida),
              gerar_excel.gerar(casos.SURCIN, saida)):
        print(c)
