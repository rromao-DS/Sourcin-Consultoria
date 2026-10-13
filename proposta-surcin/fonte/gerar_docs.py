# -*- coding: utf-8 -*-
"""Gera os documentos Word da proposta Surcin (versão preliminar, 13/10/2026)."""
import sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SAIDA = sys.argv[1] if len(sys.argv) > 1 else "."
AZUL = RGBColor(0x1F, 0x3A, 0x5F)
CINZA = RGBColor(0x59, 0x59, 0x59)
VERSAO = "Versão preliminar · 13/10/2026 · uso interno até revisão do Renato"


def novo_doc(titulo, subtitulo):
    d = Document()
    for s in d.sections:
        s.left_margin = s.right_margin = Cm(2.2)
        s.top_margin = s.bottom_margin = Cm(2)
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    for nome, tam in (("Heading 1", 16), ("Heading 2", 13), ("Heading 3", 11.5)):
        h = d.styles[nome]
        h.font.name = "Calibri"
        h.font.size = Pt(tam)
        h.font.color.rgb = AZUL
        h.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    p = d.add_paragraph()
    r = p.add_run(titulo)
    r.bold = True
    r.font.size = Pt(22)
    r.font.color.rgb = AZUL
    p = d.add_paragraph()
    r = p.add_run(subtitulo)
    r.font.size = Pt(13)
    r.font.color.rgb = CINZA
    p = d.add_paragraph()
    r = p.add_run(VERSAO)
    r.italic = True
    r.font.size = Pt(9)
    r.font.color.rgb = CINZA
    rodape = d.sections[0].footer.paragraphs[0]
    rodape.text = "Surcin Consultoria · Proposta de consultoria em organização e processos · Confidencial"
    rodape.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rodape.runs[0].font.size = Pt(8)
    rodape.runs[0].font.color.rgb = CINZA
    return d


def h(d, texto, nivel=1):
    d.add_heading(texto, level=nivel)


def par(d, texto, negrito_ini=None, italico=False):
    p = d.add_paragraph()
    if negrito_ini:
        p.add_run(negrito_ini).bold = True
    r = p.add_run(texto)
    r.italic = italico
    return p


def lista(d, itens, numerada=False):
    estilo = "List Number" if numerada else "List Bullet"
    for i in itens:
        p = d.add_paragraph(style=estilo)
        if isinstance(i, tuple):
            p.add_run(i[0]).bold = True
            p.add_run(i[1])
        else:
            p.add_run(i)


def sombrear(celula, cor):
    tcPr = celula._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), cor)
    tcPr.append(shd)


def tabela(d, cabecalho, linhas, larguras=None):
    t = d.add_table(rows=1, cols=len(cabecalho))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, c in enumerate(cabecalho):
        cel = t.rows[0].cells[i]
        cel.text = ""
        r = cel.paragraphs[0].add_run(c)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        sombrear(cel, "1F3A5F")
    for li in linhas:
        cels = t.add_row().cells
        for i, v in enumerate(li):
            cels[i].text = ""
            texto = str(v)
            negrito = texto.startswith("**")
            r = cels[i].paragraphs[0].add_run(texto.strip("*"))
            r.font.size = Pt(10)
            r.bold = negrito
    if larguras:
        for row in t.rows:
            for i, w in enumerate(larguras):
                row.cells[i].width = Cm(w)
    d.add_paragraph()
    return t


def aviso(d, texto):
    t = d.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    cel = t.rows[0].cells[0]
    sombrear(cel, "FFF4D6")
    cel.text = ""
    r = cel.paragraphs[0].add_run(texto)
    r.font.size = Pt(10)
    d.add_paragraph()


LEGENDA = ("Legenda usada neste documento: [FATO] confirmado na reunião ou no briefing; "
           "[HIPÓTESE] inferência do consultor, a validar; [PREENCHER] completar com a "
           "transcrição ou a gravação da reunião de 12/10/2026.")


# ---------------------------------------------------------------------------
# 01 · Diagnóstico preliminar
# ---------------------------------------------------------------------------
def diagnostico():
    d = novo_doc("Diagnóstico preliminar", "Surcin Consultoria · leitura da reunião de descoberta")
    aviso(d, "Este documento foi montado antes da chegada da transcrição. Tudo que não está marcado "
             "como [FATO] precisa ser conferido com a gravação antes de ir para a Thamires. "
             "Nenhum número, processo ou volume da empresa foi inventado: os campos vazios estão "
             "marcados como [PREENCHER].")
    par(d, LEGENDA, italico=True)

    h(d, "1. O que já foi feito")
    par(d, "Em 12/10/2026 foi realizada a reunião de descoberta com a Thamires, com duração de cerca "
           "de 2h30. Nela, a cliente apresentou a empresa de ponta a ponta. Por isso, essa reunião é "
           "tratada como a primeira parte do diagnóstico, e não como uma conversa comercial prévia.")
    par(d, "O que ainda falta para fechar o diagnóstico: ouvir os funcionários que executam as tarefas, "
           "entender os insumos (inputs) de cada rotina, de onde vêm, quem os produz e quem depende deles.")

    h(d, "2. Perfil da empresa")
    tabela(d, ["Item", "Situação", "Fonte"], [
        ["Responsável / decisora", "Thamires, contadora e advogada de formação, dona do escritório", "[FATO] briefing"],
        ["Tipo de negócio", "Escritório próprio com serviços contábeis [confirmar se presta serviços jurídicos também]", "[FATO] / [PREENCHER]"],
        ["Áreas identificadas", "Departamento Pessoal, Financeiro, Contabilidade, Vendas", "[FATO] briefing"],
        ["Objetivo declarado", "Organizar e automatizar os processos da empresa", "[FATO] briefing"],
        ["Número de funcionários e por área", "", "[PREENCHER]"],
        ["Número de clientes atendidos", "", "[PREENCHER]"],
        ["Volume mensal (folhas, lançamentos, guias, contratos)", "", "[PREENCHER]"],
        ["Faturamento ou porte (se ela citou)", "", "[PREENCHER]"],
    ], [4.5, 8, 3.5])

    h(d, "3. Ferramentas citadas")
    par(d, "As ferramentas abaixo foram mencionadas na reunião. A finalidade e o uso efetivo de cada uma "
           "ainda precisam ser confirmados.")
    tabela(d, ["Ferramenta", "Uso provável", "Área", "Status"], [
        ["Conta Azul", "Gestão financeira / ERP [HIPÓTESE]", "Financeiro", "[PREENCHER] uso real e quem acessa"],
        ["Domínio", "Sistema contábil e fiscal / folha [HIPÓTESE]", "Contabilidade, DP", "[PREENCHER]"],
        ["Veri (veri.com.br)", "[PREENCHER] finalidade", "[PREENCHER]", "[PREENCHER]"],
        ["Jusbrasil", "Pesquisa jurídica / acompanhamento de processos [HIPÓTESE]", "[PREENCHER]", "[PREENCHER]"],
        ["Microsoft OneDrive", "Armazenamento e compartilhamento de arquivos [HIPÓTESE]", "Todas", "[PREENCHER] organização das pastas"],
        ["Trello", "Gestão de tarefas [HIPÓTESE]", "[PREENCHER]", "[PREENCHER] quem usa e como"],
        ["NetsApp", "[PREENCHER] finalidade", "[PREENCHER]", "[PREENCHER]"],
    ], [3, 5.5, 3, 4.5])

    h(d, "4. Necessidades, dores e expectativas")
    par(d, "Preencher com a transcrição. Para cada dor, registrar a frase da cliente (ou o minuto da "
           "gravação), a área afetada e o impacto que ela descreveu.")
    tabela(d, ["#", "Dor ou necessidade (palavras da cliente)", "Área", "Impacto citado", "Minuto na gravação"],
           [[str(i), "[PREENCHER]", "", "", ""] for i in range(1, 7)], [0.8, 6.5, 2.5, 3.5, 2.7])
    par(d, "Expectativas a registrar: o que ela considera sucesso, em que prazo espera ver resultado, "
           "se mencionou orçamento, e se quer autonomia da equipe ou um serviço gerenciado.")

    h(d, "5. Leitura preliminar do consultor")
    par(d, "Observações que se apoiam apenas no que já se sabe e que servem como hipóteses de trabalho:")
    lista(d, [
        ("[HIPÓTESE] Muitas ferramentas para um escritório pequeno. ",
         "Sete sistemas citados indicam risco de informação duplicada e retrabalho entre eles. A confirmar no inventário."),
        ("[HIPÓTESE] Dependência da dona. ",
         "Uma empresária com dupla formação tende a concentrar decisões e conhecimento técnico. A confirmar nas entrevistas."),
        ("[HIPÓTESE] Responsabilidades pouco formalizadas. ",
         "O pedido de organizar a empresa sugere que papéis e fluxos não estão escritos. Por isso a estrutura organizacional entra na proposta."),
        ("[HIPÓTESE] Dados sensíveis. ",
         "DP trata dados pessoais e o escritório tem sigilo profissional. Qualquer automação passa por LGPD e acesso mínimo."),
        ("[HIPÓTESE] Domínio com integração limitada. ",
         "Não prometer automação dentro do Domínio antes de verificar o que ele permite exportar ou integrar."),
    ])

    h(d, "6. Lacunas e perguntas objetivas")
    par(d, "Use esta lista para conferir a gravação. O que a gravação não responder vira pergunta para a "
           "Thamires na apresentação de quinta ou na primeira entrevista.")
    blocos = {
        "Empresa e pessoas": [
            "Quantas pessoas trabalham hoje no escritório e em qual área está cada uma?",
            "Quem é responsável por cada área? Existe alguém além da Thamires que toma decisões?",
            "Há funcionários terceirizados, estagiários ou parceiros externos (ex.: advogados, correspondentes)?",
            "Quantos clientes o escritório atende hoje, e de que tipo (MEI, Simples, Lucro Presumido, pessoa física)?",
        ],
        "Departamento Pessoal": [
            "Quantas folhas de pagamento são processadas por mês?",
            "Como chegam as informações de admissão, férias e rescisão dos clientes (e-mail, WhatsApp, planilha, sistema)?",
            "Quais etapas da folha são feitas no Domínio e quais são manuais?",
        ],
        "Financeiro": [
            "O Conta Azul é usado para o financeiro do próprio escritório, dos clientes ou de ambos?",
            "Como é feita a cobrança dos honorários e quem acompanha a inadimplência?",
            "Quem concilia as contas e com que frequência?",
        ],
        "Contabilidade": [
            "Como os clientes enviam documentos (notas, extratos, comprovantes) e com que atraso costumam enviar?",
            "Quais obrigações e prazos mensais mais geram retrabalho ou multa?",
            "Quanto do lançamento é importado automaticamente e quanto é digitado?",
        ],
        "Vendas": [
            "Como chegam os novos clientes hoje (indicação, internet, parceiros)?",
            "Existe proposta padrão, contrato padrão e processo de entrada (onboarding) do cliente?",
            "Quem faz o atendimento comercial e acompanha os orçamentos enviados?",
        ],
        "Ferramentas e dados": [
            "Para que serve o Veri e o NetsApp no dia a dia, e quem usa?",
            "Quem tem acesso de administrador a cada sistema?",
            "Como estão organizadas as pastas no OneDrive? Há padrão de nomes?",
            "O Trello é usado por toda a equipe ou só por algumas pessoas?",
        ],
        "Expectativas e condições": [
            "Qual é a dor que, se resolvida primeiro, mais mudaria o dia a dia dela?",
            "Em quanto tempo ela espera ver o primeiro resultado?",
            "Ela tem uma faixa de investimento em mente para esta etapa?",
            "A equipe pode participar de entrevistas fora do horário comercial (antes das 10h ou após 19h30) ou em horário de almoço?",
            "Ela prefere que a equipe aprenda a manter as melhorias ou que o consultor mantenha?",
        ],
    }
    for titulo, perguntas in blocos.items():
        h(d, titulo, 3)
        lista(d, perguntas, numerada=False)

    h(d, "7. Próximos passos do diagnóstico")
    lista(d, [
        "Conferir a transcrição e a gravação e preencher os campos [PREENCHER].",
        "Apresentar a proposta na quinta-feira, 15/10/2026, e validar as lacunas principais com a Thamires.",
        "Após o aceite: entrevistas com os funcionários de cada área para levantar os insumos de cada tarefa.",
        "Consolidar o mapeamento e a proposta de estrutura organizacional (Etapas 1 e 2 da proposta).",
    ], numerada=True)
    d.save(f"{SAIDA}/01-diagnostico-preliminar.docx")


# ---------------------------------------------------------------------------
# 02 · Estrutura organizacional (hipótese inicial)
# ---------------------------------------------------------------------------
def estrutura():
    d = novo_doc("Estrutura organizacional", "Hipótese inicial para validação · organograma, áreas, papéis e responsabilidades")
    aviso(d, "Este é um ponto de partida para conversa, não uma recomendação final. Ainda não se sabe "
             "quantas pessoas trabalham no escritório nem como as tarefas estão divididas hoje. A versão "
             "recomendada só sai depois das entrevistas com os funcionários (Etapas 1 e 2 da proposta).")

    h(d, "1. É viável recomendar uma estrutura agora?")
    par(d, "Sim, como hipótese. O que já se sabe (quatro áreas e uma sócia que concentra a direção) permite "
           "desenhar um modelo de referência e mostrar à Thamires como ficará o resultado. Não é possível, "
           "ainda, dizer quem deve ocupar cada papel, nem se alguma área precisa de mais ou menos pessoas.")
    par(d, "Recomendação para quinta-feira: mostrar o modelo abaixo como exemplo do entregável e pedir que "
           "ela corrija em voz alta. As correções dela já são dados de diagnóstico.")

    h(d, "2. Organograma de referência")
    par(d, "Modelo funcional simples, adequado a escritórios de pequeno porte. Os nomes das áreas vêm da "
           "reunião; a camada de coordenação e o apoio administrativo são [HIPÓTESE].")
    org = [
        "Direção · Thamires (sócia, responsável técnica contábil e jurídica)",
        "    ├── Departamento Pessoal · responsável: [PREENCHER]",
        "    ├── Contabilidade e Fiscal · responsável: [PREENCHER]",
        "    ├── Financeiro (do próprio escritório) · responsável: [PREENCHER]",
        "    ├── Comercial / Vendas · responsável: [PREENCHER]",
        "    └── Apoio administrativo e atendimento [HIPÓTESE: confirmar se existe]",
    ]
    for linha in org:
        p = d.add_paragraph()
        r = p.add_run(linha)
        r.font.name = "Consolas"
        r.font.size = Pt(10)
        p.paragraph_format.space_after = Pt(0)
    d.add_paragraph()

    h(d, "3. Missão e responsabilidades de cada área")
    tabela(d, ["Área", "Missão (proposta)", "Responsabilidades típicas [HIPÓTESE]", "Sistemas citados"], [
        ["Direção", "Definir prioridades, aprovar e responder tecnicamente",
         "Aprovação de entregas críticas, relacionamento com clientes-chave, decisões de preço e contratação", "Todos (consulta)"],
        ["Departamento Pessoal", "Garantir folha e obrigações trabalhistas no prazo",
         "Admissões, folha, férias, rescisões, encargos, atendimento a dúvidas trabalhistas dos clientes", "Domínio [confirmar]"],
        ["Contabilidade e Fiscal", "Manter escrituração e obrigações dos clientes em dia",
         "Recebimento de documentos, lançamentos, apuração de impostos, obrigações acessórias, balanços", "Domínio [confirmar]"],
        ["Financeiro", "Manter o caixa do escritório saudável",
         "Faturamento de honorários, cobrança, contas a pagar, conciliação, relatórios para a Direção", "Conta Azul [confirmar]"],
        ["Comercial / Vendas", "Trazer e integrar novos clientes",
         "Atendimento a interessados, propostas, contratos, onboarding do cliente", "[PREENCHER]"],
    ], [3, 3.8, 6.2, 3])

    h(d, "4. Papéis transversais sugeridos")
    par(d, "Em equipes pequenas, uma mesma pessoa acumula papéis. Formalizá-los evita que tarefas fiquem sem dono.")
    lista(d, [
        ("Dono do processo: ", "responde pelo resultado de um fluxo de ponta a ponta (ex.: folha mensal), mesmo que outras pessoas executem partes."),
        ("Ponto focal do cliente: ", "pessoa única de contato para cada cliente, que recebe e distribui as demandas."),
        ("Responsável por ferramentas: ", "mantém acessos, padrões de pastas no OneDrive e quadros do Trello."),
        ("Guardião de dados (LGPD): ", "controla quem acessa dados pessoais e documentos sigilosos."),
    ])

    h(d, "5. Matriz de responsabilidades (modelo RACI)")
    par(d, "R = executa · A = aprova e responde · C = é consultado · I = é informado. "
           "Exemplo de preenchimento; a matriz real será construída nas entrevistas.")
    tabela(d, ["Atividade (exemplo)", "Direção", "DP", "Contábil", "Financeiro", "Comercial"], [
        ["Fechar folha mensal de um cliente", "I", "R/A", "C", "I", "-"],
        ["Apurar impostos do mês", "A", "C", "R", "I", "-"],
        ["Faturar e cobrar honorários", "A", "-", "-", "R", "I"],
        ["Enviar proposta a novo cliente", "A", "C", "C", "C", "R"],
        ["Cadastrar novo cliente nos sistemas", "I", "R", "R", "R", "A"],
    ], [5.5, 2, 1.8, 2, 2.2, 2.3])

    h(d, "6. O que precisamos confirmar para fechar a estrutura")
    lista(d, [
        "Quantas pessoas existem e quais tarefas cada uma executa de fato hoje.",
        "Se há alguém, além da Thamires, com autonomia para aprovar entregas.",
        "Se o Financeiro cuida só do escritório ou também presta serviço financeiro a clientes.",
        "Se existe atendimento/recepção separado e quem responde aos clientes no WhatsApp e e-mail.",
        "Se Vendas é uma função de alguém ou se a própria Thamires vende.",
    ], numerada=True)

    h(d, "7. Entregável final desta frente (Etapa 2 da proposta)")
    lista(d, [
        "Organograma atual (como é) e organograma proposto (como deve ser).",
        "Descrição de papéis por área: missão, responsabilidades, entregas e indicadores simples.",
        "Matriz RACI das atividades principais.",
        "Lista de sobreposições, lacunas de responsabilidade e dependências da Direção.",
    ])
    d.save(f"{SAIDA}/02-estrutura-organizacional-hipotese.docx")


# ---------------------------------------------------------------------------
# 03 · Metodologia de mapeamento de fluxos
# ---------------------------------------------------------------------------
def metodologia():
    d = novo_doc("Metodologia de mapeamento de processos",
                 "Como vamos levantar fluxos, gargalos e dependências e propor melhorias e automações")

    h(d, "1. Princípios")
    lista(d, [
        ("Entender antes de automatizar. ", "Nenhuma automação é proposta antes de o processo atual estar desenhado e validado por quem o executa."),
        ("Ouvir quem faz. ", "A Thamires conhece o negócio; os funcionários conhecem os detalhes. As duas visões são necessárias."),
        ("Começar pelo que dói mais. ", "Mapeamento detalhado apenas dos processos prioritários; os demais ficam em nível macro."),
        ("Sigilo e LGPD. ", "Documentos de clientes são vistos apenas como exemplo, com acesso mínimo e acordo de confidencialidade."),
        ("Respeitar a rotina da equipe. ", "Entrevistas curtas (45 a 60 min), agendadas fora dos picos de fechamento."),
    ])

    h(d, "2. Etapas do método")
    etapas = [
        ("Etapa A · Inventário de processos (macro). ",
         "Listar todos os processos por área, com frequência, responsável e sistema. Resultado: cadeia de valor do escritório em uma página."),
        ("Etapa B · Priorização. ",
         "Pontuar cada processo de 1 a 5 em quatro critérios: dor relatada, volume/frequência, risco (multa, erro, sigilo) e facilidade de melhoria. Os de maior nota seguem para o mapeamento detalhado."),
        ("Etapa C · Entrevistas com executores. ",
         "Roteiro padrão (seção 3) para entender passos, insumos, saídas, tempo gasto e exceções. Sempre que possível, acompanhar a tarefa sendo feita."),
        ("Etapa D · Desenho do fluxo atual (AS-IS). ",
         "Diagrama em raias (uma raia por pessoa ou área), mostrando passos, decisões, sistemas e esperas. Ferramenta sugerida: draw.io ou Miro, salvos no OneDrive da cliente."),
        ("Etapa E · Validação. ",
         "O fluxo desenhado é revisado com quem executa e com a Thamires. Só fluxos validados seguem para análise."),
        ("Etapa F · Análise de gargalos e dependências. ",
         "Identificar esperas, retrabalho, digitação duplicada, aprovações concentradas e pontos únicos de falha. Montar a matriz de dependências entre pessoas e áreas."),
        ("Etapa G · Fluxo otimizado (TO-BE). ",
         "Primeiro simplificar (eliminar, padronizar, reorganizar responsabilidades), depois automatizar. Cada mudança indica ganho esperado e esforço."),
        ("Etapa H · Backlog de automação. ",
         "Lista priorizada das oportunidades, com estimativa de esforço em pacotes P, M ou G. Essa lista é a base da proposta de implementação, que é separada."),
    ]
    lista(d, etapas, numerada=False)

    h(d, "3. Roteiro de entrevista com funcionários")
    par(d, "Duração: 45 a 60 minutos por pessoa. Uma entrevista por processo prioritário ou por pessoa-chave.")
    lista(d, [
        "Quais são as suas tarefas em um mês típico? Quais são diárias, semanais e mensais?",
        "Para esta tarefa, o que você precisa receber para começar? De quem e por qual canal?",
        "Quais são os passos, na ordem? Em qual sistema cada passo é feito?",
        "O que você entrega no final, para quem e em que formato?",
        "Quanto tempo leva, em média? E no pior mês?",
        "Onde você costuma esperar por alguém ou por um documento?",
        "O que você digita mais de uma vez em lugares diferentes?",
        "O que dá errado com mais frequência? O que acontece quando dá errado?",
        "Quem precisa aprovar algo antes de você seguir?",
        "Se você pudesse mudar uma coisa nesta tarefa, o que seria?",
    ], numerada=True)

    h(d, "4. Ficha de registro de cada processo")
    tabela(d, ["Campo", "O que registrar"], [
        ["Nome e área", "Ex.: Admissão de funcionário de cliente · DP"],
        ["Dono do processo", "Quem responde pelo resultado"],
        ["Gatilho", "O que inicia o processo (pedido do cliente, data do mês etc.)"],
        ["Insumos", "Documentos e informações necessárias, origem e canal"],
        ["Passos e responsáveis", "Sequência, quem faz, em que sistema"],
        ["Saídas", "O que é entregue, para quem, formato e prazo"],
        ["Volume e tempo", "Quantas vezes por mês e quanto tempo por execução"],
        ["Sistemas", "Domínio, Conta Azul, Trello, OneDrive, planilhas, WhatsApp etc."],
        ["Problemas", "Esperas, retrabalho, erros, multas, reclamações"],
        ["Dados sensíveis", "Há dados pessoais ou sigilosos? Quem acessa?"],
    ], [4, 12])

    h(d, "5. Como identificamos gargalos e dependências")
    tabela(d, ["Sinal", "Como aparece", "Tipo de melhoria provável"], [
        ["Espera", "Tarefa parada aguardando documento ou aprovação", "Prazos combinados, lembretes automáticos, checklist de envio"],
        ["Retrabalho", "Mesmo dado digitado em dois sistemas", "Integração ou importação; padronização"],
        ["Aprovação concentrada", "Tudo depende da Thamires", "Delegação com regras claras (estrutura organizacional)"],
        ["Ponto único de falha", "Só uma pessoa sabe fazer", "Documentação do procedimento e treinamento cruzado"],
        ["Erro recorrente", "Correções e multas frequentes", "Validações, checklists, conferência automática"],
        ["Comunicação dispersa", "Pedidos por WhatsApp, e-mail e telefone", "Canal único de entrada e quadro de demandas"],
    ], [3.5, 6, 6.5])
    par(d, "Matriz de dependências: tabela pessoa × pessoa (ou área × área) indicando quem depende de quem "
           "para quais entregas. As células com mais dependências mostram onde a operação trava.")

    h(d, "6. Critérios para propor uma automação")
    lista(d, [
        "O processo está validado e simplificado antes de ser automatizado.",
        "Há volume ou risco suficiente para justificar o esforço (horas economizadas × custo da hora da equipe).",
        "Os sistemas envolvidos permitem exportação, importação ou integração (verificado, não suposto).",
        "Existe alguém da equipe responsável por operar e acompanhar a automação.",
        "O tratamento de dados pessoais está de acordo com a LGPD.",
    ])

    h(d, "7. Entregáveis do mapeamento")
    lista(d, [
        "Inventário macro de processos por área e matriz de priorização.",
        "Fluxos AS-IS dos processos prioritários, validados.",
        "Matriz de dependências e lista de gargalos com evidências.",
        "Fluxos TO-BE dos processos prioritários.",
        "Backlog de oportunidades de automação, priorizado e estimado em pacotes.",
    ])
    d.save(f"{SAIDA}/03-metodologia-mapeamento-processos.docx")


# ---------------------------------------------------------------------------
# 04 · Proposta comercial
# ---------------------------------------------------------------------------
def proposta():
    d = novo_doc("Proposta de consultoria", "Organização, estrutura e processos · Surcin Consultoria")
    aviso(d, "Valores e prazos calculados com taxa de referência de R$ 180/h e capacidade de 10 h/semana "
             "do consultor, com 20% de contingência. Ambos aguardam confirmação do Renato antes do envio.")

    h(d, "1. Contexto")
    par(d, "A Surcin Consultoria, liderada pela Thamires, deseja organizar e automatizar os processos do "
           "escritório, que hoje se dividem em Departamento Pessoal, Financeiro, Contabilidade e Vendas, "
           "com apoio de ferramentas como Conta Azul, Domínio, Veri, Jusbrasil, OneDrive, Trello e NetsApp.")
    par(d, "Na reunião de descoberta de 12/10/2026, a Thamires apresentou a empresa em detalhe. Essa conversa "
           "já é a primeira parte do diagnóstico. O próximo passo é ouvir a equipe que executa as tarefas e "
           "entender os insumos de cada rotina, para então propor estrutura, fluxos e automações com segurança.")
    par(d, "[PREENCHER com 2 ou 3 dores citadas pela Thamires, nas palavras dela, a partir da transcrição.]", italico=True)

    h(d, "2. Objetivos")
    lista(d, [
        "Dar clareza sobre quem faz o quê: estrutura organizacional, papéis e responsabilidades.",
        "Tornar visíveis os fluxos de trabalho, seus gargalos e as dependências entre pessoas e áreas.",
        "Propor fluxos otimizados e uma lista priorizada de automações, com esforço e ganho estimados.",
        "Preparar a implementação de forma segura, por pacotes, com escopo e preço definidos antes.",
    ])

    h(d, "3. Abordagem em etapas")
    par(d, "O trabalho segue uma sequência simples: primeiro entender como a empresa funciona hoje, depois "
           "organizar quem faz o quê e, só então, redesenhar fluxos e planejar automações. A implementação "
           "das automações não faz parte desta proposta: ela será orçada com base no que o mapeamento revelar.")
    tabela(d, ["Etapa", "O que é", "Situação"], [
        ["0 · Reunião inicial e diagnóstico preliminar", "Conversa de 2h30 com a Thamires sobre toda a empresa; leitura apresentada nesta reunião", "Concluída, sem custo"],
        ["1 · Mapeamento dos processos atuais", "Entrevistas com a equipe, insumos e saídas de cada tarefa, gargalos e dependências entre pessoas e áreas", "Nesta proposta"],
        ["2 · Estrutura organizacional", "Organograma atual e proposto, áreas, papéis e matriz de responsabilidades", "Nesta proposta"],
        ["3 · Fluxos otimizados e plano de automação", "Redesenho dos processos prioritários e lista de automações com esforço estimado", "Nesta proposta (opção Completa)"],
        ["4 · Implementação e acompanhamento", "Execução das melhorias em pacotes e ajustes mensais", "Proposta futura, após a Etapa 3"],
    ], [4.5, 8, 3.5])

    h(d, "4. Escopo e entregáveis: duas opções")
    par(d, "A Thamires escolhe o tamanho do escopo. A opção Essencial pode ser ampliada depois para a Completa por aditivo.")
    tabela(d, ["Entregável", "Essencial", "Completa (recomendada)"], [
        ["Entrevistas com a equipe (cerca de 1 h cada)", "Até 4 pessoas", "Até 5 pessoas"],
        ["Processos atuais mapeados e validados", "Até 5", "Até 8"],
        ["Gargalos e matriz de dependências", "Sim", "Sim"],
        ["Inventário das ferramentas e uso real", "Sim", "Sim"],
        ["Estrutura organizacional", "Organograma e matriz de responsabilidades", "Organograma atual e proposto, matriz de responsabilidades e descrição de papéis"],
        ["Fluxos otimizados", "Não", "5 processos prioritários"],
        ["Plano de automação", "Lista priorizada, sem estimativa", "Lista priorizada com esforço estimado, base para orçar a implementação"],
        ["Relatório e apresentação executiva", "Sim", "Sim"],
    ], [5.5, 4.5, 6])

    h(d, "5. Fora do escopo desta proposta")
    lista(d, [
        "Desenvolvimento, configuração ou integração de automações e sistemas.",
        "Migração de dados entre sistemas.",
        "Suporte contínuo, plantão ou atendimento de urgência.",
        "Licenças, assinaturas e custos de ferramentas (sempre por conta da cliente).",
        "Consultoria contábil, fiscal, trabalhista ou jurídica sobre o conteúdo das obrigações.",
        "Recrutamento, avaliação de desempenho ou definição de salários.",
    ])

    h(d, "6. Esforço estimado")
    par(d, "As horas foram estimadas antes de definir o preço. Premissas: 2 h por entrevista (1 h de conversa e "
           "1 h de preparação e registro), 2 h por processo mapeado, 2 h por processo redesenhado e 20% de contingência.")
    tabela(d, ["Atividade", "Essencial", "Completa"], [
        ["Entrevistas com a equipe", "8", "10"],
        ["Mapeamento dos processos atuais", "10", "16"],
        ["Gargalos e dependências", "3", "4"],
        ["Validação com a Thamires", "2", "2,5"],
        ["Estrutura organizacional", "6", "14"],
        ["Fluxos otimizados", "-", "10"],
        ["Plano de automação", "2", "5"],
        ["Relatório e apresentação executiva", "3", "6"],
        ["Contingência (20%)", "7", "13,5"],
        ["**Total**", "**~41 h**", "**~81 h**"],
    ], [9, 3.5, 3.5])

    h(d, "7. Investimento")
    tabela(d, ["Opção", "Investimento", "Pagamento"], [
        ["**Essencial**", "**R$ 7.800**", "50% no aceite, 50% na entrega"],
        ["**Completa (recomendada)**", "**R$ 14.800**", "30% no aceite, 35% na entrega do mapeamento, 35% na entrega final"],
        ["Hora avulsa (fora do escopo, sob aprovação prévia)", "R$ 220/h", "Mensal, conforme horas aprovadas"],
    ], [6, 4, 6])
    par(d, "A reunião inicial de 2h30 e a preparação desta proposta não são cobradas.")
    par(d, "Referência para a etapa seguinte (não contratada agora): a implementação será orçada em pacotes de "
           "preço fechado, de acordo com o plano de automação. Como ordem de grandeza, pacotes pequenos ficam "
           "entre R$ 1.500 e R$ 2.800 e pacotes médios entre R$ 3.500 e R$ 6.500. O acompanhamento mensal, se "
           "desejado, parte de R$ 900 por mês com franquia de 4 horas.")
    par(d, "Despesas de deslocamento, se houver encontros presenciais, e custos de ferramentas são repassados à parte, "
           "mediante aprovação.")

    h(d, "8. Cronograma")
    par(d, "O consultor dedica cerca de 10 horas por semana ao projeto, fora do horário comercial. Os prazos "
           "contam a partir do aceite e dependem da disponibilidade da equipe para entrevistas e validações. "
           "Essencial: 4 a 5 semanas. Completa: 8 a 9 semanas.")
    tabela(d, ["Semana (Completa)", "Atividades", "Marco"], [
        ["1", "Kick-off, agendamento e início das entrevistas", "Kick-off com a Thamires"],
        ["2 e 3", "Entrevistas, inventário de ferramentas e mapeamento dos processos atuais", ""],
        ["4", "Validação dos fluxos, gargalos e dependências", "Entrega do mapeamento"],
        ["5 e 6", "Estrutura organizacional: organogramas, papéis e matriz de responsabilidades", ""],
        ["7 e 8", "Fluxos otimizados e plano de automação com esforço estimado", ""],
        ["9", "Relatório final e apresentação executiva", "Entrega final e proposta de implementação"],
    ], [3, 8, 5])
    par(d, "Na opção Essencial, as semanas 1 a 4 se mantêm e a semana 5 concentra estrutura organizacional, "
           "plano de automação e apresentação.")
    h(d, "9. Responsabilidades")
    h(d, "Do consultor", 3)
    lista(d, [
        "Conduzir entrevistas, análises e reuniões nas datas combinadas.",
        "Entregar os documentos descritos em cada etapa, em formato editável.",
        "Manter sigilo absoluto sobre dados da empresa e de seus clientes, com acordo de confidencialidade.",
        "Avisar com antecedência qualquer risco de atraso ou necessidade de mudança de escopo.",
        "Responder mensagens em até 1 dia útil.",
    ])
    h(d, "Da cliente", 3)
    lista(d, [
        "Indicar um ponto focal e liberar a equipe para entrevistas de cerca de 1 hora, de preferência antes das 10h, no almoço ou após 19h30.",
        "Disponibilizar exemplos de documentos, planilhas e acessos de consulta necessários, com dados protegidos quando possível.",
        "Responder dúvidas em até 2 dias úteis e validar entregas em até 5 dias úteis após o envio.",
        "Tomar as decisões de priorização ao final de cada etapa.",
        "Arcar com licenças e ferramentas que decidir adotar.",
    ])

    h(d, "10. Condições gerais")
    lista(d, [
        "Reuniões em janelas fora do horário comercial do consultor: antes das 10h, no almoço ou após 19h30, preferencialmente online.",
        "Atrasos causados por falta de retorno ou de acesso deslocam o cronograma pelo mesmo período.",
        "Mudanças de escopo são orçadas à parte e só executadas após aprovação por escrito.",
        "Pausas de mais de 10 dias por parte da cliente reagendam o cronograma.",
        "Os documentos produzidos passam a ser da cliente após a quitação da etapa correspondente.",
        "Validade desta proposta: 15 dias a partir de 15/10/2026.",
    ])

    h(d, "11. Próximos passos")
    lista(d, [
        "Escolha da opção (Essencial ou Completa) e aceite da proposta.",
        "Assinatura do acordo de confidencialidade.",
        "Agendamento do kick-off e das entrevistas com a equipe.",
    ], numerada=True)
    par(d, "\nRenato [sobrenome] · Consultor · [e-mail] · [telefone]")
    d.save(f"{SAIDA}/04-proposta-comercial.docx")


# ---------------------------------------------------------------------------
# 05 · Roteiro da apresentação + pendências do Renato
# ---------------------------------------------------------------------------
def roteiro():
    d = novo_doc("Roteiro da apresentação e decisões pendentes",
                 "Preparação para quinta-feira, 15/10/2026 · documento interno do Renato")

    h(d, "1. Decisões e revisões que só você pode fazer")
    tabela(d, ["#", "Decisão", "Padrão adotado nos documentos"], [
        ["1", "Taxa-piso da sua hora", "R$ 180/h para cálculo; R$ 220/h para hora avulsa"],
        ["2", "Capacidade semanal sustentável", "10 h/semana, com 20% de contingência"],
        ["3", "Cobrar ou não pela reunião de 2h30 já feita", "Não cobrada; entra como Etapa 0 (investimento comercial)"],
        ["4", "Preço das duas opções", "Essencial R$ 7.800 (~41 h); Completa R$ 14.800 (~81 h)"],
        ["5", "Limites de processos", "Essencial até 5; Completa até 8, com 5 redesenhados"],
        ["6", "Limites de entrevistas", "Essencial até 4 pessoas; Completa até 5 (depende do tamanho da equipe)"],
        ["7", "Sua forma de faturar (MEI, PJ, RPA)", "Não citada na proposta; impostos de 6% a 15% a reservar"],
        ["8", "Cláusula de exclusividade no seu emprego atual", "Verificar antes de assinar"],
        ["9", "Seu sobrenome, e-mail e telefone na proposta", "[PREENCHER]"],
        ["10", "Grafia do nome da empresa (Surcin ou Sourcin)", "Surcin"],
    ], [0.8, 7, 8.2])

    h(d, "2. Plano para os dois dias de preparação")
    tabela(d, ["Quando", "O que fazer", "Tempo"], [
        ["Terça 13/10 · noite", "Ouvir a gravação ou ler a transcrição com o doc 01 aberto, preenchendo as dores e os [PREENCHER]", "2 a 3 h"],
        ["Quarta 14/10 · manhã", "Revisar a estrutura organizacional (doc 02) com o que ouviu; cortar o que não se aplica", "1 h"],
        ["Quarta 14/10 · noite", "Fechar decisões da tabela acima, ajustar valores da proposta (doc 04) e ensaiar a apresentação", "2 a 3 h"],
        ["Quinta 15/10", "Apresentar; levar a lista de perguntas do doc 01 impressa ou aberta", "1 h"],
    ], [3.5, 10, 2.5])
    par(d, "Se a transcrição não chegar a tempo: apresente o modelo como está, diga que as dores serão "
           "confirmadas na Etapa 1 e use a reunião de quinta para fazer as perguntas da seção 6 do doc 01.")

    h(d, "3. Roteiro da apresentação (cerca de 40 minutos)")
    slides = [
        ("1. Abertura (2 min). ", "Agradecer a reunião de 2h30 e dizer que ela já é o início do diagnóstico."),
        ("2. O que eu entendi (8 min). ", "Áreas, ferramentas e as 3 dores principais nas palavras dela. Pedir que corrija."),
        ("3. Como vamos trabalhar (5 min). ", "Etapas 0 a 4 em uma linha cada. Reforçar: entender antes de automatizar."),
        ("4. Estrutura organizacional (7 min). ", "Mostrar o organograma de referência como exemplo de entregável e pedir que ela preencha os nomes."),
        ("5. Mapeamento de processos (5 min). ", "Explicar o método em 4 passos: ouvir a equipe, desenhar, encontrar gargalos, otimizar."),
        ("6. Entregáveis e cronograma (5 min). ", "Essencial em 4 a 5 semanas; Completa em 8 a 9, com marco na semana 4."),
        ("7. Investimento (5 min). ", "Essencial e Completa lado a lado; recomendar a Completa. Implementação orçada depois, por pacotes."),
        ("8. Próximos passos e perguntas (3 min+). ", "Aceite, confidencialidade, agenda de entrevistas. Fazer as perguntas pendentes."),
    ]
    lista(d, slides)

    h(d, "4. Possíveis objeções e respostas")
    tabela(d, ["Se ela disser", "Resposta sugerida"], [
        ["Já contei tudo na reunião, por que mais diagnóstico?",
         "A reunião deu a visão da dona. Falta a visão de quem executa, que é onde estão os detalhes que fazem uma automação funcionar ou falhar."],
        ["Quero logo as automações.",
         "Automatizar um processo desorganizado só acelera o problema. A opção Completa entrega o plano de automação com esforço estimado; a primeira automação pode começar logo depois."],
        ["Está caro.",
         "Ela pode começar pela Essencial e ampliar depois. A reunião inicial e a proposta não foram cobradas."],
        ["Por que demora 8 a 9 semanas?",
         "O ritmo respeita a rotina da equipe para entrevistas e validações; dá para reduzir se a equipe tiver mais disponibilidade."],
    ], [5.5, 10.5])
    d.save(f"{SAIDA}/05-roteiro-apresentacao-e-decisoes.docx")


if __name__ == "__main__":
    diagnostico()
    estrutura()
    metodologia()
    proposta()
    roteiro()
    print("ok")
