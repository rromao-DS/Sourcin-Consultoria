# -*- coding: utf-8 -*-
"""Conteúdo do modelo de avaliação por competências da Surcin (proposta para validação, 13/10/2026).

Usado pelos geradores do Word e do Excel, para que os dois tragam exatamente as mesmas competências.
"""

VERSAO = "Versão 1 · 13/10/2026 · proposta para validação da Thamires · uso interno até revisão do Renato"

ESCALA = [
    (1, "Não atende", "O comportamento esperado raramente aparece; precisa de acompanhamento constante."),
    (2, "Atende em parte", "Aparece às vezes ou só com orientação frequente."),
    (3, "Atende", "Faz de forma consistente o que se espera da função. É a nota de quem está bem no cargo."),
    (4, "Supera", "Vai além do esperado com frequência e é referência nas situações do dia a dia."),
    (5, "Referência", "Supera de forma consistente, ensina outras pessoas e melhora o processo."),
]

# Pesos dos blocos na nota final (sugestão; editáveis na planilha)
PESOS = [
    ("Competências comportamentais (comuns a todas)", 0.40),
    ("Competências técnicas da função", 0.40),
    ("Indicadores objetivos", 0.20),
]

# (código, nome, definição, nível 1, nível 3, nível 5, origem)
COMUNS = [
    ("C1", "Qualidade e conformidade com procedimentos",
     "Executa conforme o passo a passo e o checklist, confere antes de entregar e registra a evidência.",
     "Entrega sem conferir, pula etapas do checklist, conclui cartão sem o documento.",
     "Segue o procedimento, confere e anexa a evidência; erros são raros e corrigidos assim que apontados.",
     "Encontra o erro antes que chegue ao cliente e propõe ajustes no procedimento.",
     "Briefing, seção 10"),
    ("C2", "Cumprimento de prazos",
     "Entrega no prazo combinado e avisa com antecedência quando há risco de atraso.",
     "Perde prazos ou entrega em cima da hora sem avisar.",
     "Cumpre os prazos da rotina e avisa antes quando algo vai atrasar.",
     "Organiza a semana pelos vencimentos, antecipa entregas críticas e ajuda a destravar prazos dos colegas.",
     "Briefing, seção 10 (pontualidade)"),
    ("C3", "Proatividade",
     "Identifica pendências e age sem precisar ser cobrada.",
     "Espera ser lembrada para agir.",
     "Percebe as pendências da própria rotina e resolve sem cobrança.",
     "Antecipa problemas de clientes e da empresa e chega com a solução junto com o problema.",
     "Briefing, seção 10"),
    ("C4", "Autonomia",
     "Consulta o procedimento e a base de conhecimento antes de escalar; quando escala, leva o caso já levantado.",
     "Leva toda dúvida à Thamires sem consultar o material disponível.",
     "Resolve as dúvidas comuns com os passo a passos e escala só exceções, com as informações reunidas.",
     "Resolve situações novas com bom critério e registra a solução para a equipe.",
     "Briefing, seção 10; reunião 00:18 (\"tudo tá centralizado em mim\")"),
    ("C5", "Comunicação escrita e atendimento",
     "Escreve de forma clara e cordial, retorna o cliente no prazo e registra o que foi combinado.",
     "Mensagens incompletas ou confusas; cliente fica sem retorno.",
     "Mensagens claras e cordiais, retorno no prazo, combinados registrados.",
     "Antecipa as dúvidas do cliente e cria modelos de mensagem que a equipe passa a usar.",
     "Briefing, seção 10 (escrita/atendimento)"),
    ("C6", "Comprometimento",
     "Assume a responsabilidade pelas próprias entregas e cumpre o que combinou.",
     "Deixa pendência crítica sem combinar o repasse; não reconhece os próprios erros.",
     "Assume as entregas, cumpre combinados, reconhece e corrige os erros.",
     "Age como dona do resultado do processo e se oferece para cobrir quando falta alguém, dentro da jornada combinada.",
     "Reunião 01:58 (\"perfil e comprometimento\")"),
    ("C7", "Colaboração",
     "Apoia colegas, compartilha o que sabe e cobre ausências quando combinado.",
     "Trabalha isolada; o que sabe fica só com ela.",
     "Ajuda quando solicitada e repassa informações completas nas trocas e coberturas.",
     "Ensina, documenta e organiza coberturas sem precisar de intervenção da Thamires.",
     "Sugestão do consultor (redistribuição das funções da Dani, reunião 02:24)"),
    ("C8", "Evolução profissional",
     "Aplica o feedback recebido e cumpre as ações do plano de desenvolvimento.",
     "Repete os mesmos erros e não busca aprender.",
     "Aplica o feedback e cumpre as ações combinadas no plano de desenvolvimento.",
     "Busca aprender por conta própria, aplica e ensina o que aprendeu.",
     "Briefing, seção 10; reunião 01:58 (\"conhecimento a gente desenvolve\")"),
]

# Competências técnicas: por pessoa, (código, nome, o que é "atender" (nota 3), indicador/evidência)
FUNCOES = {
    "Júlia": {
        "cargo": "Secretaria, atendimento e entrada de clientes",
        "fonte": "Reunião 00:15 a 00:19, 01:04; briefing seções 5 e 10; doc 02",
        "tecnicas": [
            ("T1", "Triagem e distribuição das demandas",
             "Toda demanda que chega por WhatsApp/Nestzap ou Veri é registrada no Trello e distribuída no mesmo dia; nada fica perdido em grupos.",
             "Demandas distribuídas no dia"),
            ("T2", "Agenda e documentos",
             "Agenda da operação em dia; documentos salvos na pasta certa do OneDrive, no padrão de nome combinado.",
             "Documentos no lugar certo na conferência por amostra"),
            ("T3", "Implantação de novos clientes",
             "Checklist de novo cliente cumprido por completo (pasta, grupo, dados, cadastro), sem pendência aberta.",
             "Tempo de implantação; checklists completos"),
            ("T4", "Propostas e contratos",
             "Propostas e contratos feitos a partir dos modelos, com dados conferidos e dentro do prazo combinado com o cliente.",
             "Propostas enviadas no prazo; contratos sem retrabalho"),
            ("T5", "Apoio ao fiscal",
             "Guias enviadas a todos os clientes com registro na rotina, conferindo se a guia é do cliente certo.",
             "Envios registrados; nenhuma guia trocada"),
        ],
        "indicadores": [
            ("Demandas distribuídas no mesmo dia (%)", "Trello"),
            ("Implantações concluídas com checklist completo (%)", "Trello"),
        ],
    },
    "Vitória": {
        "cargo": "Financeiro",
        "fonte": "Reunião 00:13, 00:38, 01:34; briefing seções 5 e 10; doc 02",
        "tecnicas": [
            ("T1", "Pagamentos dos clientes",
             "Pagamentos feitos nos dias da rotina, com a guia conferida antes (cliente, valor e vencimento).",
             "Pagamentos sem atraso e sem guia trocada"),
            ("T2", "Conciliação semanal",
             "Conciliação no Conta Azul em dia, toda semana; clientes conciliados até o dia 1º.",
             "Clientes conciliados até o dia 1º"),
            ("T3", "Emissão de notas fiscais",
             "Notas emitidas no prazo e com os dados corretos.",
             "Notas canceladas ou corrigidas no mês"),
            ("T4", "Preparação do fechamento",
             "Material do fechamento pronto para a reunião de resultado na primeira semana do mês.",
             "Fechamentos entregues na 1ª semana"),
            ("T5", "Análise e revisão",
             "Identifica lançamentos e classificações inconsistentes e sinaliza antes do fechamento.",
             "Inconsistências apontadas antes da reunião"),
        ],
        "indicadores": [
            ("Clientes conciliados até o dia 1º (%)", "Conta Azul / Trello"),
            ("Fechamentos entregues na 1ª semana (%)", "Trello"),
        ],
    },
    "Tamara": {
        "cargo": "Departamento Pessoal",
        "fonte": "Reunião 00:41, 02:05; briefing seções 5 e 10; doc 02",
        "tecnicas": [
            ("T1", "Folha mensal",
             "Folhas fechadas e enviadas até o 5º dia útil.",
             "Folhas no prazo"),
            ("T2", "Admissões e rescisões",
             "Documentos completos e prazos legais cumpridos em cada admissão e rescisão.",
             "Processos sem pendência ou multa"),
            ("T3", "eSocial e obrigações trabalhistas",
             "Eventos e obrigações transmitidos em dia, sem pendência no sistema.",
             "Pendências no eSocial"),
            ("T4", "Regularização de pendências antigas",
             "Plano de pendências antigas seguido até zerar.",
             "Pendências antigas em aberto"),
            ("T5", "Atendimento aos clientes de DP",
             "Dúvidas dos clientes sobre funcionários respondidas no prazo combinado, com registro.",
             "Dúvidas respondidas no prazo"),
        ],
        "indicadores": [
            ("Folhas entregues até o 5º dia útil (%)", "Domínio / Trello"),
            ("Pendências antigas resolvidas no semestre (%)", "Controle de pendências"),
        ],
        "obs": "Se ela continuar emitindo notas a partir de novembro (divergência entre reunião e briefing), "
               "incluir a competência \"Emissão de notas fiscais\" igual à da Vitória.",
    },
    "Alana": {
        "cargo": "Estágio no jurídico e no societário (dois dias por semana)",
        "fonte": "Reunião 00:42, 01:40, 02:18; briefing seções 5 e 10; doc 02",
        "tecnicas": [
            ("T1", "Acompanhamento de processos e prazos",
             "Andamentos dos processos legados acompanhados e nenhum prazo perdido.",
             "Prazos cumpridos"),
            ("T2", "Peças e documentos simples",
             "Peças e documentos feitos a partir dos modelos, com cada vez menos correção da Thamires.",
             "Quantidade de correções por peça"),
            ("T3", "Apoio ao societário",
             "Abertura, alteração e baixa de empresas seguindo o checklist do Trello.",
             "Etapas do checklist cumpridas"),
            ("T4", "Organização e registro",
             "Pastas e andamentos atualizados, para qualquer pessoa achar a informação.",
             "Conferência por amostra"),
            ("T5", "Aprendizado técnico",
             "Aplica no trabalho o que aprende e precisa de menos revisão a cada ciclo.",
             "Evolução das correções entre ciclos"),
        ],
        "indicadores": [
            ("Prazos processuais cumpridos (%)", "Jusbrasil / controle de prazos"),
            ("Peças entregues sem correção relevante (%)", "Revisão da Thamires"),
        ],
        "obs": "Metas proporcionais à jornada de estágio, como pede o briefing (seção 10). O estágio segue a Lei "
               "11.788/2008; a elegibilidade dela à gratificação é decisão da Thamires, com revisão jurídica.",
    },
}

# Trilha de supervisão (só Júlia; desenvolvimento, não entra na nota)
LIDERANCA = [
    ("L1", "Priorização", "Organiza as demandas da equipe por prazo e impacto e deixa claro o que vem primeiro."),
    ("L2", "Delegar e acompanhar", "Distribui tarefas com instrução clara e acompanha até a entrega, sem fazer pela pessoa."),
    ("L3", "Feedback", "Dá retorno direto e respeitoso às colegas e recebe críticas sem se defender."),
    ("L4", "Eficácia", "Mede o próprio trabalho pelo resultado entregue, não pelo volume de tarefas (reunião 02:25)."),
    ("L5", "Postura de referência", "Representa os combinados da empresa diante da equipe e dos clientes."),
]

# Indicadores objetivos comuns
ASSIDUIDADE = [
    ("Faltas injustificadas no semestre", [(0, 5), (1, 4), (2, 3), (3, 2), (4, 1)],
     "0 = 5 · 1 = 4 · 2 = 3 · 3 = 2 · 4 ou mais = 1"),
    ("Atrasos no semestre", [(0, 5), (3, 4), (6, 3), (9, 2), (13, 1)],
     "0 a 2 = 5 · 3 a 5 = 4 · 6 a 8 = 3 · 9 a 12 = 2 · 13 ou mais = 1"),
]
# % de cumprimento dos indicadores da função -> nota
FAIXAS_PCT = [(0, 1), (0.80, 2), (0.90, 3), (0.95, 4), (0.98, 5)]
FAIXAS_PCT_TXT = "abaixo de 80% = 1 · 80% a 89% = 2 · 90% a 94% = 3 · 95% a 97% = 4 · 98% ou mais = 5"

# Nota final -> percentual da gratificação de referência
FAIXAS_GRAT = [(0, 0.0, "Abaixo do esperado: sem gratificação, com plano de desenvolvimento"),
               (2.5, 0.5, "Em desenvolvimento: 50% da referência"),
               (3.5, 1.0, "Atende: 100% da referência"),
               (4.5, 1.2, "Destaque: 120% da referência")]
