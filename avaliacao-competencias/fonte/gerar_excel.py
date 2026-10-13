# -*- coding: utf-8 -*-
"""Gera a planilha de aplicação da avaliação por competências (modelo R2 Tech ou caso de cliente)."""
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import base as m  # noqa: E402

AZUL = "1F3A5F"
F_TIT = Font(bold=True, size=16, color=AZUL)
F_SUB = Font(italic=True, size=9, color="595959")
F_CAB = Font(bold=True, color="FFFFFF")
F_NEG = Font(bold=True)
P_CAB = PatternFill("solid", fgColor=AZUL)
P_ENT = PatternFill("solid", fgColor="FFF4D6")   # célula de preenchimento
P_CALC = PatternFill("solid", fgColor="E8EEF5")  # célula calculada
FINO = Side(style="thin", color="BFBFBF")
BORDA = Border(left=FINO, right=FINO, top=FINO, bottom=FINO)
QUEBRA = Alignment(wrap_text=True, vertical="top")
CENTRO = Alignment(horizontal="center", vertical="center", wrap_text=True)
REAL = '"R$" #,##0.00'
LIN_PESSOA = 26  # primeira linha da tabela de pessoas na aba Parâmetros


def cab(ws, linha, textos, col=1):
    for i, t in enumerate(textos):
        c = ws.cell(row=linha, column=col + i, value=t)
        c.font, c.fill, c.alignment, c.border = F_CAB, P_CAB, CENTRO, BORDA


def cel(ws, ref, valor=None, fill=None, fonte=None, alin=QUEBRA, fmt=None):
    c = ws[ref]
    if valor is not None:
        c.value = valor
    c.border = BORDA
    c.alignment = alin
    if fill:
        c.fill = fill
    if fonte:
        c.font = fonte
    if fmt:
        c.number_format = fmt
    return c


def larguras(ws, d):
    for col, w in d.items():
        ws.column_dimensions[col].width = w


def gerar(cfg, saida):
    pessoas = list(cfg["pessoas"].items())
    n = len(pessoas)
    gestor = cfg["gestor"]
    generico = all(p["tecnicas"] is None for _, p in pessoas)
    comuns = m.comuns(cfg)
    wb = Workbook()

    def titulo(ws, texto):
        ws["A1"] = texto
        ws["A1"].font = F_TIT
        ws["A2"] = cfg["versao"]
        ws["A2"].font = F_SUB

    # ------------------------------------------------------------------ Instruções
    ws = wb.active
    ws.title = "Instruções"
    titulo(ws, f"Avaliação por competências · {cfg['empresa']}")
    passos = []
    if generico:
        passos += [
            "Modelo da R2 Tech Consultoria para qualquer empresa. Para adaptar a um cliente:",
            "a) Na aba Parâmetros, preencha empresa, gestor(a), ciclo e a tabela de pessoas (nome e cargo).",
            "b) Em cada aba de pessoa, escreva de 4 a 6 competências técnicas do cargo, escolhidas na aba Biblioteca "
            "e ajustadas ao processo real do cliente, e os 2 indicadores da função.",
            "c) Valide pesos, faixas e valores com a direção e com revisão trabalhista antes de anunciar à equipe.",
            "d) Apague as abas de pessoas que sobrarem e também as linhas delas nas abas Resumo, Assiduidade e PDI.",
            "",
        ]
    else:
        passos += ["Proposta para validação. Pesos, faixas e valores ficam na aba Parâmetros e podem ser alterados.", ""]
    passos += [
        "Células amarelas são de preenchimento; células azuis são calculadas. Não apague as fórmulas.",
        "Use um arquivo por ciclo (semestre) e preencha o nome do ciclo na aba Parâmetros.",
        "1. Todo mês, lance faltas injustificadas, atrasos e faltas justificadas/atestados na aba Assiduidade.",
        "2. No fim do semestre, cada pessoa preenche a coluna Autoavaliação da sua aba, com exemplos.",
        f"3. Quem avalia ({gestor}) preenche a coluna de avaliação e os dois indicadores da função (em %).",
        "4. Na conversa individual, fechem a Nota final. Se ficar em branco, vale a nota de quem avalia.",
        "5. Registre de 2 a 3 ações na aba PDI (plano de desenvolvimento individual).",
        "6. No 2º semestre, copie a nota final do 1º semestre para a aba Resumo. A nota do ano é a média dos dois.",
        "7. A gratificação é apurada só no fim do ano e fica limitada à reserva acumulada (aba Parâmetros).",
        "Escala: 1 Não atende · 2 Atende em parte · 3 Atende · 4 Supera · 5 Referência. "
        "A descrição de cada nível está na aba Competências.",
        "Atestados e faltas justificadas são só registrados e não reduzem a nota.",
        "Confidencial: cada pessoa vê só a própria aba. Guarde o arquivo em pasta de acesso restrito. "
        "Não anexe atestados aqui; registre só a quantidade.",
    ]
    for i, t in enumerate(passos, start=4):
        ws.cell(row=i, column=1, value=t).alignment = QUEBRA
    ws.column_dimensions["A"].width = 120

    # ------------------------------------------------------------------ Parâmetros
    pa = wb.create_sheet("Parâmetros")
    titulo(pa, "Parâmetros")
    cel(pa, "A4", "Ciclo", fonte=F_NEG)
    cel(pa, "B4", cfg["ciclo"], fill=P_ENT)
    cel(pa, "D4", "Empresa", fonte=F_NEG)
    cel(pa, "E4", cfg["empresa"], fill=P_ENT)
    cel(pa, "G4", "Quem avalia", fonte=F_NEG)
    cel(pa, "H4", gestor, fill=P_ENT)

    cab(pa, 6, ["Bloco", "Peso"])
    for i, (nome, peso) in enumerate(m.PESOS):
        cel(pa, f"A{7 + i}", nome)
        cel(pa, f"B{7 + i}", peso, fill=P_ENT, fmt="0%")
    cel(pa, "A10", "Soma (deve ser 100%)", fonte=F_NEG)
    cel(pa, "B10", "=SUM(B7:B9)", fill=P_CALC, fmt="0%")

    cab(pa, 12, ["Faltas injustificadas (a partir de)", "Nota"])
    for i, (lim, nota) in enumerate(m.ASSIDUIDADE[0][1]):
        cel(pa, f"A{13 + i}", lim, fill=P_ENT)
        cel(pa, f"B{13 + i}", nota, fill=P_ENT)
    cab(pa, 12, ["Atrasos (a partir de)", "Nota"], col=4)
    for i, (lim, nota) in enumerate(m.ASSIDUIDADE[1][1]):
        cel(pa, f"D{13 + i}", lim, fill=P_ENT)
        cel(pa, f"E{13 + i}", nota, fill=P_ENT)
    cab(pa, 12, ["Cumprimento do indicador (a partir de)", "Nota"], col=7)
    for i, (lim, nota) in enumerate(m.FAIXAS_PCT):
        cel(pa, f"G{13 + i}", lim, fill=P_ENT, fmt="0%")
        cel(pa, f"H{13 + i}", nota, fill=P_ENT)

    cab(pa, 19, ["Nota do ano (a partir de)", "% da referência", "Faixa"])
    for i, (lim, pct, txt) in enumerate(m.FAIXAS_GRAT):
        cel(pa, f"A{20 + i}", lim, fill=P_ENT, fmt="0.00")
        cel(pa, f"B{20 + i}", pct, fill=P_ENT, fmt="0%")
        cel(pa, f"C{20 + i}", txt.split(":")[0], fill=P_ENT)

    cab(pa, LIN_PESSOA - 1, ["Nome", "Valor de referência da gratificação (R$)", "Participa da gratificação?", "Cargo"])
    for i, (p, f) in enumerate(pessoas):
        r = LIN_PESSOA + i
        cel(pa, f"A{r}", p, fill=P_ENT if generico else None)
        cel(pa, f"B{r}", 0, fill=P_ENT, fmt=REAL)
        cel(pa, f"C{r}", cfg["participa"].get(p, "Sim"), fill=P_ENT)
        cel(pa, f"D{r}", f["cargo"], fill=P_ENT)
    ult_p = LIN_PESSOA + n - 1
    r_res = ult_p + 2
    cel(pa, f"A{r_res}", "Reserva mensal para o fundo (R$)", fonte=F_NEG)
    cel(pa, f"B{r_res}", 0, fill=P_ENT, fmt=REAL)
    cel(pa, f"A{r_res + 1}", "Meses de reserva no ano", fonte=F_NEG)
    cel(pa, f"B{r_res + 1}", 12, fill=P_ENT)
    cel(pa, f"A{r_res + 2}", "Fundo disponível no fim do ano (R$)", fonte=F_NEG)
    cel(pa, f"B{r_res + 2}", f"=B{r_res}*B{r_res + 1}", fill=P_CALC, fmt=REAL)
    fundo = f"Parâmetros!$B${r_res + 2}"
    pa[f"A{r_res + 4}"] = "Valores zerados de propósito: a direção define a referência e a reserva."
    pa[f"A{r_res + 4}"].font = F_SUB
    dv_sim = DataValidation(type="list", formula1='"Sim,Não,A definir"', allow_blank=True)
    pa.add_data_validation(dv_sim)
    dv_sim.add(f"C{LIN_PESSOA}:C{ult_p}")
    larguras(pa, {"A": 42, "B": 26, "C": 26, "D": 30, "E": 26, "G": 26, "H": 18})

    def nome_ref(i):
        return f"Parâmetros!$A${LIN_PESSOA + i}"

    # ------------------------------------------------------------------ Competências
    co = wb.create_sheet("Competências")
    titulo(co, "Competências e níveis")
    cab(co, 4, ["Código", "Competência comum", "Definição", "Nível 1", "Nível 3", "Nível 5"])
    li = 5
    for linha in comuns:
        for j, v in enumerate(linha):
            cel(co, f"{'ABCDEF'[j]}{li}", v)
        li += 1
    if not generico:
        li += 1
        cab(co, li, ["Código", "Pessoa · competência técnica", "O que é atender (nota 3)", "Evidência"])
        li += 1
        for p, f in pessoas:
            for cod, nome, atende, evid in f["tecnicas"]:
                for j, v in enumerate([cod, f"{p} · {nome}", atende, evid]):
                    cel(co, f"{'ABCD'[j]}{li}", v)
                li += 1
    li += 1
    cab(co, li, ["Código", "Trilha de liderança", "O que se espera"])
    li += 1
    for linha in m.LIDERANCA:
        for j, v in enumerate(linha):
            cel(co, f"{'ABC'[j]}{li}", v)
        li += 1
    larguras(co, {"A": 8, "B": 32, "C": 45, "D": 35, "E": 35, "F": 35})

    # ------------------------------------------------------------------ Biblioteca
    bi = wb.create_sheet("Biblioteca")
    titulo(bi, "Biblioteca de competências técnicas por área")
    bi["A3"] = "Escolha de 4 a 6 por cargo e ajuste ao processo real do cliente. A régua é sempre a nota 3 (atende)."
    bi["A3"].font = F_SUB
    cab(bi, 4, ["Área", "Competência", "O que é atender (nota 3)", "Evidência / indicador sugerido"])
    li = 5
    for area, itens in m.BIBLIOTECA.items():
        for nome, atende, evid in itens:
            for j, v in enumerate([area, nome, atende, evid]):
                cel(bi, f"{'ABCD'[j]}{li}", v)
            li += 1
    larguras(bi, {"A": 26, "B": 34, "C": 60, "D": 36})
    bi.freeze_panes = "A5"
    bi.auto_filter.ref = f"A4:D{li - 1}"

    # ------------------------------------------------------------------ Assiduidade
    asd = wb.create_sheet("Assiduidade")
    titulo(asd, "Registro mensal de assiduidade")
    asd["A3"] = "=\"Ciclo: \"&Parâmetros!B4"
    cab(asd, 4, ["Mês", "Pessoa", "Faltas injustificadas", "Atrasos",
                 "Faltas justificadas / atestados (só registro)", "Observação"])
    li = 5
    for mes in range(1, 7):
        for i in range(n):
            cel(asd, f"A{li}", f"Mês {mes}", fill=P_ENT)
            cel(asd, f"B{li}", f"={nome_ref(i)}", fill=P_CALC)
            for col in "CDE":
                cel(asd, f"{col}{li}", 0, fill=P_ENT, alin=CENTRO)
            cel(asd, f"F{li}", None, fill=P_ENT)
            li += 1
    ult_asd = li - 1
    dv_int = DataValidation(type="whole", operator="between", formula1="0", formula2="200", allow_blank=True)
    asd.add_data_validation(dv_int)
    dv_int.add(f"C5:E{ult_asd}")
    larguras(asd, {"A": 12, "B": 16, "C": 14, "D": 10, "E": 22, "F": 40})
    asd.freeze_panes = "A5"

    def soma_asd(col, i):
        return f"=SUMIFS(Assiduidade!${col}$5:${col}${ult_asd},Assiduidade!$B$5:$B${ult_asd},{nome_ref(i)})"

    # ------------------------------------------------------------------ Abas individuais
    refs = []
    for i, (p, f) in enumerate(pessoas):
        ws = wb.create_sheet(p)
        r_par = LIN_PESSOA + i
        ws["A1"] = f"=Parâmetros!A{r_par}&\" · \"&Parâmetros!D{r_par}"
        ws["A1"].font = F_TIT
        ws["A2"] = cfg["versao"]
        ws["A2"].font = F_SUB
        ws["A3"] = "=\"Ciclo: \"&Parâmetros!B4"
        ws["A3"].font = F_NEG
        cab(ws, 5, ["Bloco", "Código", "Competência", "Autoavaliação", f"Avaliação {gestor}",
                    "Nota final (acordada)", "Nota considerada", "Exemplos e evidências do período"])
        dv_nota = DataValidation(type="whole", operator="between", formula1="1", formula2="5", allow_blank=True,
                                 error="Use uma nota de 1 a 5.", errorTitle="Nota inválida")
        ws.add_data_validation(dv_nota)

        def linha_comp(li, bloco, cod, nome, editavel=False):
            cel(ws, f"A{li}", bloco)
            cel(ws, f"B{li}", cod, alin=CENTRO)
            cel(ws, f"C{li}", nome, fill=P_ENT if editavel else None)
            for col in "DEF":
                cel(ws, f"{col}{li}", None, fill=P_ENT, alin=CENTRO)
            dv_nota.add(f"D{li}:F{li}")
            cel(ws, f"G{li}", f'=IF(F{li}<>"",F{li},IF(E{li}<>"",E{li},""))', fill=P_CALC, alin=CENTRO)
            cel(ws, f"H{li}", None, fill=P_ENT)

        li = 6
        ini_c = li
        for cod, nome, *_ in comuns:
            linha_comp(li, "Comportamental", cod, nome)
            li += 1
        fim_c = li - 1
        ini_t = li
        tecnicas = f["tecnicas"] or [(f"T{k}", f"[Competência técnica {k}: escolha na Biblioteca]", "", "")
                                     for k in range(1, 6)]
        for cod, nome, *_ in tecnicas:
            linha_comp(li, "Técnica", cod, nome, editavel=f["tecnicas"] is None)
            li += 1
        fim_t = li - 1

        li += 1
        cab(ws, li, ["Bloco", "", "Indicador objetivo", "Valor do período", "", "", "Nota", "Fonte / observação"])
        li += 1
        ini_i = li
        for rotulo, col_asd, tab in (("Faltas injustificadas no semestre", "C", "$A$13:$A$17,Parâmetros!$B$13:$B$17"),
                                     ("Atrasos no semestre", "D", "$D$13:$D$17,Parâmetros!$E$13:$E$17")):
            cel(ws, f"A{li}", "Indicador")
            cel(ws, f"C{li}", rotulo)
            cel(ws, f"D{li}", soma_asd(col_asd, i), fill=P_CALC, alin=CENTRO)
            cel(ws, f"G{li}", f"=LOOKUP(D{li},Parâmetros!{tab})", fill=P_CALC, alin=CENTRO)
            cel(ws, f"H{li}", "Aba Assiduidade")
            li += 1
        indicadores = f["indicadores"] or [(f"[Indicador da função {k} (%)]", "[Fonte]") for k in (1, 2)]
        for nome_ind, fonte in indicadores:
            cel(ws, f"A{li}", "Indicador")
            cel(ws, f"C{li}", nome_ind, fill=P_ENT if f["indicadores"] is None else None)
            cel(ws, f"D{li}", None, fill=P_ENT, alin=CENTRO, fmt="0%")
            cel(ws, f"G{li}", f'=IF(D{li}="","",LOOKUP(D{li},Parâmetros!$G$13:$G$17,Parâmetros!$H$13:$H$17))',
                fill=P_CALC, alin=CENTRO)
            cel(ws, f"H{li}", fonte, fill=P_ENT)
            li += 1
        fim_i = li - 1
        cel(ws, f"A{li}", "Registro")
        cel(ws, f"C{li}", "Faltas justificadas / atestados (não entram na nota)")
        cel(ws, f"D{li}", soma_asd("E", i), fill=P_CALC, alin=CENTRO)
        li += 2

        cab(ws, li, ["Resultado", "", "Bloco", "Média", "Peso", "", "", ""])
        li += 1
        r_c, r_t, r_i = li, li + 1, li + 2
        for k, (nome_b, ini, fim, prow) in enumerate([
                (m.PESOS[0][0], ini_c, fim_c, 7), (m.PESOS[1][0], ini_t, fim_t, 8), (m.PESOS[2][0], ini_i, fim_i, 9)]):
            r = li + k
            cel(ws, f"C{r}", nome_b)
            cel(ws, f"D{r}", f'=IFERROR(ROUND(AVERAGE(G{ini}:G{fim}),2),"")', fill=P_CALC, alin=CENTRO, fmt="0.00")
            cel(ws, f"E{r}", f"=Parâmetros!B{prow}", fill=P_CALC, alin=CENTRO, fmt="0%")
        r_f = li + 3
        cel(ws, f"C{r_f}", "Nota final do ciclo", fonte=F_NEG)
        cel(ws, f"D{r_f}",
            f'=IF(OR(D{r_c}="",D{r_t}="",D{r_i}=""),"",ROUND(D{r_c}*E{r_c}+D{r_t}*E{r_t}+D{r_i}*E{r_i},2))',
            fill=P_CALC, alin=CENTRO, fonte=F_NEG, fmt="0.00")
        cel(ws, f"E{r_f}", f'=IF(D{r_f}="","",LOOKUP(D{r_f},Parâmetros!$A$20:$A$23,Parâmetros!$C$20:$C$23))',
            fill=P_CALC)
        ws.merge_cells(f"E{r_f}:H{r_f}")
        refs.append((r_c, r_t, r_i, r_f))

        li = r_f + 2
        if p in cfg["lideranca"]:
            rot = ("Trilha de liderança (opcional): desenvolvimento, não entra na nota nem na gratificação"
                   if generico else
                   "Trilha de supervisão: desenvolvimento, não entra na nota nem na gratificação")
            ws.cell(row=li, column=1, value=rot).font = F_NEG
            li += 1
            cab(ws, li, ["Bloco", "Código", "Competência", "Autoavaliação", f"Avaliação {gestor}", "", "",
                         "Exemplos e próximos passos"])
            li += 1
            for cod, nome, _ in m.LIDERANCA:
                cel(ws, f"A{li}", "Liderança")
                cel(ws, f"B{li}", cod, alin=CENTRO)
                cel(ws, f"C{li}", nome)
                for col in "DE":
                    cel(ws, f"{col}{li}", None, fill=P_ENT, alin=CENTRO)
                dv_nota.add(f"D{li}:E{li}")
                cel(ws, f"H{li}", None, fill=P_ENT)
                li += 1
            li += 1
        if f.get("obs"):
            ws.cell(row=li, column=1, value=f["obs"]).font = F_SUB

        for faixa in (f"G{ini_c}:G{fim_t}", f"G{ini_i}:G{fim_i}"):
            ws.conditional_formatting.add(faixa, CellIsRule(operator="lessThan", formula=["3"],
                                                            fill=PatternFill("solid", fgColor="F8D7DA")))
        larguras(ws, {"A": 15, "B": 8, "C": 44, "D": 14, "E": 16, "F": 14, "G": 12, "H": 50})
        ws.freeze_panes = "A6"

    # ------------------------------------------------------------------ Resumo
    rs = wb.create_sheet("Resumo", 1)
    titulo(rs, "Resumo do ciclo e gratificação")
    rs["A3"] = "=\"Ciclo: \"&Parâmetros!B4"
    cab(rs, 5, ["Pessoa", "Comportamentais", "Técnicas", "Indicadores", "Nota deste ciclo",
                "Nota do 1º semestre (copiar no 2º ciclo)", "Nota do ano", "Faixa", "% da referência",
                "Valor de referência", "Participa?", "Gratificação calculada", "Gratificação ajustada ao fundo"])
    tot = 6 + n
    for i, (p, _) in enumerate(pessoas):
        r = 6 + i
        r_c, r_t, r_i, r_f = refs[i]
        aba = f"'{p}'"
        cel(rs, f"A{r}", f"={nome_ref(i)}", fonte=F_NEG)
        cel(rs, f"B{r}", f"={aba}!D{r_c}", fill=P_CALC, alin=CENTRO, fmt="0.00")
        cel(rs, f"C{r}", f"={aba}!D{r_t}", fill=P_CALC, alin=CENTRO, fmt="0.00")
        cel(rs, f"D{r}", f"={aba}!D{r_i}", fill=P_CALC, alin=CENTRO, fmt="0.00")
        cel(rs, f"E{r}", f"={aba}!D{r_f}", fill=P_CALC, alin=CENTRO, fmt="0.00")
        cel(rs, f"F{r}", None, fill=P_ENT, alin=CENTRO, fmt="0.00")
        cel(rs, f"G{r}", f'=IF(E{r}="","",IF(F{r}="",E{r},ROUND(AVERAGE(E{r},F{r}),2)))',
            fill=P_CALC, alin=CENTRO, fmt="0.00")
        cel(rs, f"H{r}", f'=IF(G{r}="","",LOOKUP(G{r},Parâmetros!$A$20:$A$23,Parâmetros!$C$20:$C$23))', fill=P_CALC)
        cel(rs, f"I{r}", f'=IF(G{r}="","",LOOKUP(G{r},Parâmetros!$A$20:$A$23,Parâmetros!$B$20:$B$23))',
            fill=P_CALC, alin=CENTRO, fmt="0%")
        cel(rs, f"J{r}", f"=Parâmetros!B{LIN_PESSOA + i}", fill=P_CALC, fmt=REAL)
        cel(rs, f"K{r}", f"=Parâmetros!C{LIN_PESSOA + i}", fill=P_CALC, alin=CENTRO)
        cel(rs, f"L{r}", f'=IF(OR(I{r}="",K{r}<>"Sim"),0,ROUND(I{r}*J{r},2))', fill=P_CALC, fmt=REAL)
        cel(rs, f"M{r}", f"=IF(L${tot}=0,0,ROUND(L{r}*MIN(1,{fundo}/L${tot}),2))", fill=P_CALC, fmt=REAL)
    cel(rs, f"A{tot}", "Total", fonte=F_NEG)
    cel(rs, f"L{tot}", f"=SUM(L6:L{tot - 1})", fill=P_CALC, fonte=F_NEG, fmt=REAL)
    cel(rs, f"M{tot}", f"=SUM(M6:M{tot - 1})", fill=P_CALC, fonte=F_NEG, fmt=REAL)
    cel(rs, f"A{tot + 1}", "Fundo disponível", fonte=F_NEG)
    cel(rs, f"M{tot + 1}", f"={fundo}", fill=P_CALC, fmt=REAL)
    rs[f"A{tot + 3}"] = ("A gratificação é apurada só no fim do ano. Se a soma calculada passar do fundo, todas são "
                         "reduzidas na mesma proporção. Valores e forma de pagamento dependem de revisão trabalhista.")
    rs[f"A{tot + 3}"].font = F_SUB
    larguras(rs, {"A": 14, "B": 15, "C": 11, "D": 12, "E": 12, "F": 18, "G": 11, "H": 18, "I": 11,
                  "J": 14, "K": 11, "L": 15, "M": 17})
    rs.row_dimensions[5].height = 45

    # ------------------------------------------------------------------ PDI
    pdi = wb.create_sheet("PDI")
    titulo(pdi, "Plano de desenvolvimento individual")
    pdi["A3"] = "=\"Ciclo: \"&Parâmetros!B4"
    cab(pdi, 5, ["Pessoa", "Competência a desenvolver", "Ação combinada", "Apoio da empresa", "Prazo",
                 "Situação", "Comentário no acompanhamento"])
    li = 6
    dv_sit = DataValidation(type="list", formula1='"Não iniciada,Em andamento,Concluída"', allow_blank=True)
    pdi.add_data_validation(dv_sit)
    for i in range(n):
        for _ in range(3):
            cel(pdi, f"A{li}", f"={nome_ref(i)}", fill=P_CALC)
            for col in "BCDEFG":
                cel(pdi, f"{col}{li}", None, fill=P_ENT)
            pdi[f"E{li}"].number_format = "dd/mm/yyyy"
            li += 1
    dv_sit.add(f"F6:F{li - 1}")
    larguras(pdi, {"A": 13, "B": 30, "C": 45, "D": 30, "E": 12, "F": 15, "G": 40})

    os.makedirs(saida, exist_ok=True)
    caminho = os.path.join(saida, cfg["arquivo"] + ".xlsx")
    wb.save(caminho)
    return caminho
