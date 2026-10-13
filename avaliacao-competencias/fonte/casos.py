# -*- coding: utf-8 -*-
"""Casos de aplicação do modelo de avaliação por competências da R2 Tech Consultoria.

GENERICO é o modelo em branco para qualquer empresa; SURCIN é o primeiro caso preenchido.
Para um cliente novo, copie GENERICO, troque empresa, gestor e cargos e escolha as
competências técnicas na BIBLIOTECA de base.py.
"""

# Competências técnicas: por pessoa, (código, nome, o que é "atender" (nota 3), indicador/evidência)
PESSOAS_SURCIN = {
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


ORIGENS_SURCIN = {'C1': 'Briefing, seção 10',
 'C2': 'Briefing, seção 10 (pontualidade)',
 'C3': 'Briefing, seção 10',
 'C4': 'Briefing, seção 10; reunião 00:18 ("tudo tá centralizado em mim")',
 'C5': 'Briefing, seção 10 (escrita/atendimento)',
 'C6': 'Reunião 01:58 ("perfil e comprometimento")',
 'C7': 'Sugestão do consultor (redistribuição das funções da Dani, reunião 02:24)',
 'C8': 'Briefing, seção 10; reunião 01:58 ("conhecimento a gente desenvolve")'}

SURCIN = {
    "arquivo": "avaliacao-competencias-surcin",
    "empresa": "Surcin Assessoria Empresarial",
    "gestor": "Thamires",
    "ao_gestor": "à Thamires",
    "do_gestor": "da Thamires",
    "versao": "Versão 2 · 13/10/2026 · aplicação do modelo R2 Tech · proposta para validação da Thamires",
    "ciclo": "1º semestre de 2027",
    "pessoas": PESSOAS_SURCIN,
    "lideranca": ["Júlia"],
    "participa": {"Alana": "A definir"},
    "origens": ORIGENS_SURCIN,
}

GENERICO = {
    "arquivo": "modelo-avaliacao-competencias-r2tech",
    "empresa": "[Nome da empresa]",
    "gestor": "gestor(a)",
    "ao_gestor": "ao(à) gestor(a)",
    "do_gestor": "do(a) gestor(a)",
    "versao": "Modelo R2 Tech Consultoria · versão 1 · 13/10/2026",
    "ciclo": "[1º semestre de AAAA]",
    "pessoas": {f"Pessoa {i}": {"cargo": "[Cargo]", "tecnicas": None, "indicadores": None} for i in range(1, 7)},
    "lideranca": [f"Pessoa {i}" for i in range(1, 7)],
    "participa": {},
    "origens": {},
}

# Organograma atual da Surcin (documento 02, seção 1, a partir da reunião de 12/10/2026).
# Só o que as fontes dizem: sem datas de admissão, e-mails ou tipo de vínculo não informado.
ORGANOGRAMA_SURCIN = {
    "areas": ["Direção", "Secretaria e atendimento", "Financeiro", "Departamento Pessoal", "Jurídico e societário"],
    "cargos": {
        # cargo: (área, missão ou responsabilidades citadas)
        "Direção": ("Direção", "Direção, técnica contábil e jurídica, fiscal, comercial, reuniões de fechamento"),
        "Secretaria, atendimento e entrada de clientes": ("Secretaria e atendimento",
            "Atendimento, implantação de clientes, apoio no fiscal"),
        "Financeiro": ("Financeiro", "Pagamentos, notas, conciliação, preparação do fechamento"),
        "Departamento Pessoal": ("Departamento Pessoal", "DP; até outubro de 2026 também apoio no financeiro e notas"),
        "Estágio no jurídico e no societário (dois dias por semana)": ("Jurídico e societário",
            "Acompanhamento de processos, peças simples, apoio ao societário"),
    },
    # pessoa: (cargo, gestor, tipo de vínculo, jornada)
    "pessoas": {
        "Thamires": ("Direção", None, "socio", None),
        "Júlia": ("Secretaria, atendimento e entrada de clientes", "Thamires", "nao_informado", None),
        "Vitória": ("Financeiro", "Thamires", "nao_informado", None),
        "Tamara": ("Departamento Pessoal", "Thamires", "nao_informado", None),
        "Alana": ("Estágio no jurídico e no societário (dois dias por semana)", "Thamires", "estagio",
                  "Dois dias por semana (quarta e sexta)"),
    },
    "ciclos": [
        ("Piloto 2026", "piloto", "2026-11-01", "2026-12-31", False),
        ("1º semestre de 2027", "regular", "2027-01-01", "2027-06-30", True),
        ("2º semestre de 2027", "regular", "2027-07-01", "2027-12-31", True),
    ],
}
