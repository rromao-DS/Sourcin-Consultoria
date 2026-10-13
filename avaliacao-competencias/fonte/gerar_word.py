# -*- coding: utf-8 -*-
"""Gera o documento Word do modelo de avaliação por competências da Surcin."""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "proposta-surcin", "fonte"))
import gerar_docs as gd  # noqa: E402  (reaproveita o padrão visual da proposta)
from gerar_docs import h, par, lista, tabela, aviso  # noqa: E402
import modelo as m  # noqa: E402

SAIDA = sys.argv[1] if len(sys.argv) > 1 else "."


def documento():
    gd.VERSAO = m.VERSAO
    d = gd.novo_doc("Avaliação por competências",
                    "Surcin Assessoria Empresarial · modelo de avaliação de desempenho e desenvolvimento da equipe")
    rodape = d.sections[0].footer.paragraphs[0]
    rodape.runs[0].text = "Surcin Assessoria Empresarial · Avaliação por competências · Confidencial"

    aviso(d, "Este material é uma proposta para a Thamires validar. Ele organiza o que ela pediu na reunião de "
             "12/10/2026 e no briefing, mais a sugestão do Renato de 13/10/2026. Não define salário, aumento, "
             "contratação ou desligamento. Pesos, faixas e valores são sugestões ajustáveis, e a forma de pagamento "
             "da gratificação precisa de revisão trabalhista antes de ser anunciada à equipe.")

    # 1
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

    # 2
    h(d, "2. Princípios do modelo")
    lista(d, [
        ("Avalia o profissional, não a pessoa. ", "Cada nota se apoia em fatos e exemplos do período."),
        ("Qualidade antes de volume. ", "Cartão concluído sem evidência não conta como entrega."),
        ("Dado objetivo mais conversa. ", "Indicadores do Trello e dos sistemas entram na nota; o restante é "
         "avaliado pela Thamires, depois da autoavaliação de cada uma."),
        ("A régua é a função. ", "Competências comportamentais iguais para todas; competências técnicas próprias "
         "de cada cargo."),
        ("Serve para desenvolver. ", "Toda avaliação termina com um plano de desenvolvimento curto, com duas ou três "
         "ações."),
        ("Regras por escrito e iguais para todas. ", "As regras são entregues à equipe antes do início do ciclo."),
    ])

    # 3
    h(d, "3. Estrutura da nota")
    par(d, "A nota final vai de 1 a 5 e é a média ponderada de três blocos:")
    tabela(d, ["Bloco", "O que entra", "Peso sugerido"], [
        [m.PESOS[0][0], "8 competências, as mesmas para toda a equipe (seção 5)", "40%"],
        [m.PESOS[1][0], "5 competências do cargo de cada pessoa (seção 6)", "40%"],
        [m.PESOS[2][0], "Faltas injustificadas, atrasos e 2 indicadores de resultado da função (seção 7)", "20%"],
    ], [5.5, 8, 2.5])

    h(d, "Escala de 1 a 5", 2)
    tabela(d, ["Nota", "Nível", "Significado"], [[str(n), nv, s] for n, nv, s in m.ESCALA], [1.5, 3, 11.5])
    par(d, "A nota 3 é a de quem está bem no cargo. Notas 4 e 5 pedem exemplos concretos do período, e notas 1 e "
           "2 pedem exemplos e uma ação no plano de desenvolvimento.", italico=True)

    # 4
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
    h(d, "Passos de cada avaliação", 2)
    lista(d, [
        "Cada funcionária preenche a autoavaliação na planilha, com exemplos.",
        "A Thamires preenche a avaliação dela e lança os indicadores do semestre.",
        "Conversa individual de cerca de 1 hora: comparar as duas visões e fechar a nota final.",
        "Plano de desenvolvimento com duas ou três ações, prazo e apoio da empresa.",
        "Acompanhamento mensal curto (30 minutos) para ver o plano e os indicadores.",
    ], numerada=True)
    par(d, "Na reunião, o Renato sugeriu um acompanhamento semanal com a Júlia (02:25). Ele pode substituir o "
           "acompanhamento mensal no caso dela.")

    # 5
    h(d, "5. Competências comportamentais (comuns)")
    par(d, "Descrição dos níveis 1, 3 e 5. As notas 2 e 4 ficam entre eles.")
    for cod, nome, defin, n1, n3, n5, origem in m.COMUNS:
        h(d, f"{cod} · {nome}", 3)
        par(d, defin)
        tabela(d, ["Nível 1", "Nível 3", "Nível 5"], [[n1, n3, n5]], [5.3, 5.3, 5.4])
        par(d, f"Origem: {origem}.", italico=True)

    # 6
    h(d, "6. Competências técnicas por função")
    par(d, "Rascunho a partir das rotinas que a Thamires descreveu. A lista final sai do mapeamento de processos "
           "e das entrevistas com a equipe (Etapas 1 e 2 da proposta) e conversa com os papéis do documento 02.")
    for nome, f in m.FUNCOES.items():
        h(d, f"{nome} · {f['cargo']}", 2)
        tabela(d, ["", "Competência", "O que é atender (nota 3)", "Evidência"],
               [[c, n, a, e] for c, n, a, e in f["tecnicas"]], [1, 3.5, 7.5, 4])
        if f.get("obs"):
            par(d, f["obs"], italico=True)
        par(d, f"Base: {f['fonte']}.", italico=True)

    h(d, "Trilha de supervisão da Júlia (desenvolvimento, fora da nota)", 2)
    par(d, "A Thamires disse que a supervisão seria para 2027, condicionada à faculdade e de forma gradual "
           "(02:25). Esta trilha mostra à Júlia o que se espera de uma supervisora e onde ela está. Ela é avaliada "
           "na mesma escala, mas não entra na nota nem na gratificação.")
    tabela(d, ["", "Competência", "O que se espera"], [list(x) for x in m.LIDERANCA], [1, 3.5, 11.5])

    # 7
    h(d, "7. Indicadores objetivos")
    tabela(d, ["Indicador", "Como vira nota", "Fonte"], [
        [m.ASSIDUIDADE[0][0], m.ASSIDUIDADE[0][2], "Controle de ponto ou registro da Thamires"],
        [m.ASSIDUIDADE[1][0], m.ASSIDUIDADE[1][2], "Controle de ponto ou registro da Thamires"],
        ["Atestados e faltas justificadas", "Só registro. Não reduz a nota", "Registro de DP"],
        ["2 indicadores de resultado da função", m.FAIXAS_PCT_TXT, "Trello e sistemas (seção 6)"],
    ], [4.5, 7.5, 4])
    aviso(d, "Atestados: a sugestão inicial incluía atestados na avaliação. Recomendamos registrar, mas não "
             "descontar pontos por falta justificada ou atestado médico. Penalizar ausência legalmente justificada "
             "cria risco trabalhista e de discriminação. A decisão final é da Thamires, com revisão trabalhista.")
    lista(d, [
        ("Atraso em trabalho remoto. ", "A Surcin atua de forma remota (briefing, seção 2). É preciso definir o que "
         "conta como atraso: registro de ponto, início no sistema ou primeira resposta no WhatsApp."),
        ("Indicadores só valem com evidência. ", "Os indicadores de resultado dependem da regra de concluir cartão "
         "com evidência (controle proposto na Fase 1). No ciclo piloto eles são só informativos."),
        ("Dúvidas levadas à Thamires. ", "O briefing pede um indicador de dependência. Sugerimos acompanhar a "
         "tendência sem tirar pontos, para ninguém deixar de perguntar e errar."),
    ])

    # 8
    h(d, "8. Ligação com a gratificação de fim de ano")
    par(d, "Proposta: um valor de referência por pessoa, definido pela Thamires, ajustado pela nota do ano.")
    rotulos = ["Abaixo de 2,5", "De 2,5 a 3,49", "De 3,5 a 4,49", "4,5 ou mais"]
    tabela(d, ["Nota do ano", "Gratificação"],
           [[r, txt] for r, (_, _, txt) in zip(rotulos, m.FAIXAS_GRAT)], [4, 12])
    lista(d, [
        ("Reserva mensal. ", "A Thamires separa todo mês um valor ou percentual da receita para o fundo de "
         "gratificação. Se a receita crescer, o fundo cresce; se não crescer, ela não assume um compromisso que "
         "não cabe no caixa."),
        ("Teto. ", "A soma das gratificações não passa do que foi reservado. Se passar, todas são reduzidas na "
         "mesma proporção."),
        ("Clientes trazidos. ", "Em vez de um bônus mensal por cliente, a indicação de clientes entra como "
         "exemplo na competência C3 (Proatividade) e, para a Júlia, na T4 (Propostas e contratos). Se a Thamires "
         "preferir manter um prêmio por indicação, sugerimos valor fixo por cliente que fechar e continuar ativo "
         "após três meses."),
    ])
    h(d, "Pontos para decidir com revisão trabalhista", 2)
    lista(d, [
        "A forma jurídica do pagamento (prêmio por desempenho, PLR ou gratificação) muda encargos e a integração "
        "ao salário. A PLR, por exemplo, exige negociação com comissão de empregados ou sindicato e permite no "
        "máximo dois pagamentos por ano (Lei 10.101/2000).",
        "O briefing já registra que pagar por cartão de benefícios não afasta a natureza remuneratória.",
        "As regras precisam ser as mesmas para todas, por escrito e entregues antes do início do ciclo.",
        "Estagiária: o estágio tem regras próprias (Lei 11.788/2008). Definir se a Alana participa.",
    ])

    # 9
    h(d, "9. Confidencialidade e dados pessoais")
    par(d, "Avaliações, faltas e atestados são dados pessoais, e atestados podem conter dados de saúde. Cada "
           "funcionária vê só a própria avaliação. A planilha fica numa pasta do OneDrive com acesso restrito à "
           "Thamires (papel de guardião de dados, documento 02, seção 4). Os atestados não vão para a planilha: "
           "ela registra só a quantidade.")

    # 10
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

    h(d, "Anexo · Roteiro da conversa de avaliação (cerca de 1 hora)", 1)
    lista(d, [
        "Abertura (5 min): objetivo da conversa e como a nota é formada.",
        "Como ela vê o semestre (10 min): o que deu certo, o que foi difícil.",
        "Competência por competência (25 min): comparar autoavaliação e avaliação, com exemplos; fechar a nota.",
        "Indicadores (5 min): números do semestre.",
        "Plano de desenvolvimento (10 min): duas ou três ações, prazo e o apoio da empresa.",
        "Fechamento (5 min): resumo, próximos passos e data do próximo acompanhamento.",
    ], numerada=True)
    par(d, "A planilha de aplicação (avaliacao-competencias-surcin.xlsx) traz uma aba por funcionária, o "
           "registro mensal de assiduidade, o resumo com a gratificação calculada e o plano de desenvolvimento.")

    par(d, "Base: transcrição da reunião de 12/10/2026 (minutos entre parênteses), briefing enviado pela Surcin "
           "(seções 2, 5 e 10), documentos 01 e 02 da proposta e conversa do Renato com a Thamires no WhatsApp em "
           "13/10/2026. Os materiais de referência da pasta do Drive (guia de competências da Korn Ferry e "
           "materiais de liderança da Apple) serviram só de referência de formato, com competência, definição, "
           "comportamentos observáveis por nível e plano de desenvolvimento; nenhum texto deles foi copiado.",
        italico=True)
    par(d, gd.CONSULTOR, italico=True)

    os.makedirs(SAIDA, exist_ok=True)
    d.save(os.path.join(SAIDA, "avaliacao-competencias-surcin.docx"))


if __name__ == "__main__":
    documento()
    print("ok")
