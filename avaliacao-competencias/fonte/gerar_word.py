# -*- coding: utf-8 -*-
"""Gera os documentos Word: modelo genérico da R2 Tech e aplicação a um cliente (Surcin)."""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "proposta-surcin", "fonte"))
import gerar_docs as gd  # noqa: E402  (reaproveita o padrão visual da proposta)
from gerar_docs import h, par, lista, tabela, aviso  # noqa: E402
import base as m  # noqa: E402

CONSULTOR = gd.CONSULTOR


def novo(cfg, titulo, subtitulo, rodape):
    gd.VERSAO = cfg["versao"]
    d = gd.novo_doc(titulo, subtitulo)
    d.sections[0].footer.paragraphs[0].runs[0].text = rodape
    return d


# ---------------------------------------------------------------------------
# Seções comuns aos dois documentos
# ---------------------------------------------------------------------------
def sec_principios(d, num, cfg):
    h(d, f"{num}. Princípios do modelo")
    lista(d, [
        ("Avalia o profissional, não a pessoa. ", "Cada nota se apoia em fatos e exemplos do período."),
        ("Qualidade antes de volume. ", "Tarefa concluída sem evidência não conta como entrega."),
        ("Dado objetivo mais conversa. ", "Indicadores dos sistemas entram na nota; o restante é avaliado por "
         f"quem avalia ({cfg['gestor']}), depois da autoavaliação de cada pessoa."),
        ("A régua é o cargo. ", "Competências comportamentais iguais para todos; competências técnicas próprias "
         "de cada cargo."),
        ("Serve para desenvolver. ", "Toda avaliação termina com um plano de desenvolvimento curto, com duas ou três "
         "ações."),
        ("Regras por escrito e iguais para todos. ", "As regras são entregues à equipe antes do início do ciclo."),
    ])


def sec_estrutura(d, num):
    h(d, f"{num}. Estrutura da nota")
    par(d, "A nota final vai de 1 a 5 e é a média ponderada de três blocos:")
    tabela(d, ["Bloco", "O que entra", "Peso sugerido"], [
        [m.PESOS[0][0], "8 competências, as mesmas para toda a equipe", "40%"],
        [m.PESOS[1][0], "4 a 6 competências do cargo de cada pessoa", "40%"],
        [m.PESOS[2][0], "Faltas injustificadas, atrasos e 2 indicadores de resultado do cargo", "20%"],
    ], [5.5, 8, 2.5])
    h(d, "Escala de 1 a 5", 2)
    tabela(d, ["Nota", "Nível", "Significado"], [[str(n), nv, s] for n, nv, s in m.ESCALA], [1.5, 3, 11.5])
    par(d, "A nota 3 é a de quem está bem no cargo. Notas 4 e 5 pedem exemplos concretos do período, e notas 1 e "
           "2 pedem exemplos e uma ação no plano de desenvolvimento.", italico=True)


def sec_passos(d, cfg, nivel=2):
    h(d, "Passos de cada avaliação", nivel)
    lista(d, [
        "Cada pessoa preenche a autoavaliação na planilha, com exemplos.",
        f"Quem avalia ({cfg['gestor']}) preenche a avaliação e lança os indicadores do semestre.",
        "Conversa individual de cerca de 1 hora: comparar as duas visões e fechar a nota final.",
        "Plano de desenvolvimento com duas ou três ações, prazo e apoio da empresa.",
        "Acompanhamento mensal curto (30 minutos) para ver o plano e os indicadores.",
    ], numerada=True)


def sec_comuns(d, num, cfg):
    h(d, f"{num}. Competências comportamentais (comuns)")
    par(d, "Descrição dos níveis 1, 3 e 5. As notas 2 e 4 ficam entre eles.")
    for cod, nome, defin, n1, n3, n5 in m.comuns(cfg):
        h(d, f"{cod} · {nome}", 3)
        par(d, defin)
        tabela(d, ["Nível 1", "Nível 3", "Nível 5"], [[n1, n3, n5]], [5.3, 5.3, 5.4])
        if cfg["origens"].get(cod):
            par(d, f"Origem: {cfg['origens'][cod]}.", italico=True)


def sec_indicadores(d, num, cfg, remoto=False):
    h(d, f"{num}. Indicadores objetivos")
    tabela(d, ["Indicador", "Como vira nota", "Fonte"], [
        [m.ASSIDUIDADE[0][0], m.ASSIDUIDADE[0][2], "Controle de ponto ou registro de quem avalia"],
        [m.ASSIDUIDADE[1][0], m.ASSIDUIDADE[1][2], "Controle de ponto ou registro de quem avalia"],
        ["Atestados e faltas justificadas", "Só registro. Não reduz a nota", "Registro de DP"],
        ["2 indicadores de resultado do cargo", m.FAIXAS_PCT_TXT, "Sistemas e controle de tarefas"],
    ], [4.5, 7.5, 4])
    aviso(d, "Atestados: recomendamos registrar, mas não descontar pontos por falta justificada ou atestado "
             "médico. Penalizar ausência legalmente justificada cria risco trabalhista e de discriminação. A decisão "
             "final é da direção, com revisão trabalhista.")
    itens = []
    if remoto:
        itens.append(("Atraso em trabalho remoto. ", "A Surcin atua de forma remota (briefing, seção 2). É preciso "
                      "definir o que conta como atraso: registro de ponto, início no sistema ou primeira resposta no "
                      "WhatsApp."))
    else:
        itens.append(("Atraso. ", "Definir com a direção o que conta como atraso, principalmente em trabalho remoto "
                      "ou híbrido: registro de ponto, início no sistema ou primeira resposta ao canal de atendimento."))
    itens += [
        ("Indicadores só valem com evidência. ", "Os indicadores de resultado dependem de tarefas concluídas com "
         "evidência no sistema. Enquanto isso não existir, eles são só informativos."),
        ("Dúvidas levadas à direção. ", "Vale acompanhar a quantidade como tendência, sem tirar pontos, para "
         "ninguém deixar de perguntar e errar."),
    ]
    lista(d, itens)


def sec_gratificacao(d, num, cfg, texto_clientes):
    h(d, f"{num}. Ligação com a gratificação de fim de ano")
    par(d, "Um valor de referência por pessoa, definido pela direção, ajustado pela nota do ano (média dos dois "
           "semestres).")
    rotulos = ["Abaixo de 2,5", "De 2,5 a 3,49", "De 3,5 a 4,49", "4,5 ou mais"]
    tabela(d, ["Nota do ano", "Gratificação"],
           [[r, txt] for r, (_, _, txt) in zip(rotulos, m.FAIXAS_GRAT)], [4, 12])
    lista(d, [
        ("Reserva mensal. ", "A direção separa todo mês um valor ou percentual da receita para o fundo de "
         "gratificação. Se a receita crescer, o fundo cresce; se não crescer, a empresa não assume um compromisso que "
         "não cabe no caixa."),
        ("Teto. ", "A soma das gratificações não passa do que foi reservado. Se passar, todas são reduzidas na "
         "mesma proporção."),
        ("Clientes trazidos. ", texto_clientes),
    ])
    h(d, "Pontos para decidir com revisão trabalhista", 2)
    lista(d, [
        "A forma jurídica do pagamento (prêmio por desempenho, PLR ou gratificação) muda encargos e a integração "
        "ao salário. A PLR, por exemplo, exige negociação com comissão de empregados ou sindicato e permite no "
        "máximo dois pagamentos por ano (Lei 10.101/2000).",
        "Pagar por cartão de benefícios, por si só, não afasta a natureza remuneratória.",
        "As regras precisam ser as mesmas para todos, por escrito e entregues antes do início do ciclo.",
        "Estagiários seguem regras próprias (Lei 11.788/2008). Definir se participam.",
    ])


def sec_dados(d, num, cfg, guardiao=""):
    h(d, f"{num}. Confidencialidade e dados pessoais")
    par(d, "Avaliações, faltas e atestados são dados pessoais, e atestados podem conter dados de saúde. Cada "
           "pessoa vê só a própria avaliação. A planilha fica numa pasta com acesso restrito a quem avalia"
           f"{guardiao}. Os atestados não vão para a planilha: ela registra só a quantidade.")


def roteiro(d, arquivo):
    h(d, "Anexo · Roteiro da conversa de avaliação (cerca de 1 hora)", 1)
    lista(d, [
        "Abertura (5 min): objetivo da conversa e como a nota é formada.",
        "Como a pessoa vê o semestre (10 min): o que deu certo, o que foi difícil.",
        "Competência por competência (25 min): comparar autoavaliação e avaliação, com exemplos; fechar a nota.",
        "Indicadores (5 min): números do semestre.",
        "Plano de desenvolvimento (10 min): duas ou três ações, prazo e o apoio da empresa.",
        "Fechamento (5 min): resumo, próximos passos e data do próximo acompanhamento.",
    ], numerada=True)
    par(d, f"A planilha de aplicação ({arquivo}.xlsx) traz uma aba por pessoa, o registro mensal de "
           "assiduidade, o resumo com a gratificação calculada, o plano de desenvolvimento e a biblioteca de "
           "competências técnicas.")


# ---------------------------------------------------------------------------
# Modelo genérico R2 Tech
# ---------------------------------------------------------------------------
def doc_generico(cfg, saida):
    d = novo(cfg, "Avaliação por competências",
             "Modelo R2 Tech Consultoria · avaliação de desempenho e desenvolvimento de equipes",
             "R2 Tech Consultoria · Modelo de avaliação por competências")
    aviso(d, "Modelo para qualquer empresa: escritórios de contabilidade, advocacia, assessoria ou outro ramo. "
             "A estrutura (competências comuns, escala, indicadores, ciclo e gratificação) é a mesma; o que muda "
             "de um cliente para outro são os cargos e as competências técnicas, escolhidas na biblioteca da "
             "seção 7. O modelo não define salário, aumento, contratação ou desligamento.")

    h(d, "1. Para que serve")
    lista(d, [
        ("Avaliar cada pessoa pelo que o cargo dela exige, ", "com a mesma régua de comportamento para todos."),
        ("Dar à equipe clareza sobre o que se espera ", "e onde cada pessoa precisa evoluir."),
        ("Reconhecer desempenho sem aumentar o custo fixo, ", "com uma gratificação anual ligada à nota e a uma "
         "reserva que acompanha a receita."),
        ("Reduzir a dependência da direção, ", "premiando qualidade, prazo e autonomia, e não volume de tarefas."),
    ])

    h(d, "2. Como aplicar a um cliente")
    tabela(d, ["Passo", "O que fazer", "Com quem"], [
        ["1. Levantar cargos", "Listar pessoas, cargos e rotinas reais (entrevistas e processos mapeados).",
         "Direção e equipe"],
        ["2. Escolher competências técnicas", "De 4 a 6 por cargo, a partir da biblioteca (seção 7), ajustando "
         "o texto ao processo do cliente.", "Consultor"],
        ["3. Escolher indicadores", "2 por cargo, que o cliente já consiga medir no sistema que usa.",
         "Consultor e direção"],
        ["4. Validar regras", "Pesos, faixas, valor de referência, reserva mensal, atestados e definição de atraso.",
         "Direção"],
        ["5. Revisão trabalhista", "Forma jurídica da gratificação e texto das regras.", "Advogado ou contador "
         "trabalhista do cliente"],
        ["6. Apresentar à equipe", "Regras por escrito, antes do início do ciclo.", "Direção"],
        ["7. Ciclo piloto", "Uma rodada sem efeito financeiro, para calibrar a régua.", "Direção, com apoio do "
         "consultor"],
        ["8. Ciclos semestrais", "Duas avaliações por ano e gratificação no fim do ano.", "Direção"],
    ], [3.5, 9, 3.5])

    sec_principios(d, 3, cfg)
    sec_estrutura(d, 4)

    h(d, "5. Ciclo de avaliação")
    par(d, "Duas avaliações por ano, como em empresas maiores, e a gratificação apurada no fim do ano.")
    tabela(d, ["Momento", "O que acontece", "Efeito financeiro"], [
        ["Antes do 1º ciclo", "Apresentação das regras à equipe; início do registro de faltas, atrasos e "
         "indicadores", "Nenhum"],
        ["Ciclo piloto (1 a 2 meses)", "Autoavaliação e conversa curta com cada pessoa, para calibrar", "Nenhum"],
        ["1º semestre", "Ciclo com acompanhamento mensal; avaliação no fim do semestre", "Nota guardada"],
        ["2º semestre", "Ciclo com acompanhamento mensal; avaliação no fim do ano; nota do ano = média dos dois",
         "Pagamento da gratificação"],
    ], [4, 9, 3])
    sec_passos(d, cfg)

    sec_comuns(d, 6, cfg)

    h(d, "7. Biblioteca de competências técnicas por área")
    par(d, "Ponto de partida para montar o bloco técnico de cada cargo. Escolha de 4 a 6, reescreva o \"atender\" "
           "com o processo real do cliente e use a evidência como base dos indicadores. Cargos que acumulam áreas "
           "combinam competências de mais de uma área.")
    for area, itens in m.BIBLIOTECA.items():
        h(d, area, 2)
        tabela(d, ["Competência", "O que é atender (nota 3)", "Evidência / indicador"],
               [list(x) for x in itens], [4, 8, 4])
    h(d, "Trilha de liderança (opcional, fora da nota)", 2)
    par(d, "Para quem se prepara para supervisionar a equipe. É avaliada na mesma escala, mas não entra na nota "
           "nem na gratificação: mostra o que se espera e onde a pessoa está.")
    tabela(d, ["", "Competência", "O que se espera"], [list(x) for x in m.LIDERANCA], [1, 3.5, 11.5])

    sec_indicadores(d, 8, cfg)
    sec_gratificacao(d, 9, cfg, "Em vez de um bônus mensal por cliente, a indicação de clientes entra como "
                     "exemplo na competência C3 (Proatividade) ou numa competência técnica comercial. Se o cliente "
                     "preferir um prêmio por indicação, sugerimos valor fixo por cliente que fechar e continuar "
                     "ativo após três meses.")
    sec_dados(d, 10, cfg)

    h(d, "11. Decisões que cada cliente precisa tomar")
    tabela(d, ["#", "Decisão", "Sugestão do modelo"], [
        ["1", "Periodicidade da avaliação e do pagamento", "Avaliação semestral, pagamento anual"],
        ["2", "Pesos dos blocos", "40% comportamentais, 40% técnicas e 20% indicadores"],
        ["3", "Valor de referência da gratificação por pessoa", "Definido pela direção"],
        ["4", "Valor ou percentual da reserva mensal", "Definido pela direção, conforme o caixa"],
        ["5", "Prêmio separado por cliente indicado?", "Não; incluir na avaliação"],
        ["6", "Atestados entram na nota?", "Não; só registro"],
        ["7", "Como medir atraso", "Definir conforme o regime de trabalho"],
        ["8", "Estagiários participam da gratificação?", "Decisão da direção, com revisão jurídica"],
        ["9", "Fazer ciclo piloto?", "Sim, sem efeito financeiro"],
    ], [1, 10, 5])

    roteiro(d, cfg["arquivo"])
    par(d, "Referências de formato: guias de desenvolvimento de competências de mercado (competência, definição, "
           "comportamentos por nível e plano de desenvolvimento). Nenhum texto de terceiros foi copiado.",
        italico=True)
    par(d, CONSULTOR, italico=True)
    os.makedirs(saida, exist_ok=True)
    caminho = os.path.join(saida, cfg["arquivo"] + ".docx")
    d.save(caminho)
    return caminho


# ---------------------------------------------------------------------------
# Aplicação à Surcin
# ---------------------------------------------------------------------------
def doc_surcin(cfg, saida):
    d = novo(cfg, "Avaliação por competências",
             "Surcin Assessoria Empresarial · modelo de avaliação de desempenho e desenvolvimento da equipe",
             "Surcin Assessoria Empresarial · Avaliação por competências · Confidencial")

    aviso(d, "Este material aplica à Surcin o modelo de avaliação por competências da R2 Tech Consultoria e é uma "
             "proposta para a Thamires validar. Ele organiza o que ela pediu na reunião de 12/10/2026 e no "
             "briefing, mais a sugestão do Renato de 13/10/2026. Não define salário, aumento, contratação ou "
             "desligamento. Pesos, faixas e valores são sugestões ajustáveis, e a forma de pagamento da "
             "gratificação precisa de revisão trabalhista antes de ser anunciada à equipe.")

    h(d, "1. Por que avaliar e o que a Thamires pediu")
    lista(d, [
        ("Avaliar cada pessoa pelo que ela faz. ", "\"Eu preciso fazer essa avaliação de forma individual, porque cada "
         "um faz uma coisa\", e dar à equipe a sensação de \"eu tô sendo vista\" (reunião 01:58)."),
        ("Reconhecer quem absorveu mais trabalho sem dar aumento. ", "Ela não deu aumento e prometeu um programa de "
         "bonificação para produzir mais e errar menos (00:46). Quer remunerar o ganho de eficiência \"sem sair "
         "aumentando\" o salário (00:47)."),
        ("Pontos sobre um salário base. ", "\"Eu tenho um salário base, mas eu tenho pontos\" (02:21)."),
        ("Mostrar onde cada uma precisa evoluir. ", "Na conversa sobre a Júlia, o Renato sugeriu colocar no papel o "
         "que é um líder para a Surcin, onde ela está e o que precisa desenvolver (02:26 a 02:27)."),
        ("Critérios do briefing (seção 10). ", "Reconhecer qualidade, pontualidade, proatividade, autonomia, "
         "escrita/atendimento, conformidade com procedimentos e evolução profissional; metas por função; não "
         "premiar volume bruto de cartões; dados do Trello e dos sistemas com revisão humana; valores e natureza "
         "jurídica com revisão trabalhista."),
        ("Sugestão do Renato (WhatsApp, 13/10). ", "Avaliação semestral (duas por ano), com faltas, atrasos e "
         "atestados, e uma gratificação no fim do ano, em vez de uma gratificação por cliente trazido. Assim a "
         "Thamires reserva o valor mês a mês conforme a receita entra."),
    ])

    sec_principios(d, 2, cfg)
    sec_estrutura(d, 3)

    h(d, "4. Ciclo de avaliação")
    par(d, "Duas avaliações por ano, como em empresas maiores, e a gratificação apurada no fim do ano.")
    tabela(d, ["Período", "O que acontece", "Efeito financeiro"], [
        ["Novembro de 2026", "Thamires apresenta o modelo e as regras à equipe; começa o registro de faltas, "
         "atrasos e indicadores", "Nenhum"],
        ["Dezembro de 2026, após a prova de 13/12", "Ciclo piloto: autoavaliação e conversa curta com cada uma, "
         "para calibrar a régua", "Nenhum"],
        ["Janeiro a junho de 2027", "1º ciclo; acompanhamento mensal de 30 minutos", "Conta para a gratificação"],
        ["Julho de 2027", "Avaliação do 1º semestre e plano de desenvolvimento", "Nota guardada"],
        ["Julho a dezembro de 2027", "2º ciclo; acompanhamento mensal", "Conta para a gratificação"],
        ["Dezembro de 2027", "Avaliação do 2º semestre; nota do ano = média dos dois semestres; "
         "pagamento da gratificação", "Pagamento"],
    ], [4, 9, 3])
    sec_passos(d, cfg)
    par(d, "Na reunião, o Renato sugeriu um acompanhamento semanal com a Júlia (02:25). Ele pode substituir o "
           "acompanhamento mensal no caso dela.")

    sec_comuns(d, 5, cfg)

    h(d, "6. Competências técnicas por função")
    par(d, "Rascunho a partir das rotinas que a Thamires descreveu, com base na biblioteca do modelo R2 Tech. A "
           "lista final sai do mapeamento de processos e das entrevistas com a equipe (Etapas 1 e 2 da proposta) e "
           "conversa com os papéis do documento 02.")
    for nome, f in cfg["pessoas"].items():
        h(d, f"{nome} · {f['cargo']}", 2)
        tabela(d, ["", "Competência", "O que é atender (nota 3)", "Evidência"],
               [[c, n, a, e] for c, n, a, e in f["tecnicas"]], [1, 3.5, 7.5, 4])
        if f.get("obs"):
            par(d, f["obs"], italico=True)
        par(d, f"Base: {f['fonte']}.", italico=True)
    h(d, "Trilha de supervisão da Júlia (desenvolvimento, fora da nota)", 2)
    par(d, "A Thamires disse que a supervisão seria para 2027, condicionada à faculdade e de forma gradual "
           "(02:25). Esta trilha mostra à Júlia o que se espera de uma supervisora e onde ela está. Ela é avaliada "
           "na mesma escala, mas não entra na nota nem na gratificação. A competência L4 (Eficácia) vem de uma fala "
           "da Thamires: \"quanto do seu trabalho você é efetivo\" (02:25).")
    tabela(d, ["", "Competência", "O que se espera"], [list(x) for x in m.LIDERANCA], [1, 3.5, 11.5])

    sec_indicadores(d, 7, cfg, remoto=True)
    sec_gratificacao(d, 8, cfg, "Em vez de um bônus mensal por cliente, a indicação de clientes entra como exemplo "
                     "na competência C3 (Proatividade) e, para a Júlia, na T4 (Propostas e contratos). Se a Thamires "
                     "preferir manter um prêmio por indicação, sugerimos valor fixo por cliente que fechar e continuar "
                     "ativo após três meses.")
    sec_dados(d, 9, cfg, guardiao=" (papel de guardião de dados, documento 02, seção 4)")

    h(d, "10. Decisões da Thamires")
    tabela(d, ["#", "Decisão", "Sugestão"], [
        ["1", "Periodicidade: avaliação semestral com gratificação anual, ou pagamento mensal como ela citou "
              "na reunião (02:21)?", "Semestral, com pagamento anual"],
        ["2", "Pesos dos blocos", "40% comportamentais, 40% técnicas e 20% indicadores"],
        ["3", "Valor de referência da gratificação por pessoa", "Definido por ela"],
        ["4", "Valor ou percentual da reserva mensal", "Definido por ela, conforme o caixa"],
        ["5", "Prêmio separado por cliente indicado?", "Não; incluir na avaliação"],
        ["6", "Atestados entram na nota?", "Não; só registro"],
        ["7", "Como medir atraso no trabalho remoto?", "A definir com ela"],
        ["8", "A Alana participa da gratificação?", "Decisão dela, com revisão jurídica"],
        ["9", "Fazer o ciclo piloto em dezembro de 2026?", "Sim, sem efeito financeiro"],
    ], [1, 10, 5])

    roteiro(d, cfg["arquivo"])
    par(d, "Base: transcrição da reunião de 12/10/2026 (minutos entre parênteses), briefing enviado pela Surcin "
           "(seções 2, 5 e 10), documentos 01 e 02 da proposta e conversa do Renato com a Thamires no WhatsApp em "
           "13/10/2026. Referências de formato: guias de desenvolvimento de competências de mercado; nenhum texto "
           "de terceiros foi copiado.", italico=True)
    par(d, CONSULTOR, italico=True)
    os.makedirs(saida, exist_ok=True)
    caminho = os.path.join(saida, cfg["arquivo"] + ".docx")
    d.save(caminho)
    return caminho
