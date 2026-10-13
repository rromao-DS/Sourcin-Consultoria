# -*- coding: utf-8 -*-
"""Gera o deck da apresentação da proposta Surcin (versão preliminar)."""
import sys
from pptx import Presentation
from pptx.util import Cm, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

SAIDA = sys.argv[1] if len(sys.argv) > 1 else "."
AZUL = RGBColor(0x1F, 0x3A, 0x5F)
CLARO = RGBColor(0xE8, 0xEE, 0xF5)
CINZA = RGBColor(0x59, 0x59, 0x59)
BRANCO = RGBColor(0xFF, 0xFF, 0xFF)
AMARELO = RGBColor(0xFF, 0xF4, 0xD6)

prs = Presentation()
prs.slide_width, prs.slide_height = Cm(33.867), Cm(19.05)
VAZIO = prs.slide_layouts[6]


def caixa(slide, x, y, w, h, texto="", tam=16, cor=CINZA, negrito=False, fundo=None):
    if fundo is not None:
        s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Cm(x), Cm(y), Cm(w), Cm(h))
        s.fill.solid()
        s.fill.fore_color.rgb = fundo
        s.line.fill.background()
        s.adjustments[0] = 0.08
        s.shadow.inherit = False
    else:
        s = slide.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
    tf = s.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = tf.margin_right = tf.margin_top = Cm(0.5)
    linhas = texto if isinstance(texto, list) else [texto]
    for i, l in enumerate(linhas):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r = p.add_run()
        r.text = l
        r.font.size = Pt(tam)
        r.font.color.rgb = cor
        r.font.bold = negrito or (fundo is not None and i == 0)
        p.alignment = PP_ALIGN.LEFT
        r.font.name = "Calibri"
        p.space_after = Pt(6)
    return s


def slide_titulo(titulo, subtitulo=None):
    s = prs.slides.add_slide(VAZIO)
    faixa = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Cm(0.5))
    faixa.fill.solid()
    faixa.fill.fore_color.rgb = AZUL
    faixa.line.fill.background()
    caixa(s, 1.8, 1.3, 30, 2, titulo, 30, AZUL, True)
    if subtitulo:
        caixa(s, 1.8, 3.2, 30, 1.2, subtitulo, 16, CINZA)
    caixa(s, 1.8, 17.6, 30, 0.8, "Surcin Consultoria · Proposta de consultoria · Confidencial", 9, CINZA)
    return s


# 1 · Capa
s = prs.slides.add_slide(VAZIO)
bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid()
bg.fill.fore_color.rgb = AZUL
bg.line.fill.background()
caixa(s, 2.5, 5.5, 29, 2.5, "Organização, estrutura e processos", 40, BRANCO, True)
caixa(s, 2.5, 8.3, 29, 1.5, "Proposta de consultoria para a Surcin Consultoria", 22, BRANCO)
caixa(s, 2.5, 13.5, 29, 1.2, "Renato [sobrenome] · 15 de outubro de 2026", 16, BRANCO)

# 2 · O que eu entendi
s = slide_titulo("O que eu entendi", "Nossa reunião de 2h30 já é o início do diagnóstico")
caixa(s, 1.8, 5, 14.5, 10.5, ["Áreas", "Departamento Pessoal", "Financeiro", "Contabilidade", "Vendas",
                              "", "Ferramentas", "Conta Azul · Domínio · Veri · Jusbrasil", "OneDrive · Trello · NetsApp"],
      16, AZUL, fundo=CLARO)
caixa(s, 17.5, 5, 14.5, 10.5, ["Principais dores", "1. [PREENCHER com a transcrição]",
                               "2. [PREENCHER]", "3. [PREENCHER]", "",
                               "Objetivo: organizar e automatizar os processos do escritório"],
      16, AZUL, fundo=AMARELO)

# 3 · Como vamos trabalhar
s = slide_titulo("Como vamos trabalhar", "Entender antes de automatizar. Cada etapa termina com uma entrega e uma decisão sua.")
etapas = [("0", "Reunião de descoberta", "Concluída"),
          ("1", "Diagnóstico e estrutura organizacional", "Nesta proposta"),
          ("2", "Mapeamento detalhado de processos", "Nesta proposta"),
          ("3", "Implementação em pacotes", "Proposta futura"),
          ("4", "Acompanhamento mensal", "Opcional")]
for i, (n, nome, st) in enumerate(etapas):
    x = 1.8 + i * 6.1
    cor = AZUL if st == "Nesta proposta" else CLARO
    txt = BRANCO if st == "Nesta proposta" else AZUL
    caixa(s, x, 6, 5.7, 7, [f"Etapa {n}", nome, "", st], 15, txt, fundo=cor)

# 4 · Estrutura organizacional
s = slide_titulo("Estrutura organizacional", "Exemplo do entregável · hipótese inicial para validarmos juntas")
caixa(s, 12.4, 4.8, 9, 1.8, ["Direção · Thamires"], 16, BRANCO, True, fundo=AZUL)
areas = ["Departamento Pessoal", "Contabilidade e Fiscal", "Financeiro", "Comercial / Vendas", "Apoio adm. [?]"]
for i, a in enumerate(areas):
    caixa(s, 1.8 + i * 6.1, 8.2, 5.7, 2.4, [a, "Responsável: ?"], 13, AZUL, fundo=CLARO)
caixa(s, 1.8, 11.8, 30, 4.5, ["Entregável da Etapa 1: organograma atual e proposto, papéis e responsabilidades por área, "
                              "matriz RACI (quem executa, aprova, é consultado e informado) e as dependências da Direção."],
      15, CINZA)

# 5 · Mapeamento de processos
s = slide_titulo("Mapeamento de processos", "Quatro passos, sempre ouvindo quem executa")
passos = [("Ouvir", "Entrevistas de 45 a 60 min com a equipe: insumos, passos, sistemas, esperas"),
          ("Desenhar", "Fluxo atual em raias, validado por quem faz"),
          ("Encontrar gargalos", "Esperas, retrabalho, aprovações concentradas, dependências"),
          ("Otimizar", "Simplificar primeiro, depois listar automações com esforço e ganho")]
for i, (t, d) in enumerate(passos):
    caixa(s, 1.8 + i * 7.6, 5.5, 7.2, 8, [f"{i + 1}. {t}", "", d], 15, AZUL, fundo=CLARO)

# 6 · Entregáveis e cronograma
s = slide_titulo("Entregáveis e cronograma", "8 semanas, cerca de 10 horas por semana, reuniões fora do horário comercial")
caixa(s, 1.8, 5, 14.5, 10.8, ["Etapa 1 · semanas 1 a 4",
                              "• Entrevistas com a equipe (até 6)",
                              "• Inventário das ferramentas",
                              "• Relatório de diagnóstico",
                              "• Organograma, papéis e RACI",
                              "• Escolha dos processos prioritários"], 15, AZUL, fundo=CLARO)
caixa(s, 17.5, 5, 14.5, 10.8, ["Etapa 2 · semanas 5 a 8",
                               "• Até 4 processos mapeados",
                               "• Fluxos atuais e otimizados",
                               "• Gargalos e dependências",
                               "• Backlog de automação priorizado",
                               "• Proposta de implementação"], 15, AZUL, fundo=CLARO)

# 7 · Investimento
s = slide_titulo("Investimento", "Preço fechado por etapa. A implementação é orçada depois, por pacotes.")
precos = [("Etapa 1", "R$ 6.300", "Diagnóstico e estrutura"),
          ("Etapa 2", "R$ 6.800", "Mapeamento de até 4 processos"),
          ("Etapas 1 e 2", "R$ 11.900", "Contratadas juntas")]
for i, (t, v, d) in enumerate(precos):
    fundo = AZUL if i == 2 else CLARO
    cor = BRANCO if i == 2 else AZUL
    caixa(s, 1.8 + i * 10.2, 5.3, 9.6, 6.5, [t, v, d], 20, cor, True, fundo=fundo)
caixa(s, 1.8, 12.6, 30, 4, ["50% no início e 50% na entrega de cada etapa · processo adicional R$ 1.250",
                            "Fora do escopo: desenvolvimento de automações, integrações, suporte contínuo e licenças."],
      14, CINZA)

# 8 · Próximos passos
s = slide_titulo("Próximos passos")
caixa(s, 1.8, 4.5, 30, 10, ["1. Aceite da proposta (Etapa 1 ou Etapas 1 e 2)",
                            "2. Acordo de confidencialidade",
                            "3. Kick-off e agenda das entrevistas com a equipe",
                            "", "Perguntas para hoje:",
                            "• Quantas pessoas trabalham em cada área?",
                            "• Qual dor, se resolvida primeiro, mais mudaria o seu dia a dia?",
                            "• A equipe pode conversar antes das 10h, no almoço ou após 19h30?"], 18, AZUL)

prs.save(f"{SAIDA}/06-apresentacao-proposta.pptx")
print("ok")
