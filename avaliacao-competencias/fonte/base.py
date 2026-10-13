# -*- coding: utf-8 -*-
"""Base do modelo de avaliação por competências da R2 Tech Consultoria.

Vale para qualquer empresa. Textos com {gestor} recebem o nome de quem avalia.
O que é próprio de cada cliente fica em casos.py.
"""


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

# (código, nome, definição, nível 1, nível 3, nível 5)
COMUNS = [
    ("C1", "Qualidade e conformidade com procedimentos",
     "Executa conforme o passo a passo e o checklist, confere antes de entregar e registra a evidência.",
     "Entrega sem conferir, pula etapas do checklist, conclui cartão sem o documento.",
     "Segue o procedimento, confere e anexa a evidência; erros são raros e corrigidos assim que apontados.",
     "Encontra o erro antes que chegue ao cliente e propõe ajustes no procedimento."),
    ("C2", "Cumprimento de prazos",
     "Entrega no prazo combinado e avisa com antecedência quando há risco de atraso.",
     "Perde prazos ou entrega em cima da hora sem avisar.",
     "Cumpre os prazos da rotina e avisa antes quando algo vai atrasar.",
     "Organiza a semana pelos vencimentos, antecipa entregas críticas e ajuda a destravar prazos dos colegas."),
    ("C3", "Proatividade",
     "Identifica pendências e age sem precisar ser cobrada.",
     "Espera ser lembrada para agir.",
     "Percebe as pendências da própria rotina e resolve sem cobrança.",
     "Antecipa problemas de clientes e da empresa e chega com a solução junto com o problema."),
    ("C4", "Autonomia",
     "Consulta o procedimento e a base de conhecimento antes de escalar; quando escala, leva o caso já levantado.",
     "Leva toda dúvida {ao_gestor} sem consultar o material disponível.",
     "Resolve as dúvidas comuns com os passo a passos e escala só exceções, com as informações reunidas.",
     "Resolve situações novas com bom critério e registra a solução para a equipe."),
    ("C5", "Comunicação escrita e atendimento",
     "Escreve de forma clara e cordial, retorna o cliente no prazo e registra o que foi combinado.",
     "Mensagens incompletas ou confusas; cliente fica sem retorno.",
     "Mensagens claras e cordiais, retorno no prazo, combinados registrados.",
     "Antecipa as dúvidas do cliente e cria modelos de mensagem que a equipe passa a usar."),
    ("C6", "Comprometimento",
     "Assume a responsabilidade pelas próprias entregas e cumpre o que combinou.",
     "Deixa pendência crítica sem combinar o repasse; não reconhece os próprios erros.",
     "Assume as entregas, cumpre combinados, reconhece e corrige os erros.",
     "Age como dona do resultado do processo e se oferece para cobrir quando falta alguém, dentro da jornada combinada."),
    ("C7", "Colaboração",
     "Apoia colegas, compartilha o que sabe e cobre ausências quando combinado.",
     "Trabalha isolada; o que sabe fica só com ela.",
     "Ajuda quando solicitada e repassa informações completas nas trocas e coberturas.",
     "Ensina, documenta e organiza coberturas sem precisar de intervenção {do_gestor}."),
    ("C8", "Evolução profissional",
     "Aplica o feedback recebido e cumpre as ações do plano de desenvolvimento.",
     "Repete os mesmos erros e não busca aprender.",
     "Aplica o feedback e cumpre as ações combinadas no plano de desenvolvimento.",
     "Busca aprender por conta própria, aplica e ensina o que aprendeu."),
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

# Trilha de liderança (desenvolvimento; não entra na nota)
LIDERANCA = [
    ("L1", "Priorização", "Organiza as demandas da equipe por prazo e impacto e deixa claro o que vem primeiro."),
    ("L2", "Delegar e acompanhar", "Distribui tarefas com instrução clara e acompanha até a entrega, sem fazer pela pessoa."),
    ("L3", "Feedback", "Dá retorno direto e respeitoso aos colegas e recebe críticas sem se defender."),
    ("L4", "Eficácia", "Mede o próprio trabalho pelo resultado entregue, não pelo volume de tarefas."),
    ("L5", "Postura de referência", "Representa os combinados da empresa diante da equipe e dos clientes."),
]

# Biblioteca de competências técnicas por área: escolher de 4 a 6 por cargo e ajustar ao processo do cliente.
# área -> lista de (competência, o que é atender (nota 3), evidência / indicador sugerido)
BIBLIOTECA = {
    "Atendimento e secretaria": [
        ("Triagem e distribuição das demandas", "Toda demanda recebida é registrada e distribuída ao responsável no mesmo dia.", "Demandas distribuídas no dia (%)"),
        ("Agenda e documentos", "Agenda em dia; documentos salvos no lugar certo, no padrão de nome combinado.", "Conferência por amostra"),
        ("Implantação de novos clientes", "Checklist de entrada do cliente cumprido por completo, sem pendência aberta.", "Tempo de implantação; checklists completos (%)"),
        ("Atendimento ao cliente", "Responde no prazo combinado, com informação correta e registro do atendimento.", "Tempo de resposta; reclamações"),
        ("Envio de documentos aos clientes", "Envia guias, relatórios e documentos a todos os clientes, conferindo se o documento é do cliente certo.", "Envios registrados; documentos trocados"),
    ],
    "Comercial": [
        ("Qualificação de contatos", "Registra todo contato e identifica necessidade, porte e serviço adequado antes da reunião.", "Contatos qualificados (%)"),
        ("Propostas", "Monta propostas a partir do modelo, com escopo e preço conferidos, no prazo combinado.", "Propostas enviadas no prazo (%)"),
        ("Acompanhamento (follow-up)", "Retoma todas as propostas abertas nas datas combinadas.", "Propostas sem retorno há mais de 7 dias"),
        ("Contratos e passagem para a operação", "Contrato assinado e dados completos entregues à operação antes do início.", "Clientes iniciados com dados completos (%)"),
        ("Indicação e relacionamento", "Pede indicações e mantém contato com a base de clientes conforme o plano.", "Clientes indicados que fecharam"),
    ],
    "Financeiro": [
        ("Contas a pagar", "Pagamentos feitos no dia, com documento conferido (favorecido, valor e vencimento).", "Pagamentos sem atraso e sem erro (%)"),
        ("Contas a receber e cobrança", "Recebimentos baixados e inadimplência cobrada conforme a régua combinada.", "Inadimplência; títulos sem baixa"),
        ("Conciliação bancária", "Contas conciliadas na frequência combinada, sem diferenças em aberto.", "Contas conciliadas no prazo (%)"),
        ("Emissão de notas fiscais", "Notas emitidas no prazo e com os dados corretos.", "Notas canceladas ou corrigidas"),
        ("Fechamento e relatórios", "Fechamento do mês pronto na data combinada, com explicação das variações.", "Fechamentos no prazo (%)"),
        ("Análise e revisão", "Identifica lançamentos e classificações inconsistentes antes do fechamento.", "Inconsistências apontadas antes da entrega"),
    ],
    "Contabilidade": [
        ("Lançamentos e integrações", "Movimento do mês lançado ou integrado e conferido dentro do prazo interno.", "Empresas com movimento lançado no prazo (%)"),
        ("Conciliações contábeis", "Contas patrimoniais conciliadas, com diferenças explicadas.", "Contas conciliadas (%)"),
        ("Balancete e demonstrações", "Balancete revisado e demonstrações entregues no prazo.", "Balancetes entregues no prazo (%)"),
        ("Obrigações acessórias contábeis", "ECD, ECF e demais obrigações transmitidas no prazo, com recibo arquivado.", "Obrigações no prazo; multas"),
        ("Encerramento do exercício", "Encerramento feito com checklist e revisão técnica.", "Pendências no encerramento"),
    ],
    "Fiscal": [
        ("Captura de documentos fiscais", "Notas de entrada e saída de todos os clientes capturadas e conferidas no mês.", "Clientes com documentos completos (%)"),
        ("Cadastro e parametrização tributária", "Regime, atividades, alíquotas e município de cada cliente conferidos e atualizados no sistema.", "Cadastros revisados; erros de parâmetro"),
        ("Apuração de impostos", "Apurações feitas e conferidas por outra pessoa antes de gerar a guia.", "Apurações com retificação"),
        ("Guias e envio", "Guias geradas, conferidas e enviadas ao cliente antes do vencimento, com evidência.", "Guias enviadas no prazo (%)"),
        ("Obrigações acessórias fiscais", "Declarações transmitidas no prazo, inclusive as sem movimento, com recibo arquivado.", "Obrigações no prazo; multas"),
    ],
    "Departamento Pessoal": [
        ("Folha de pagamento", "Folhas fechadas e enviadas dentro do prazo combinado com o cliente.", "Folhas no prazo (%)"),
        ("Admissões e rescisões", "Documentos completos e prazos legais cumpridos em cada processo.", "Processos sem pendência ou multa"),
        ("eSocial e obrigações trabalhistas", "Eventos e obrigações transmitidos em dia, sem pendência no sistema.", "Pendências no eSocial"),
        ("Férias, benefícios e afastamentos", "Programação e cálculos feitos dentro dos prazos legais.", "Ocorrências fora do prazo"),
        ("Atendimento aos clientes de DP", "Dúvidas sobre funcionários respondidas no prazo combinado, com registro.", "Dúvidas respondidas no prazo (%)"),
    ],
    "Jurídico e societário": [
        ("Acompanhamento de processos e prazos", "Andamentos acompanhados e nenhum prazo perdido.", "Prazos cumpridos (%)"),
        ("Peças e contratos", "Peças e contratos feitos a partir dos modelos, com cada vez menos correção.", "Correções por peça"),
        ("Atos societários", "Abertura, alteração e baixa de empresas seguindo o checklist, nos prazos dos órgãos.", "Processos concluídos sem exigência"),
        ("Organização e registro", "Pastas e andamentos atualizados, para qualquer pessoa achar a informação.", "Conferência por amostra"),
    ],
    "Administrativo e operações (qualquer ramo)": [
        ("Execução da rotina do cargo", "Cumpre as tarefas da rotina no prazo, seguindo o procedimento documentado.", "Tarefas no prazo com evidência (%)"),
        ("Controle e registro", "Registra o que fez no sistema de tarefas, com evidência anexada.", "Tarefas concluídas com evidência (%)"),
        ("Uso das ferramentas", "Usa os sistemas da empresa como combinado, sem controles paralelos.", "Controles paralelos encontrados"),
        ("Melhoria do processo", "Aponta gargalos e propõe ajustes no procedimento do seu processo.", "Melhorias propostas e adotadas"),
        ("Gestão de fornecedores e compras", "Compras e contratos com fornecedores feitos com cotação e aprovação.", "Compras sem aprovação"),
    ],
}


def comuns(cfg):
    """Competências comuns com o nome de quem avalia já aplicado."""
    return [tuple(t.format(**cfg) for t in c) for c in COMUNS]
