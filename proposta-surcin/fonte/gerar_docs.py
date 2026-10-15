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
VERSAO = "Versão 4 · 13/10/2026 · dados reconferidos com a transcrição · uso interno até revisão do Renato"


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
    rodape.text = "Surcin Assessoria Empresarial · Proposta de consultoria · Confidencial"
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


LEGENDA = ("Legenda: [REUNIÃO] dito pela Thamires em 12/10/2026 (minuto da gravação entre parênteses); "
           "[BRIEFING] relatório de briefing que a Surcin enviou ao consultor; [HIPÓTESE] leitura do consultor; "
           "[DIVERGÊNCIA] as fontes discordam (ver seção 8). Quando as fontes discordam, vale a reunião.")

CONSULTOR = "Renato Romão · Consultor responsável · R2 Tech Consultoria · r2techconsultoria@gmail.com · [telefone]"


# ---------------------------------------------------------------------------
# 01 · Diagnóstico preliminar
# ---------------------------------------------------------------------------
def diagnostico():
    d = novo_doc("Diagnóstico preliminar", "Surcin Assessoria Empresarial · leitura da reunião de 12/10/2026 e do briefing")
    aviso(d, "Fontes, por ordem de prioridade: (1) transcrição automática da reunião de 12/10/2026, 2h38; "
             "(2) \"Briefing para proposta de consultoria e implantação\", 14 páginas, enviado pela Surcin; "
             "(3) anotações automáticas do Gemini sobre a reunião. As divergências estão registradas na seção 8. "
             "Nada aqui foi acrescentado além do que as fontes dizem.")
    par(d, LEGENDA, italico=True)

    h(d, "1. Resumo executivo")
    par(d, "A Surcin é uma assessoria empresarial pequena que já tem processos desenhados, mas ainda depende da "
           "Thamires como fonte de conhecimento, decisão e revisão. Depois de uma quebra causada por crescer sem "
           "estrutura, ela reconstruiu a operação com passo a passos, checklists e rotinas no Trello, "
           "e recuperou cerca de 90% dos clientes (00:06 a 00:11; o ano da reconstrução está na seção 8).")
    par(d, "O gargalo atual não é falta de processo, é falta de eficiência, de controle e de autonomia. Em 2026 os "
           "sistemas novos (Domínio, Veri, Conta Azul) não foram implantados de fato, e um erro de parametrização de "
           "ISS gerou imposto pago errado, retificações, multa, um impacto de cerca de R$ 10 mil e a perda de um "
           "cliente (00:26 a 00:29; briefing, seção 4.1). Desde a saída da responsável pelo fiscal, em agosto, a "
           "Thamires executa o fiscal pessoalmente.")
    par(d, "Há prazo pessoal e financeiro: prova de certificação em 13/12/2026, caixa garantido por um Pronampe até "
           "novembro e a meta de entrar em janeiro com a operação estável para retomar vendas e reavaliar contratações "
           "(00:31 a 00:37, 02:14; briefing, seção 1).")
    par(d, "Frase dela: \"Hoje eu sinto que eu tenho um processo. Esse processo ele só não tá eficiente. Se eu "
           "melhorar isso, eu consigo escalar com as mesmas pessoas.\" (01:14)", italico=True)

    h(d, "2. A empresa")
    tabela(d, ["Item", "O que as fontes dizem", "Fonte"], [
        ["Fundação", "Constituída em 2021; dedicação integral da Thamires desde janeiro de 2023; atuação remota", "[BRIEFING] seção 2"],
        ["Serviços", "Contabilidade, apurações fiscais, DP/eSocial, financeiro (gestão financeira dos clientes), abertura/alteração/baixa de empresas, regularizações, MEI, IRPF, parcelamentos, contratos e jurídico empresarial; revenda de certificado digital", "[BRIEFING] seção 2; [REUNIÃO] 00:52"],
        ["Proposta de valor", "Gestão do empresário de ponta a ponta: contabilidade, financeiro e jurídico consultivo", "[REUNIÃO] 00:05"],
        ["Estratégia de longo prazo", "Especialização gradual no segmento pet/veterinário, sem abandonar os demais", "[BRIEFING] seção 2"],
        ["Estrutura societária", "Três CNPJs: contabilidade, financeiro e jurídico", "[REUNIÃO] 01:02"],
        ["Carteira fiscal/contábil", "Cerca de 40 a 45 empresas; o fiscal do mês passado cobriu 44", "[REUNIÃO] 01:55, 02:00; [BRIEFING] seção 3"],
        ["Clientes do financeiro", "A Vitória cuida de 12 clientes (00:38). Na contagem do Trello ela citou 11, 13 e 16, este último incluindo as três empresas dela (01:02). Número exato a confirmar", "[REUNIÃO] 00:38, 01:02"],
        ["Departamento Pessoal", "Cerca de 25 vidas, em 4 ou 5 clientes com funcionários", "[REUNIÃO] 00:40"],
        ["Jurídico", "Cerca de 20 processos legados em fase final; contratos e societário; sem receita recorrente hoje", "[REUNIÃO] 00:43, 01:45"],
        ["Situação financeira", "Pronampe garante caixa até novembro; dezembro apertado; pagamento começa em fevereiro", "[REUNIÃO] 00:31, 01:33"],
        ["Decisões já tomadas", "Sem contratações até o fim do ano; tráfego pago pausado (valor investido em anúncios a confirmar); social media mantida; conciliação semanal; comunicação com clientes de contabilidade só pelo aplicativo da Veri a partir de novembro", "[REUNIÃO] 00:30, 01:16, 01:31, 02:12"],
    ], [3.3, 9.7, 3])

    h(d, "3. Pessoas")
    tabela(d, ["Pessoa", "Função", "Observações", "Fonte"], [
        ["Thamires", "Direção, clientes, jurídico, societário, análises financeiras, reuniões de fechamento e, desde agosto, execução do fiscal", "Precisa reduzir o envolvimento operacional para estudar", "00:18, 00:30; briefing 5"],
        ["Júlia", "Secretaria e atendimento: WhatsApp (Nestzap), agenda, documentos no OneDrive, Trello, propostas e contratos, implantação de clientes, apoio no fiscal e no societário", "Braço direito; candidata a supervisora em 2027, condicionado a graduação", "00:15 a 00:19, 01:04; briefing 5"],
        ["Vitória", "Financeiro: pagamentos (terças e sextas), notas, conciliação no Conta Azul, preparação dos fechamentos", "Férias em outubro, retorno em 28/10; a partir de novembro assume o financeiro integralmente", "00:13, 01:34; briefing 5"],
        ["Tamara", "Em outubro acumula DP, conciliação e notas; a partir de novembro, DP", "[DIVERGÊNCIA] sobre as notas a partir de novembro (seção 8)", "00:41; briefing 5"],
        ["Alana", "Estagiária do jurídico e do societário, dois dias por semana, paga por hora", "Permanência em reavaliação", "00:42, 01:40, 02:18"],
        ["Apoio externo", "Social media e gestora de tráfego", "Social media mantida; campanhas de tráfego canceladas", "00:37, 02:12"],
    ], [2.3, 6.2, 5, 2.5])
    par(d, "Saída recente: Dani, que cuidava da contabilidade e do fiscal e emitia notas, saiu depois do erro de agosto. "
           "A Thamires absorveu o setor e hoje não há ninguém na contabilidade (00:30, 00:40, 02:00).")

    h(d, "4. Ferramentas e uso real")
    tabela(d, ["Ferramenta", "Uso atual", "Fonte"], [
        ["Trello", "Rotinas diárias e mensais por pessoa, pendências, checklists de novo cliente e abertura de empresa. Não comprova sozinho que a tarefa foi feita corretamente", "01:03 a 01:07; briefing 4.3"],
        ["OneDrive / Microsoft 365", "Repositório oficial: pastas por frente de serviço e por cliente, passo a passos e modelos", "00:52 a 00:54; briefing 6"],
        ["Google Agenda", "Agenda central da operação, controlada pela Júlia", "00:51"],
        ["WhatsApp + Nestzap", "Número único com vários usuários; entrada de demandas e grupos com clientes", "01:54; briefing 6"],
        ["Veri", "Aplicativo do cliente (guias, certidões, documentos) e modelos de contrato; adoção real a confirmar", "01:15 a 01:17; briefing 6"],
        ["Domínio", "Contábil, fiscal e folha. Parametrização com erro desde a migração; o fiscal está sendo feito direto no portal da Receita", "01:17; briefing 6"],
        ["CITAX", "Em avaliação para captura e apuração fiscal", "briefing 6"],
        ["Conta Azul", "Dados financeiros dos clientes do financeiro, conciliação; emissão de nota pela conciliação não configurada", "00:40, 01:20; briefing 6"],
        ["Jusbrasil", "IA jurídica e modelos; monitoramento de processos não configurado", "01:43"],
        ["Canva e PowerPoint", "Propostas comerciais (Canva) e apresentações de fechamento mensal (PowerPoint)", "01:22; briefing 6"],
        ["Claude e Lovable", "Testes da Thamires no fechamento financeiro (5 h no primeiro, 1 a 2 h nos últimos), em conta ligada ao e-mail antigo (RT). Plano: ambiente novo da Surcin (Claude Team)", "00:33, 00:59; briefing 12"],
    ], [3.3, 10.2, 2.5])

    h(d, "5. Processos identificados")
    tabela(d, ["#", "Processo", "Quem executa", "Situação"], [
        ["1", "Atendimento e triagem de demandas (WhatsApp, Nestzap, Veri)", "Júlia", "Pedidos podem se perder em grupos e planilhas"],
        ["2", "Comercial: primeiro atendimento, proposta, reunião, contrato", "Júlia e Thamires", "Checklist e modelos prontos; retomada em 2027"],
        ["3", "Implantação de novo cliente (contábil e financeiro)", "Júlia e Vitória", "Checklists prontos, a atualizar"],
        ["4", "Abertura, alteração e baixa de empresas", "Júlia, Alana, Thamires", "Checklist no Trello; abertura em Campinas gravada, sem refinar"],
        ["5", "Fiscal mensal: captura, conferência de cadastro e tributação, apuração, guia, envio, evidência", "Thamires e Júlia", "Maior risco: erros de parâmetro (ISS, regime, Fator R)"],
        ["6", "Pedidos de pagamento e pagamentos dos clientes do financeiro", "Vitória", "Pedidos chegam por WhatsApp; risco de guia do cliente errado"],
        ["7", "Emissão de notas fiscais", "Tamara e Vitória", "Feita por fora do Conta Azul"],
        ["8", "Conciliação e fechamento mensal com reunião de resultado", "Vitória e Thamires", "Conciliação passando a semanal; mais de 10 reuniões na semana do fechamento; promessa de formato mais interativo"],
        ["9", "Folha, admissões, rescisões, eSocial", "Tamara", "Volume baixo; pendências antigas"],
        ["10", "Acompanhamento de processos jurídicos", "Alana e Thamires", "Revisão manual"],
        ["11", "Rotinas transversais: EFD-Reinf, IRPF, parcelamentos", "A definir", "Citadas no briefing"],
    ], [0.8, 6.4, 3.3, 5.5])

    h(d, "6. Dores e riscos")
    tabela(d, ["Dor ou risco", "Área", "Fonte"], [
        ["\"Tudo tá centralizado em mim. Eu não tenho o direito de ficar doente.\" Dúvidas e revisões sobem para a Thamires", "Gestão", "00:18; briefing 4.3"],
        ["ISS tratado como devido a outro município por várias competências: retificações, impacto de cerca de R$ 10 mil (guia de cerca de R$ 5 mil numa etapa) e cliente perdido", "Fiscal", "00:26 a 00:29; briefing 4.1"],
        ["Cadastro municipal como regime normal em vez de Simples; nutricionistas com Anexo/Fator R inadequado; DCTF sem movimento não transmitidas; taxas municipais esquecidas", "Fiscal", "briefing 4.1"],
        ["Guia de um cliente salva na pasta de outro, encontrada pelo Financeiro na hora de pagar", "Documentos e pagamentos", "briefing 4.2"],
        ["Trello marcado como concluído sem documento, ou documento sem cartão atualizado", "Controle", "briefing 4.3"],
        ["Fechamento financeiro concentrado no fim do mês e reuniões de resultado atrasadas", "Financeiro", "01:31"],
        ["Escalar sem contratar: a Vitória atende 12 clientes; a Thamires fala em 20 (00:38) e em dobrar \"de 15 para 30\" (01:25)", "Financeiro", "00:38, 01:25"],
        ["Avaliar desempenho individual e criar premiação por pontos, com revisão trabalhista", "Pessoas", "00:46, 02:21; briefing 10"],
        ["Ter tempo para estudar até 13/12", "Direção", "00:36; briefing 1"],
    ], [10, 3, 3])

    h(d, "7. O que a Surcin pediu ao consultor (briefing)")
    lista(d, [
        "Proposta modular que separe consultoria, implantação, desenvolvimento, integrações, licenças e manutenção, com valores e responsabilidades separados (seção 14).",
        "Diagnóstico com fluxos atual e futuro e lista de casos de uso priorizada por valor, risco, esforço e dependência externa.",
        "Ganhos já em outubro e novembro, sem consumir horas diárias da diretora e sem interromper as entregas correntes (seções 12 e 17).",
        "Controles de segurança: aprovação humana, matriz de autonomia (verde, amarelo, vermelho), LGPD, propriedade dos ativos pela Surcin e continuidade sem o consultor (seções 11 e 14).",
        "Estimativa do custo mensal recorrente de ferramentas e plano de contingência.",
        "Respostas às perguntas da seção 16 (respondidas na proposta comercial).",
        "Comercial e CRM só a partir de janeiro de 2027.",
    ])

    h(d, "8. Divergências entre as fontes")
    tabela(d, ["Tema", "Reunião (prevalece)", "Outra fonte", "Como tratamos"], [
        ["Tamara a partir de novembro", "\"Vai ficar exclusiva com o departamento pessoal\" (00:41)", "Briefing: DP e emissão de notas dos clientes contábeis", "Usamos só DP; confirmar quem emite notas"],
        ["Retomada do tráfego pago", "Combinado começar em 15/12 para colher em janeiro (02:16)", "Briefing: retomada em janeiro de 2027. Gemini: \"pausar em dezembro\"", "Usamos 15/12; confirmar"],
        ["Contratação", "\"Provavelmente eu vou contratar um contador\" em janeiro (00:32, 01:49)", "Briefing: reavaliar em janeiro caso a distribuição não funcione", "Tratada como decisão em aberto"],
        ["Novo domínio", "Contas novas no domínio da Surcin (00:59, 02:10)", "Gemini: \"novo domínio RT\". Briefing: RT é a conta antiga", "Gemini errou; novo ambiente é Surcin"],
        ["Fiscal feito pela Thamires", "44 clientes em 3 dias, 3 a 4 horas por dia (02:00)", "Gemini: \"3 horas fracionadas\"", "Vale a reunião"],
        ["Tempo do fechamento com IA", "De 5 h para 1 a 2 h (00:34)", "Gemini: 1 h 30", "Usamos 1 a 2 h"],
        ["Clientes do financeiro", "12 (00:38); 11, 13 e 16 na contagem do Trello (01:02); \"de 15 para 30\" (01:25)", "Briefing: 14 a 15", "Usamos \"cerca de 12 a 16\"; confirmar"],
        ["Ano da quebra e da reconstrução", "Ambígua: \"no final de 2023, eu quebrei\" (00:06) e \"em 2023 foi o ano que eu comecei a me reconstruir\" (00:11)", "Briefing: quebra no fim de 2023, reconstrução em 2024. Gemini: quebra no fim de 2023", "Não citamos ano nos documentos; confirmar"],
    ], [2.6, 4.8, 4.8, 3.8])

    h(d, "9. Leitura do consultor")
    lista(d, [
        ("[HIPÓTESE] O ponto de partida é bom. ", "Há documentação, padrão de pastas e rotinas no Trello; o mapeamento parte do que existe."),
        ("[HIPÓTESE] O maior risco está nos parâmetros fiscais. ", "Sistemas apuram certo com parâmetro errado. Separar execução de conferência e corrigir a parametrização do Domínio (com o suporte do sistema) vem antes de qualquer automação."),
        ("[HIPÓTESE] Três controles manuais já reduzem risco antes da prova. ", "Conferência de guia antes de pagar, evidência obrigatória para concluir cartão e registro das dúvidas que chegam à Thamires. Não exigem desenvolvimento."),
        ("[HIPÓTESE] A Júlia é ponto único de falha. ", "Ela recebe, distribui e acompanha tudo; precisa de papel formal e substituto."),
        ("[HIPÓTESE] A premiação depende de papéis claros. ", "Sem função e entregas medíveis, o programa vira discussão; e não deve premiar volume de cartões (briefing, seção 10)."),
        ("[HIPÓTESE] A capacidade do consultor limita o que cabe antes de 13/12. ", "Com cerca de 10 h por semana, cabe mapear, estruturar e implantar controles manuais. Pilotos de software ficam para janeiro, salvo troca de escopo."),
    ])

    h(d, "10. Perguntas para quinta-feira")
    blocos = {
        "Confirmar divergências": [
            "Quantos clientes o financeiro atende hoje, sem contar as três empresas da Thamires?",
            "A partir de novembro, quem emite as notas dos clientes contábeis: Tamara ou Vitória?",
            "O tráfego pago volta em 15/12 ou em janeiro?",
            "A contratação de um(a) contador(a) em janeiro está decidida ou depende do teste de novembro e dezembro?",
        ],
        "Prioridades e agenda": [
            "Qual processo, resolvido primeiro, mais devolve seu tempo: fiscal, fechamento financeiro ou implantação de clientes?",
            "A equipe pode participar de entrevistas no início do expediente, antes das 10h, ou após as 19h30?",
            "A Júlia pode ser a ponto focal do projeto?",
        ],
        "Sistemas": [
            "Quem vai corrigir a parametrização do Domínio, e até quando? O CITAX entra nessa decisão?",
            "Quando o ambiente novo da Surcin (e-mail, Claude, Lovable) será criado e por quem?",
        ],
        "Investimento": [
            "Qual faixa de investimento cabe agora, considerando o caixa até dezembro?",
            "Há orçamento separado para licenças (Claude Team, Lovable, API de WhatsApp)?",
        ],
    }
    for titulo, perguntas in blocos.items():
        h(d, titulo, 3)
        lista(d, perguntas)

    h(d, "11. Materiais")
    lista(d, [
        "Recebidos: transcrição da reunião, briefing de 14 páginas e anotações do Gemini.",
        "Pendentes: gravação e apresentação usada na reunião (02:36); acesso de leitura ao Trello e à pasta Geral do OneDrive, via Júlia (02:09).",
    ])
    d.save(f"{SAIDA}/01-diagnostico-preliminar.docx")


# ---------------------------------------------------------------------------
# 02 · Estrutura organizacional
# ---------------------------------------------------------------------------
def org_bloco(d, linhas):
    for linha in linhas:
        p = d.add_paragraph()
        r = p.add_run(linha)
        r.font.name = "Consolas"
        r.font.size = Pt(10)
        p.paragraph_format.space_after = Pt(0)
    d.add_paragraph()


def estrutura():
    d = novo_doc("Estrutura organizacional", "Estrutura atual e hipótese de estrutura proposta · para validação")
    aviso(d, "A estrutura atual vem do que a Thamires descreveu em 12/10/2026. A estrutura proposta reúne as ideias "
             "discutidas na reunião e é uma hipótese: a versão recomendada sai depois das entrevistas com a equipe "
             "(Etapa 2 da proposta).\n\nNenhuma contratação, desligamento ou mudança definitiva de função é recomendada nesta fase. "
             "Os itens marcados [decisão dela] são intenções que a própria Thamires citou na reunião ou no briefing; "
             "só serão avaliados depois de comparar responsabilidades, volume de trabalho, competências e disponibilidade.")

    h(d, "1. Estrutura atual (como é)")
    org_bloco(d, [
        "Thamires · direção, técnica contábil e jurídica, fiscal, comercial, reuniões de fechamento",
        "    ├── Júlia · secretária: atendimento, implantação de clientes, apoio no fiscal",
        "    ├── Vitória · financeiro: pagamentos, notas, conciliação, preparação do fechamento",
        "    ├── Tamara · DP + apoio no financeiro e notas (só DP a partir de novembro)",
        "    └── Alana · estagiária do jurídico (quarta e sexta)",
    ])
    par(d, "Pontos de atenção que ela mesma levantou:")
    lista(d, [
        "Contabilidade e fiscal executados pela Thamires desde a saída da Dani, em agosto.",
        "Todas as dúvidas e revisões sobem para a Thamires.",
        "A Júlia acumula atendimento, distribuição de demandas, implantação, comercial e parte do fiscal.",
        "A Tamara alterna entre três áreas diferentes (até outubro).",
        "O jurídico consome revisão da Thamires e não gera receita recorrente.",
    ])

    h(d, "2. Hipótese de estrutura proposta (como poderia ser)")
    par(d, "Desenho discutido na reunião (01:38 a 01:51), organizado por fluxo do cliente: entrada, operação e revisão técnica.")
    org_bloco(d, [
        "Thamires · direção, estratégia, relacionamento com clientes-chave, jurídico consultivo",
        "    ├── Revisão técnica contábil · contador(a) que ela pensa contratar em 2027 [decisão dela]",
        "    │       └── Contabilidade e fiscal (operação)",
        "    ├── Entrada e relacionamento · Júlia",
        "    │       comercial, implantação de clientes, atendimento e triagem",
        "    ├── Financeiro · Vitória",
        "    ├── Departamento Pessoal · Tamara [avaliar se absorve apoio ao societário]",
        "    └── Jurídico · processos legados [decisão dela: ela citou absorver com o monitoramento do Jusbrasil]",
    ])
    par(d, "Racional: a área que mais cresce com novos clientes é a de entrada e suporte, não a operação; Vitória e "
           "Tamara podem atender mais clientes com processos claros; a revisão técnica deixa de depender da "
           "Thamires quando houver um(a) contador(a) sênior (01:38 a 01:40, 02:04).", italico=True)

    h(d, "3. Papéis e responsabilidades (proposta inicial)")
    tabela(d, ["Papel", "Missão", "Responsabilidades principais", "Entregas que podem virar indicador"], [
        ["Direção (Thamires)", "Definir prioridades e responder tecnicamente", "Decisões de preço e contratação, clientes-chave, aprovação de exceções", "Reuniões de resultado realizadas no prazo"],
        ["Revisão técnica contábil (a contratar)", "Garantir a qualidade técnica da contabilidade e do fiscal", "Revisão das apurações, configuração do Domínio, resposta a dúvidas técnicas", "Obrigações entregues no prazo, sem multa"],
        ["Entrada e relacionamento (Júlia)", "Trazer, implantar e atender clientes", "Primeiro atendimento, proposta, contrato, implantação, triagem das demandas", "Tempo de implantação, demandas distribuídas no dia"],
        ["Financeiro (Vitória)", "Manter o financeiro dos clientes em dia", "Pagamentos, notas, conciliação semanal, preparação do fechamento", "Clientes conciliados até o dia 1º, fechamentos entregues na 1ª semana"],
        ["Departamento Pessoal (Tamara)", "Garantir folha e obrigações trabalhistas", "Folha até o 5º dia útil, admissões, rescisões, pendências antigas", "Folhas no prazo, pendências zeradas"],
        ["Jurídico (Alana ou Thamires)", "Não perder prazos dos processos legados", "Acompanhamento, petições simples, apoio ao societário", "Prazos cumpridos"],
    ], [3.2, 3.5, 5.3, 4])

    h(d, "4. Papéis transversais")
    lista(d, [
        ("Substituto da Júlia na triagem: ", "evita que a entrada de demandas pare quando ela não está."),
        ("Dono de cada processo: ", "uma pessoa responde pelo resultado de ponta a ponta, mesmo que outras executem partes."),
        ("Responsável por ferramentas e acessos: ", "Trello, OneDrive, migração para o novo domínio, licenças de IA."),
        ("Guardião de dados (LGPD): ", "controla acesso a dados pessoais da folha e a documentos sigilosos."),
    ])

    h(d, "5. Matriz de responsabilidades (exemplo com os processos reais)")
    par(d, "R = executa · A = aprova e responde · C = é consultado · I = é informado. A matriz final sai das entrevistas.")
    tabela(d, ["Processo", "Thamires", "Júlia", "Vitória", "Tamara", "Revisor contábil"], [
        ["Implantação de novo cliente", "I", "R/A", "C", "C", "C"],
        ["Fiscal mensal e envio das guias", "A (hoje R)", "R (envio)", "-", "-", "R (futuro)"],
        ["Conciliação e fechamento financeiro", "A (reunião)", "I", "R", "-", "-"],
        ["Emissão de notas", "I", "I", "R/A", "C", "-"],
        ["Folha mensal", "I", "I", "-", "R/A", "C"],
        ["Proposta a novo cliente", "A", "R", "C", "C", "-"],
    ], [5, 2.2, 2, 2, 2, 2.8])

    h(d, "6. Ligação com a remuneração variável")
    par(d, "A Thamires quer um programa de pontos por produtividade (00:46, 02:21). A estrutura entrega a base que ele "
           "precisa: papéis, entregas e indicadores por função. O desenho da avaliação por competência está orçado como "
           "parte da opção Completa na proposta comercial (seções 4 e 9); pesos, metas e valores são decisão dela. O briefing já define critérios: reconhecer qualidade, pontualidade, "
           "autonomia e conformidade, não o volume de cartões concluídos, e passar valores e natureza jurídica por "
           "revisão trabalhista (seção 10).")

    h(d, "7. O que precisamos confirmar nas entrevistas")
    lista(d, [
        "Quanto tempo cada pessoa gasta hoje em cada rotina.",
        "Se a Júlia quer e pode assumir comercial e implantação, e quem a substitui na triagem.",
        "Se a Tamara tem capacidade para apoiar o societário depois de novembro.",
        "O que a Thamires quer manter consigo e o que delega ao(à) futuro(a) contador(a).",
        "O futuro do estágio jurídico.",
    ], numerada=True)

    h(d, "8. Entregável final desta frente")
    lista(d, [
        "Organograma atual e proposto, validados com a Thamires.",
        "Descrição de cada papel: missão, responsabilidades, entregas e indicadores.",
        "Matriz de responsabilidades dos processos principais.",
        "Lista de sobreposições, lacunas e dependências da direção, com plano de transição.",
    ])
    d.save(f"{SAIDA}/02-estrutura-organizacional-hipotese.docx")


# ---------------------------------------------------------------------------
# 03 · Metodologia de mapeamento
# ---------------------------------------------------------------------------
def metodologia():
    d = novo_doc("Metodologia de mapeamento de processos",
                 "Como vamos levantar fluxos, gargalos e dependências e propor melhorias e automações")

    h(d, "1. Princípios")
    lista(d, [
        ("Partir do que já existe. ", "A Surcin já tem passo a passos, checklists e rotinas no Trello. O mapeamento começa por eles, e as entrevistas confirmam o que acontece de fato."),
        ("Entender antes de automatizar. ", "Nenhuma automação é proposta antes de o processo atual estar desenhado e validado por quem executa."),
        ("Ouvir quem faz. ", "A Thamires conhece o negócio; Júlia, Vitória e Tamara conhecem os detalhes do dia a dia."),
        ("Respeitar a agenda. ", "Nada de entrevistas na primeira semana do mês (fechamentos) nem perto do dia 20 (impostos); conversas curtas, de cerca de 1 hora."),
        ("Sigilo e LGPD. ", "Documentos de clientes vistos só como exemplo, com acesso mínimo e acordo de confidencialidade."),
    ])

    h(d, "2. Etapas do método")
    lista(d, [
        ("A · Coleta do que existe. ", "Passo a passos da pasta Geral, quadros do Trello, checklists, planilha de cadastro de clientes e gravações de processos."),
        ("B · Inventário e priorização. ", "Lista dos 11 processos identificados (seção 3), pontuados de 1 a 5 em dor, volume, risco (multa, erro, sigilo) e facilidade de melhoria."),
        ("C · Entrevistas com executores. ", "Roteiro da seção 4, uma conversa por pessoa, acompanhando a tarefa sendo feita sempre que possível."),
        ("D · Fluxo atual (AS-IS). ", "Diagrama em raias (uma por pessoa ou área), com passos, decisões, sistemas e esperas, salvo no OneDrive da Surcin."),
        ("E · Validação. ", "Revisão com quem executa e com a Thamires."),
        ("F · Gargalos e dependências. ", "Esperas, retrabalho, digitação duplicada, revisões concentradas na Thamires e pontos únicos de falha, em uma matriz pessoa × pessoa."),
        ("G · Fluxo otimizado (TO-BE). ", "Primeiro simplificar e configurar o que as ferramentas já fazem; depois automatizar."),
        ("H · Plano de automação. ", "Lista priorizada, com esforço estimado em pacotes e indicação de quem usa cada ferramenta de IA e a que custo."),
    ])

    h(d, "3. Processos identificados e prioridade inicial")
    tabela(d, ["Processo", "Dor", "Volume", "Risco", "Prioridade inicial [HIPÓTESE]"], [
        ["Fiscal mensal", "Alta", "44 clientes/mês", "Alto (multa)", "1"],
        ["Conciliação e fechamento financeiro", "Alta", "12 a 16 clientes/mês", "Médio", "1"],
        ["Implantação de novo cliente (contábil e financeiro)", "Média", "Cresce com vendas", "Médio", "2"],
        ["Atendimento e triagem de demandas", "Alta", "Diário", "Médio", "2"],
        ["Emissão de notas", "Média", "Recorrente", "Médio", "2"],
        ["Pagamentos dos clientes do financeiro", "Média", "2x por semana", "Médio", "3"],
        ["Folha e DP", "Baixa", "25 vidas", "Médio", "3"],
        ["Comercial (lead a contrato)", "Média", "Baixo agora", "Baixo", "3"],
        ["Abertura de empresa", "Baixa", "Eventual", "Médio", "3"],
        ["Acompanhamento de processos jurídicos", "Baixa", "20 processos", "Alto (prazos)", "3"],
        ["EFD-Reinf, IRPF e parcelamentos", "Baixa", "Anual e mensal", "Médio", "3"],
        ["Pendências antigas de DP", "Baixa", "Pontual", "Médio", "Fora do mapeamento"],
    ], [5.2, 1.8, 3.2, 2.6, 3.2])

    h(d, "4. Roteiro de entrevista")
    lista(d, [
        "Quais são as suas tarefas em um mês típico? Quais são diárias, semanais e mensais?",
        "Para esta tarefa, o que você precisa receber para começar? De quem e por qual canal?",
        "Quais são os passos, na ordem? Em qual sistema cada passo é feito?",
        "O que você entrega no final, para quem e em que formato?",
        "Quanto tempo leva, em média? E no pior mês?",
        "Onde você costuma esperar por alguém ou por um documento?",
        "O que você digita mais de uma vez em lugares diferentes?",
        "Que dúvidas você leva para a Thamires com mais frequência?",
        "O que dá errado com mais frequência? O que acontece quando dá errado?",
        "Se você pudesse mudar uma coisa nesta tarefa, o que seria?",
    ], numerada=True)

    h(d, "5. Ficha de registro de cada processo")
    tabela(d, ["Campo", "O que registrar"], [
        ["Nome e área", "Ex.: Fiscal mensal · Contabilidade"],
        ["Dono do processo", "Quem responde pelo resultado"],
        ["Gatilho e prazo", "O que inicia o processo e a data-limite (ex.: guias até o dia 20)"],
        ["Insumos", "Documentos e informações, origem e canal (Veri, WhatsApp, portal)"],
        ["Passos e responsáveis", "Sequência, quem faz, em que sistema"],
        ["Saídas", "O que é entregue, para quem, formato e prazo"],
        ["Volume e tempo", "Quantas vezes por mês e quanto tempo por execução"],
        ["Documentação existente", "Passo a passo, checklist do Trello, gravação"],
        ["Problemas", "Esperas, retrabalho, erros, multas, reclamações"],
        ["Dados sensíveis", "Há dados pessoais ou sigilosos? Quem acessa?"],
    ], [4, 12])

    h(d, "6. Sinais de gargalo e tipo de melhoria")
    tabela(d, ["Sinal", "Exemplo da Surcin", "Melhoria provável"], [
        ["Revisão concentrada", "Tudo passa pela Thamires", "Critérios de revisão, papel de revisor técnico, assistente de dúvidas"],
        ["Trabalho acumulado no fim do mês", "Conciliação feita só no fechamento", "Conciliação semanal, calendário de rotinas"],
        ["Recurso da ferramenta não usado", "Nota emitida por fora do Conta Azul; monitoramento do Jusbrasil desligado", "Configuração antes de automação"],
        ["Ponto único de falha", "Júlia na triagem; Thamires no fiscal", "Substituto definido e passo a passo atualizado"],
        ["Instrução repetida", "Prompt do fechamento refeito a cada mês", "Transformar em rotina padronizada (skill) com revisão"],
        ["Comunicação dispersa", "WhatsApp, e-mail e aplicativo da Veri", "Canal único por tipo de demanda"],
        ["Concluído sem evidência", "Cartão do Trello fechado sem comprovante no OneDrive", "Evidência obrigatória e auditoria por amostra"],
        ["Parâmetro errado", "ISS de outro município, regime municipal, Fator R", "Separar execução de conferência; checklist de parâmetros"],
    ], [3.5, 6, 6.5])

    h(d, "7. Critérios para propor uma automação")
    lista(d, [
        "O processo está validado e simplificado.",
        "Há volume ou risco que justifique o esforço (horas economizadas × custo da hora da equipe).",
        "Os sistemas permitem integração (verificado, não suposto); o Domínio só depois de corrigida a configuração.",
        "Existe alguém da equipe responsável por operar e acompanhar a automação.",
        "O custo recorrente de ferramentas (licenças de IA, API do WhatsApp) cabe no orçamento.",
        "O tratamento de dados pessoais está de acordo com a LGPD.",
        "A ação respeita a matriz de autonomia do briefing: verde automático, amarelo com confirmação humana, vermelho (pagar, protocolar, decidir) sempre humano.",
    ])
    d.save(f"{SAIDA}/03-metodologia-mapeamento-processos.docx")


# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 04 · Proposta comercial
# ---------------------------------------------------------------------------
def proposta():
    d = novo_doc("Proposta de consultoria", "Organização, estrutura, processos e plano de automação · Surcin Assessoria Empresarial")
    aviso(d, "Valores calculados com taxa de referência de cerca de R$ 180/h e capacidade de 10 h/semana do "
             "consultor, com 20% de contingência. Aguardam confirmação do Renato antes do envio.")

    h(d, "1. O que entendemos")
    par(d, "A Surcin oferece contabilidade, fiscal, DP, financeiro, societário e jurídico empresarial, com cerca de "
           "40 a 45 empresas na carteira fiscal, cerca de 12 a 16 clientes no financeiro e uma equipe enxuta. A empresa já tem processos "
           "desenhados, padrão de pastas e rotinas no Trello, mas a Thamires continua sendo a fonte única de "
           "conhecimento, decisão e revisão, e os erros recentes vieram de parâmetros fiscais errados e de controles "
           "que dependem de atenção humana.")
    par(d, "O briefing enviado pela Surcin pede uma proposta modular, com entregas verificáveis, que gere ganhos ainda "
           "em outubro e novembro sem consumir o tempo de estudo da Thamires, e que não seja vendida como \"colocar IA "
           "em todos os setores\". Esta proposta segue esse caminho: primeiro processo, controle e estrutura; depois "
           "automação assistida, em módulos orçados um a um.")

    h(d, "2. Objetivos")
    lista(d, [
        "Reduzir já os riscos mais caros (guia do cliente errado, tarefa concluída sem evidência, dúvidas repetidas) com controles que não exigem software.",
        "Tirar a Thamires do centro da operação: papéis claros, critérios de revisão e escalonamento só para exceções.",
        "Tornar visíveis os fluxos, gargalos e dependências entre pessoas e sistemas.",
        "Entregar o plano de automação priorizado por valor, risco, esforço e dependência externa, com custo recorrente estimado.",
        "Preparar a operação para a retomada comercial e para as decisões de contratação de janeiro de 2027.",
    ])

    h(d, "3. O que esta proposta cobre (e o que não cobre)")
    par(d, "O briefing pede que consultoria, implantação, desenvolvimento, integrações, licenças e manutenção fiquem separados.")
    tabela(d, ["Frente", "Situação nesta proposta"], [
        ["Consultoria: diagnóstico, mapeamento, estrutura, plano", "Incluída (Fase 1, preço fechado)"],
        ["Contenção imediata: 3 controles manuais", "Incluída na opção Completa"],
        ["Implantação e desenvolvimento: ambiente Claude, especialistas, validadores, painéis", "Fase 2, módulos orçados à parte após o plano"],
        ["Integrações (Conta Azul, Domínio, Nestzap, OneDrive, Trello)", "Fase 2, cada uma com prova de viabilidade antes de orçar"],
        ["Licenças e ferramentas", "Por conta da Surcin; estimativa mensal entregue no plano"],
        ["Manutenção e suporte", "Fase 3, mensalidade com franquia de horas, opcional"],
    ], [9, 7])

    h(d, "4. Fase 1 · Diagnóstico, estrutura e plano: duas opções")
    tabela(d, ["Entregável", "Essencial", "Completa (recomendada)"], [
        ["Entrevistas (cerca de 1 h cada)", "Até 4 pessoas: Thamires, Júlia, Vitória, Tamara", "Até 5 pessoas (inclui a Alana)"],
        ["Processos atuais mapeados e validados", "Até 5", "Até 8, entre os 11 identificados"],
        ["Gargalos e matriz de dependências", "Sim", "Sim"],
        ["Inventário de ferramentas, contas, licenças e acessos", "Sim", "Sim"],
        ["Contenção imediata: 3 controles manuais implantados com a equipe", "Não", "Sim, até 15/11"],
        ["Estrutura organizacional", "Organograma e matriz de responsabilidades", "Organograma atual e proposto, descrição de papéis e indicadores por função"],
        ["Fluxos otimizados (atual e futuro)", "Não", "5 processos prioritários"],
        ["Plano de automação", "Lista priorizada, sem estimativa", "Casos de uso priorizados por valor, risco, esforço e dependência, com módulos estimados e custo recorrente"],
        ["Avaliação de desempenho por competência", "Não (pode ser contratada à parte por R$ 3.200)", "Sim, em janeiro de 2027: matriz de competências, formulário, ciclo semestral e ligação com a gratificação"],
        ["Relatório e apresentação executiva", "Sim", "Sim"],
    ], [5.5, 4.5, 6])

    h(d, "Contenção imediata (opção Completa)", 3)
    par(d, "Três controles manuais, desenhados a partir dos erros reais citados no briefing, implantados com a equipe "
           "sem desenvolvimento e sem depender da Thamires no dia a dia:")
    lista(d, [
        ("Conferência de guia antes do pagamento: ", "checagem de cliente, CNPJ, pasta, tributo, competência e valor, com padrão mínimo de nome de arquivo."),
        ("Evidência para concluir tarefa: ", "nas rotinas críticas, o cartão do Trello só é concluído com o link do comprovante no OneDrive."),
        ("Registro de escalonamentos: ", "toda dúvida levada à Thamires é registrada com motivo e solução, o que vira o indicador de dependência e a base do futuro especialista de dúvidas."),
    ])

    h(d, "5. Fase 2 · Implantação em módulos (orçada depois do plano)")
    par(d, "Módulos citados no briefing, apresentados como ordem de grandeza para planejamento. O escopo, as horas e o "
           "preço de cada módulo só são fechados depois da Fase 1, com prova de viabilidade dos conectores envolvidos. "
           "Nenhum deles está contratado nesta proposta.")
    tabela(d, ["Módulo", "O que entrega", "Porte provável", "Dependências"], [
        ["Ambiente Surcin e Base Mestre de Clientes", "Conta Claude da Surcin, permissões, Projects Diretoria, Financeiro e Fiscal, base mínima de clientes no OneDrive", "M", "Contas novas no domínio Surcin"],
        ["Especialista de dúvidas (por setor)", "Assistente que responde com os procedimentos oficiais e escala só exceções", "M", "Procedimentos atualizados na Fase 1"],
        ["Validador de guias e documentos", "Alerta quando cliente, CNPJ, competência, tributo ou valor divergem; pagamento sempre humano", "M a G", "Padrão de pastas; amostras reais anonimizadas"],
        ["Fechamento financeiro interativo (piloto)", "Painel para um ou dois clientes, com dados mensais estruturados e narrativa preparada pelo Claude", "M a G", "Conta Azul; Lovable com dados segregados por cliente"],
        ["Auditoria Trello × OneDrive", "Fila de exceções para uma rotina (ex.: DP), sem concluir sozinha que algo não foi feito", "M", "Controle de evidência da Fase 1"],
        ["Fila de pedidos de pagamento", "Captura padronizada dos pedidos que chegam por WhatsApp; alternativa por formulário se os grupos não forem acessíveis", "M a G", "Viabilidade técnica e termos do Nestzap/Meta"],
        ["Painel de desempenho", "Dados para o programa de premiação, com critérios ajustáveis", "M", "Revisão trabalhista dos critérios"],
        ["Comercial e CRM", "Leads, propostas, onboarding", "G", "Janeiro de 2027"],
    ], [3.8, 6.2, 2, 4])
    par(d, "Porte de referência: P de R$ 1.500 a R$ 2.800; M de R$ 3.500 a R$ 6.500; G de R$ 8.000 a R$ 13.000. "
           "Cada módulo inclui desenho, construção, testes com dados anonimizados, documentação e treinamento.")

    h(d, "6. Princípios de implantação")
    lista(d, [
        ("Processo antes de ferramenta. ", "Nada é automatizado antes de o fluxo estar validado; parâmetros fiscais são conferidos antes de qualquer automação."),
        ("Matriz de autonomia. ", "Verde (pesquisar, resumir, conferir) pode ser automático; amarelo (criar tarefa, preparar mensagem, registrar conta a pagar) exige confirmação humana e registro; vermelho (pagar, protocolar, excluir, decidir) é sempre humano."),
        ("Ativos da Surcin. ", "Contas, licenças, prompts, especialistas, bases e código ficam em nome da Surcin, documentados, com acesso administrativo entregue."),
        ("Segurança e LGPD. ", "Segregação por cliente e função, acesso mínimo, registro de ações, dados reais só após homologação com dados anonimizados."),
        ("Continuidade. ", "Cada módulo tem procedimento manual de contingência e pode ser operado sem o consultor."),
    ])

    h(d, "7. Fora do escopo da Fase 1")
    lista(d, [
        "Desenvolvimento, configuração ou integração de automações e sistemas (Fase 2).",
        "Correção da parametrização do Domínio ou do CITAX (exige suporte do sistema ou especialista).",
        "Migração de contas para o domínio novo da Surcin.",
        "Definição de valores, periodicidade e natureza jurídica da premiação (exige revisão trabalhista).",
        "Recrutamento e seleção.",
        "Suporte contínuo, plantão ou urgência.",
        "Licenças e assinaturas.",
        "Serviços contábeis, fiscais, trabalhistas ou jurídicos.",
    ])

    h(d, "8. Esforço estimado (Fase 1)")
    par(d, "Premissas: 2 h por entrevista (1 h de conversa e 1 h de preparação e registro), 2 h por processo mapeado, "
           "2 h por processo redesenhado e 20% de contingência. Na Completa, a contenção imediata é absorvida pelo "
           "mapeamento do fiscal e do financeiro e pela contingência.")
    tabela(d, ["Atividade", "Essencial", "Completa"], [
        ["Entrevistas com a equipe", "8", "10"],
        ["Mapeamento dos processos atuais", "10", "16"],
        ["Gargalos e dependências", "3", "4"],
        ["Validação com a Thamires", "2", "2,5"],
        ["Estrutura organizacional", "6", "14"],
        ["Fluxos otimizados", "-", "10"],
        ["Plano de automação", "2", "5"],
        ["Relatório e apresentação executiva", "3", "6"],
        ["Avaliação de desempenho por competência", "-", "12"],
        ["Contingência (20%)", "7", "16"],
        ["**Total**", "**~41 h**", "**~96 h**"],
    ], [9, 3.5, 3.5])

    h(d, "9. Investimento (Fase 1)")
    tabela(d, ["Opção", "Investimento", "Pagamento"], [
        ["**Essencial**", "**R$ 7.800**", "50% no aceite, 50% na entrega"],
        ["**Completa (recomendada)**", "**R$ 17.400**", "30% no aceite, 35% na entrega do mapeamento, 35% na entrega final (janeiro de 2027)"],
        ["Hora avulsa (fora do escopo, sob aprovação prévia)", "R$ 220/h", "Mensal, conforme horas aprovadas"],
    ], [6, 4, 6])
    par(d, "A reunião inicial de 12/10/2026 e a preparação desta proposta não são cobradas. Acompanhamento mensal "
           "(Fase 3), se desejado, a partir de R$ 900 por mês com 4 horas.")

    h(d, "Avaliação de desempenho por competência (incluída na Completa)", 3)
    par(d, "Atende ao pedido de avaliar o desempenho individual e criar uma premiação (reunião 00:46 e 02:21; briefing, "
           "seção 10). Parte dos papéis e indicadores da Fase 1 e organiza a avaliação em ciclos semestrais, com uma "
           "gratificação de fim de ano que a Surcin consegue provisionar mês a mês.")
    lista(d, [
        "Matriz de competências por função (secretária, financeiro, DP, estagiária do jurídico), com o nível esperado de cada uma.",
        "Formulário de avaliação com escala definida: autoavaliação da funcionária e avaliação da Thamires.",
        "Regras do ciclo: duas avaliações por ano, critérios de assiduidade e pontualidade, conversa de devolutiva e plano de desenvolvimento individual.",
        "Modelo de ligação com a gratificação de fim de ano, com simulação de provisão mensal. Os valores são decisão dela.",
        "Guia de aplicação e uma sessão de preparação da Thamires para o primeiro ciclo.",
    ])
    tabela(d, ["Item", "Valor"], [
        ["Na opção Completa", "Incluída no valor (cerca de 14 h, reaproveitando os papéis e indicadores da estrutura organizacional)"],
        ["**Com a Essencial ou contratada depois**", "**R$ 3.200** (cerca de 18 h)"],
        ["Quando", "Janeiro de 2027, para que o primeiro ciclo cubra o 1º semestre de 2027"],
    ], [6, 10])
    aviso(d, "Os critérios e a gratificação precisam de revisão trabalhista antes de entrar em vigor, em especial o "
             "tratamento de faltas justificadas por atestado médico e a natureza jurídica do valor pago. Essa revisão "
             "não está incluída.")

    h(d, "10. Cronograma (opção Completa, aceite até 16/10/2026)")
    par(d, "Cerca de 10 horas por semana do consultor, segunda a sexta das 6h às 10h e depois das 19h30, além de sábados e domingos. Respeita as férias da Vitória "
           "(retorno em 28/10), a semana de fechamentos no início do mês e a prova da Thamires em 13/12.")
    tabela(d, ["Semana", "Atividades", "Participação da Surcin"], [
        ["19 a 25/10", "Kick-off, inventário de contas e ferramentas, coleta dos passo a passos, entrevistas com Thamires e Júlia", "Thamires 2 h, Júlia 1 h"],
        ["26/10 a 01/11", "Entrevistas com Tamara e Vitória; desenho do fiscal e dos pagamentos; desenho dos 3 controles", "Tamara 1 h, Vitória 1 h"],
        ["02 a 08/11", "Desenho dos fluxos atuais (sem reuniões: semana de fechamentos)", "Nenhuma"],
        ["09 a 15/11", "Validação, gargalos e dependências; controles em uso; entrega do mapeamento", "Equipe 1 h, Thamires 1 h"],
        ["16 a 29/11", "Estrutura organizacional: organogramas, papéis, indicadores", "Thamires 1 h"],
        ["30/11 a 13/12", "Fluxos otimizados e plano de automação (sem reuniões na semana da prova)", "Validação por escrito"],
        ["14 a 18/12", "Apresentação dos fluxos e do plano de automação; proposta dos módulos da Fase 2", "Thamires 2 h"],
        ["05 a 22/01/2027", "Avaliação de desempenho por competência: matriz, formulário, regras do ciclo e gratificação; entrega final", "Thamires 2 h"],
    ], [2.8, 9, 4.2])
    par(d, "Opção Essencial: de 19/10 a cerca de 22/11, com entrega única no fim. Primeiros módulos da Fase 2 a partir "
           "de janeiro de 2027.")

    h(d, "11. Respostas às perguntas do briefing (seção 16)")
    tabela(d, ["Pergunta", "Resposta"], [
        ["O que pode ser implantado com segurança antes de 13/12 sem consumir horas diárias da diretora?",
         "Os três controles manuais da contenção imediata, o mapeamento e a estrutura organizacional. Pedem cerca de 7 horas da Thamires no total, concentradas em outubro e novembro."],
        ["Quais três controles podem entrar primeiro?",
         "Conferência de guia antes do pagamento, evidência obrigatória para concluir cartões críticos e registro de escalonamentos. Depois, as versões automatizadas viram módulos da Fase 2."],
        ["Como a Base Mestre será estruturada sem duplicação ou vazamento?",
         "Uma única base no OneDrive como fonte oficial, com campos mínimos definidos na Fase 1; os especialistas consultam sem duplicar cadastro, com acesso por função. O desenho técnico sai no plano."],
        ["Como verificar identidade e competência de PDFs?",
         "Primeiro com padrão de nome e conferência humana (Fase 1); depois com validador testado em amostras reais anonimizadas, sempre com pagamento humano."],
        ["Como o painel do Lovable não expõe dados entre clientes?",
         "Piloto com um ou dois clientes, dados segregados por cliente e autenticação; protótipo visual não é tratado como plataforma pronta."],
        ["Quais integrações são viáveis?",
         "Cada conector (Conta Azul, Domínio, Nestzap/WhatsApp em grupos, OneDrive, Trello) recebe prova de viabilidade antes de entrar em orçamento. Nada é presumido."],
        ["Como é a homologação?",
         "Com dados fictícios ou anonimizados e autorização por escrito antes de usar dados reais."],
        ["E se o consultor sair ou uma ferramenta mudar?",
         "Ativos em nome da Surcin, documentação de cada rotina, procedimento manual de contingência e acesso administrativo entregue."],
    ], [6, 10])

    h(d, "12. Responsabilidades")
    h(d, "Do consultor", 3)
    lista(d, [
        "Conduzir entrevistas, análises e reuniões nas datas combinadas.",
        "Entregar os documentos em formato editável, no OneDrive da Surcin.",
        "Manter sigilo sobre dados da empresa e de seus clientes, com acordo de confidencialidade.",
        "Avisar com antecedência riscos de atraso ou mudança de escopo.",
        "Trabalhar no projeto de segunda a sexta das 6h às 10h e depois das 19h30, além de sábados e domingos.",
        "Responder mensagens em até 1 dia útil, dentro dessas janelas.",
    ])
    h(d, "Da cliente", 3)
    lista(d, [
        "Indicar a Júlia (ou outra pessoa) como ponto focal para acessos e agenda.",
        "Liberar acesso de leitura ao Trello, à pasta Geral do OneDrive e aos passo a passos.",
        "Liberar a equipe para entrevistas de cerca de 1 hora, no início do expediente (antes das 10h) ou após as 19h30.",
        "Aplicar os controles combinados na rotina.",
        "Responder dúvidas em até 2 dias úteis e validar entregas em até 5 dias úteis.",
    ])

    h(d, "13. Condições gerais")
    lista(d, [
        "Reuniões preferencialmente online, dentro da disponibilidade do consultor: segunda a sexta das 6h às 10h e depois das 19h30, além de sábados e domingos.",
        "Atrasos por falta de retorno ou de acesso deslocam o cronograma; pausas de mais de 10 dias reagendam o projeto.",
        "Mudanças de escopo são orçadas à parte e só executadas após aprovação por escrito.",
        "Os documentos produzidos são da Surcin após a quitação de cada parcela.",
        "Validade desta proposta: 15 dias a partir de 15/10/2026.",
    ])

    h(d, "14. Próximos passos")
    lista(d, [
        "Escolha da opção (Essencial ou Completa) e aceite.",
        "Acordo de confidencialidade.",
        "Kick-off na semana de 19/10 e agenda das entrevistas.",
    ], numerada=True)
    par(d, "\n" + CONSULTOR)
    d.save(f"{SAIDA}/04-proposta-comercial.docx")


# ---------------------------------------------------------------------------
# 05 · Roteiro + decisões
# ---------------------------------------------------------------------------
def roteiro():
    d = novo_doc("Roteiro da apresentação e decisões pendentes",
                 "Preparação para quinta-feira, 15/10/2026 · documento interno do Renato")

    h(d, "1. O que mudou com o briefing e as anotações do Gemini")
    lista(d, [
        "A Surcin espera mais do que consultoria: pede proposta modular com implantação, desenvolvimento, licenças e manutenção separados, e ganhos ainda em outubro e novembro.",
        "Para atender sem prometer implantação completa: a proposta agora tem contenção imediata (3 controles manuais) na Completa, módulos da Fase 2 com ordem de grandeza e respostas às perguntas da seção 16 do briefing.",
        "Fatos novos do briefing: fundação em 2021, plataforma Nestzap, CITAX em avaliação, detalhes do erro de ISS e de outros erros fiscais.",
        "Divergências a confirmar com ela: notas da Tamara, data do tráfego pago, contratação em janeiro, número de clientes do financeiro e ano da reconstrução (doc 01, seção 8).",
        "Versão 4 (13/10): retirados BPO, Joyce e contabilidade terceirizada, que não fazem parte do projeto, e conferidos de novo os números contra a transcrição.",
        "Preço da Completa: R$ 17.400 (era R$ 14.800), porque agora inclui a avaliação por competência em janeiro (~96 h). A contenção continua dentro da contingência.",
    ])

    h(d, "2. Decisões e revisões que só você pode fazer")
    tabela(d, ["#", "Decisão", "Padrão adotado"], [
        ["1", "Taxa-piso e preço", "Cerca de R$ 180/h; Essencial R$ 7.800, Completa R$ 17.400 (com avaliação por competência); hora avulsa R$ 220"],
        ["2", "Capacidade semanal", "10 h/semana, com 20% de contingência"],
        ["3", "Parcelamento", "Ela tem caixa até novembro e você disse que valores são conversáveis (02:07). Considerar a Completa em 4 vezes até janeiro"],
        ["4", "Contenção dentro das ~96 h", "Absorvida pela contingência; se preferir cobrar à parte, some cerca de 4 h (R$ 700)"],
        ["5", "Piloto antes de 13/12", "Não cabe nas 10 h/semana junto com a Completa. Alternativa: trocar os fluxos otimizados por um piloto (ex.: especialista de dúvidas do financeiro)"],
        ["6", "Horários das entrevistas", "Sua disponibilidade: seg-sex 6h-10h e após 19h30, sábados e domingos. A equipe trabalha em horário comercial: entrevistas no início do expediente (antes das 10h)"],
        ["7", "Contato na proposta", "Renato Romão, R2 Tech Consultoria; e-mail r2techconsultoria@gmail.com (do convite da reunião, confirmar); falta o telefone"],
        ["8", "Exclusividade no seu emprego", "Verificar antes de assinar"],
        ["9", "Avaliação por competência (decidido em 15/10)", "Dentro da Completa: R$ 17.400, ~96 h, entrega final em 22/01/2027. Com a Essencial ou depois: R$ 3.200 avulso"],
    ], [0.8, 4.5, 10.7])

    h(d, "3. Plano até quinta")
    tabela(d, ["Quando", "O que fazer", "Tempo"], [
        ["Terça 13/10 · noite", "Ler o diagnóstico (doc 01), principalmente as divergências", "1 h"],
        ["Quarta 14/10 · manhã", "Revisar a proposta (doc 04), em especial as seções 3, 5 e 11", "1 h"],
        ["Quarta 14/10 · noite", "Fechar as decisões acima e ensaiar com os slides (doc 06)", "2 h"],
        ["Quinta 15/10 · noite", "Apresentar e confirmar as divergências", "1 h"],
    ], [3.5, 10, 2.5])

    h(d, "4. Roteiro da apresentação (cerca de 45 minutos)")
    lista(d, [
        ("1. Abertura (2 min). ", "Agradecer a conversa e o briefing; dizer que ambos já são o diagnóstico preliminar, sem custo."),
        ("2. O que eu entendi (8 min). ", "Números, pessoas, erros reais e a frase \"você já tem processo, falta eficiência\"."),
        ("3. Como vamos trabalhar (5 min). ", "Processo e controle antes de ferramenta; Fases 1, 2 e 3."),
        ("4. Antes da prova (5 min). ", "Os 3 controles manuais e o que fica pronto até 13/12."),
        ("5. Estrutura organizacional (5 min). ", "Atual e hipótese proposta; pedir correções."),
        ("6. Fase 1: opções, cronograma e investimento (8 min). ", "Essencial e Completa, datas, parcelamento."),
        ("7. Fase 2: módulos (5 min). ", "Ordem de grandeza e por que só se orça depois do plano."),
        ("8. Respostas ao briefing e próximos passos (7 min). ", "Seção 11 da proposta; confirmar divergências."),
    ])

    h(d, "5. Possíveis objeções e respostas")
    tabela(d, ["Se ela disser", "Resposta sugerida"], [
        ["Eu queria a implantação, não só consultoria.", "A implantação está desenhada em módulos. Orçar agora seria chutar: cada integração precisa de prova de viabilidade, e o Domínio está com parâmetro errado. A Fase 1 já entrega controles em uso antes da prova."],
        ["O caixa está apertado até janeiro.", "Começar pela Essencial ou parcelar a Completa."],
        ["Já tenho os processos, por que mapear?", "Por isso o trabalho é mais rápido. O mapeamento mostra onde o processo trava e o que pode sair das suas mãos."],
        ["Não tenho tempo por causa da prova.", "Cerca de 7 horas suas no total, concentradas em outubro e novembro, sem reuniões na semana da prova."],
        ["E a premiação?", "Depende de papéis e indicadores, que saem da Fase 1; valores e natureza jurídica precisam de revisão trabalhista."],
    ], [5.5, 10.5])
    d.save(f"{SAIDA}/05-roteiro-apresentacao-e-decisoes.docx")


if __name__ == "__main__":
    diagnostico()
    estrutura()
    metodologia()
    proposta()
    roteiro()
    print("ok")
