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


def novo_doc(titulo, subtitulo, versao=VERSAO):
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
    r = p.add_run(versao)
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
        t.autofit = False
        for i, w in enumerate(larguras):
            t.columns[i].width = Cm(w)
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
    d = novo_doc("Proposta de consultoria",
                 "Organização, processos, rotinas do Claude e pilotos de automação · Surcin Assessoria Empresarial",
                 "Versão 6 · 26/10/2026 · oferta única · válida até 30/10/2026")

    h(d, "1. O que entendemos")
    par(d, "A Surcin oferece contabilidade, fiscal, DP, financeiro, societário e jurídico empresarial, com cerca de "
           "40 a 45 empresas na carteira fiscal, cerca de 12 a 16 clientes no financeiro e uma equipe enxuta. A empresa já tem processos "
           "desenhados, padrão de pastas e rotinas no Trello, mas a Thamires continua sendo a fonte única de "
           "conhecimento, decisão e revisão, e os erros recentes vieram de parâmetros fiscais errados e de controles "
           "que dependem de atenção humana.")
    par(d, "O objetivo é que, a partir de janeiro de 2027, a equipe opere com papéis claros, fluxos documentados, "
           "rotinas do Claude testadas e indicadores por área, sem depender da Thamires para cada decisão. A ordem é "
           "sempre a mesma: primeiro processo e controle, depois ferramenta e automação assistida.")

    h(d, "2. O que a Surcin recebe")
    lista(d, [
        "Diagnóstico, mapa dos processos atuais e plano inicial.",
        "Organograma funcional, matriz de responsabilidades e alçadas.",
        "Fluxos futuros e listas de verificação da entrada do cliente e da passagem formal para a operação.",
        "Biblioteca de 5 rotinas do Claude documentadas e testadas.",
        "2 pilotos demonstrados, com resultados registrados.",
        "Até 2 integrações implantadas entre sistemas de viabilidade confirmada.",
        "Painel de indicadores por área (DP, Financeiro, Contabilidade e Comercial) e visão da diretoria.",
        "Primeiro ciclo de avaliação de desempenho por competência.",
        "Manuais, 3 treinamentos e plano de evolução.",
    ])

    h(d, "3. Etapas, datas e aceites")
    par(d, "Um projeto deste porte normalmente leva cerca de 18 semanas. Para atender ao prazo da Surcin, ele foi "
           "condensado em 8 semanas, de 03/11 a 23/12/2026, com etapas sobrepostas. A partir de janeiro, a Surcin "
           "opera com o que foi implantado.")
    tabela(d, ["Etapa", "Período", "Horas", "O que entrega", "Aceite"], [
        ["1 · Diagnóstico e inventário", "03 a 13/11", "28 h",
         "Reunião de abertura e análise de materiais; até 5 entrevistas; mapeamento de até 8 processos atuais; inventário de sistemas e riscos",
         "Diagnóstico, mapa atual, prioridades e plano inicial validados"],
        ["2 · Arquitetura operacional", "16 a 29/11", "42 h",
         "Organograma funcional, matriz de responsabilidades e alçadas; jornada de entrada do cliente e passagem formal; redesenho de até 5 fluxos; controles prioritários; indicadores por área e competências por papel",
         "Fluxos futuros, responsabilidades e listas de verificação aprovados"],
        ["3 · Fundação do Claude e rotinas", "23/11 a 13/12", "52 h",
         "Organização da base e das fontes oficiais; Projetos do Claude; construção, testes e documentação das 5 rotinas do Claude",
         "Biblioteca de 5 rotinas do Claude validada para uso assistido"],
        ["4 · Pilotos e painel", "07 a 20/12", "63 h",
         "Implantação controlada dos pilotos A e B com dados autorizados; até 2 integrações implantadas; primeira versão do painel por área (planilha ou Trello)",
         "Demonstração funcional, resultados dos testes, aceite dos 2 pilotos e painel em uso"],
        ["5 · Adoção e transferência", "14 a 23/12", "36 h",
         "Ajustes acordados; 3 treinamentos de até 90 minutos; manuais; painel por área e da diretoria; primeiro ciclo de avaliação por competência; plano de evolução",
         "Arquivos editáveis, treinamento, avaliação aplicada, relatório final e passagem formal aprovados"],
        ["**Total**", "**8 semanas**", "**~221 h**", "", ""],
    ], [3.2, 2.2, 1.4, 5.6, 4.2])

    aviso(d, "Dois meses intensivos. Para entregar tudo funcionando até 23/12, a R2 trabalha no projeto todos os dias, "
             "inclusive sábados e domingos: são cerca de 221 horas, ou cerca de 4h15 por dia, de 03/11 a 23/12. "
             "Não há folga no calendário: o prazo depende de entrevistas, acessos e dados chegarem nas datas.")

    h(d, "4. As 5 rotinas do Claude")
    par(d, "Até 5 rotinas do Claude, escolhidas entre os processos priorizados no diagnóstico. As cinco abaixo são as "
           "candidatas iniciais. Uma rotina do Claude é um procedimento escrito e testado, operado de forma assistida: "
           "uma pessoa autorizada fornece o insumo, o Claude produz a saída e uma pessoa valida.")
    tabela(d, ["Rotina do Claude", "Entra", "Sai", "Validação humana"], [
        ["01 · Entrada do cliente e passagem formal", "Dados de implantação autorizados", "Trilha, lista de verificação, pendências e resumo da passagem formal", "Júlia coordena; a área técnica aprova a ativação"],
        ["02 · Triagem de demandas", "Mensagem ou documento importado", "Categoria, prioridade sugerida, responsável e rascunho de resposta", "Atendimento revisa antes de enviar"],
        ["03 · Conferência de guias e documentos", "Documentos e cadastro mestre autorizado", "Quadro por cliente, competência e tributo, com divergências", "Fiscal ou financeiro libera"],
        ["04 · Fechamento financeiro assistido", "Exportações do Conta Azul e planilhas", "Conferências, indicadores e minuta de análise", "Vitória e/ou Thamires valida"],
        ["05 · Controle de tarefas e evidências", "Relatório de tarefas e índice de documentos", "Pendências e inconsistências sinalizadas", "Área responsável confere a evidência"],
    ], [4.2, 3.6, 4.8, 4])
    par(d, "Cada rotina traz finalidade, procedimento, limites, 3 ou mais casos de teste e responsável. Passar de 5 "
           "rotinas exige aditivo.")

    h(d, "5. Os 2 pilotos")
    lista(d, [
        ("Piloto A · Entrada do cliente assistida, com a Júlia: ", "até 2 casos selecionados; triagem por tipo de cliente e serviços contratados; lista de verificação e identificação de campos e documentos ausentes; passagem formal com responsáveis, pendências e prazo."),
        ("Piloto B · Conferência assistida de guias e documentos: ", "documentos de teste pré-aprovados, de preferência anonimizados; confronto de cliente, CNPJ, competência, tributo, valor e pasta; sinalização de campos ausentes, diferenças e baixa confiança."),
    ])
    par(d, "Os pilotos não dependem de conexão automática com Domínio, Veri ou OneDrive: se um conector não for viável, "
           "o piloto segue com arquivos exportados. Ficam fora dos pilotos o pagamento bancário, a transmissão de "
           "declarações, decisões fiscais ou jurídicas finais e a integração com grupos de WhatsApp.")

    h(d, "6. Integrações: o que dá para ligar")
    par(d, "A proposta inclui até 2 integrações implantadas, escolhidas no diagnóstico entre os sistemas de viabilidade "
           "alta ou média confirmada. A classificação abaixo é uma leitura prévia, feita a partir do que se sabe "
           "publicamente de cada sistema, e será confirmada com os planos e acessos reais da Surcin.")
    tabela(d, ["Viabilidade", "Sistemas", "Por quê"], [
        ["**Alta**", "Trello, OneDrive e Microsoft 365 (Excel), Google Agenda, Google Forms, Notion, Slack", "Têm acesso técnico público e documentado, e a maioria já tem conector pronto para o Claude."],
        ["**Média**", "Conta Azul, WhatsApp", "O Conta Azul tem acesso técnico público, mas a Surcin precisa autorizar. No WhatsApp, só a versão oficial do WhatsApp Business permite automação; ela é paga por conversa e não automatiza grupos."],
        ["**Por arquivo exportado**", "Domínio, Veri, Nestzap, Jusbrasil, Alterdata, CITAX", "Não há acesso técnico aberto conhecido para uso direto. Nesses sistemas a rotina usa relatórios exportados até que um acesso seja comprovado."],
    ], [3, 5.5, 8])
    par(d, "Candidatas mais fortes: Trello com o Claude (controle de tarefas e painel) e Conta Azul com a planilha do "
           "fechamento. Alternativa: OneDrive, para a conferência de documentos. Se um acesso não se confirmar, a "
           "rotina segue por arquivo exportado e a troca fica registrada no plano de evolução. Nenhuma integração "
           "paga, protocola ou envia algo a cliente sem confirmação humana.")

    h(d, "7. Avaliação de desempenho e painéis por área")
    lista(d, [
        ("Avaliação por competência: ", "competências ajustadas aos papéis definidos na Etapa 2, ficha de avaliação, dicionário de notas, roteiro da conversa de avaliação, rotina de 1:1 semanal e regras de registro de faltas, atrasos e atestados. O primeiro ciclo é aplicado com a Thamires na Etapa 5. O modelo prevê avaliação semestral."),
        ("Painéis por área: ", "de 3 a 5 indicadores por área (DP, Financeiro, Contabilidade e Comercial), mais uma visão da diretoria, cada um com definição, fórmula, fonte, responsável e meta. Na primeira versão, o painel é alimentado por planilha ou pelo Trello, com uma rotina semanal de atualização; a ligação direta com Domínio e Conta Azul depende das integrações da Etapa 4."),
    ])
    aviso(d, "Os valores de gratificação são decisão da Thamires, e os critérios precisam de revisão trabalhista antes de "
             "entrar em vigor, em especial o tratamento de faltas justificadas por atestado médico. Essa revisão não "
             "está incluída.")

    h(d, "8. Escopo fechado")
    tabela(d, ["Item", "Limite do contrato"], [
        ["Entrevistas", "5"],
        ["Processos atuais mapeados", "8"],
        ["Fluxos redesenhados", "5"],
        ["Rotinas do Claude", "5"],
        ["Pilotos funcionais", "2"],
        ["Integrações implantadas", "2"],
        ["Treinamentos de até 90 minutos", "3"],
        ["Painel por área + diretoria", "1"],
        ["Ciclo de avaliação por competência", "1"],
    ], [10, 6])
    h(d, "Fora do escopo", 3)
    lista(d, [
        "Sistema de gestão integrado (ERP) ou implementação completa de todos os setores.",
        "Migração de toda a base histórica.",
        "Integrações além das 2 contratadas e sistemas sem acesso técnico (seguem por arquivo exportado).",
        "Auditoria fiscal ou contábil formal.",
        "Decisões e protocolos profissionais, que continuam com a equipe da Surcin.",
        "Disparos sensíveis e pagamentos automáticos.",
        "Suporte contínuo e monitoramento 24 horas por dia.",
        "Valores de gratificação e revisão trabalhista.",
    ])
    par(d, "Tudo além do escopo fechado exige orçamento ou aditivo, aprovado por escrito antes da execução.")

    h(d, "9. Investimento")
    tabela(d, ["", "Valor", "Quando"], [
        ["**Consultoria e implantação**", "**R$ 31.900**", "8 semanas · 5 etapas · 5 rotinas do Claude · 2 pilotos · 2 integrações"],
        ["Parcela 1 · 30%", "R$ 9.570", "03/11/2026 · início do projeto"],
        ["Parcela 2 · 35%", "R$ 11.165", "01/12/2026 · meio do projeto"],
        ["Parcela 3 · 35%", "R$ 11.165", "05/01/2027 · fim do projeto, após a entrega final de 23/12"],
    ], [5, 3.5, 7.5])
    par(d, "Valor único, com escopo fechado. As parcelas seguem o calendário do projeto, com vencimento em datas "
           "fixas: início, meio e fim.")
    h(d, "Custos da Surcin, à parte e com aprovação prévia", 3)
    par(d, "Planos do Claude e de outras ferramentas, uso de modelos de IA e integrações, automação, hospedagem, "
           "licenças, custo por conversa do WhatsApp Business, infraestrutura e eventuais terceiros.")

    h(d, "10. Princípios de implantação")
    lista(d, [
        ("Processo antes de ferramenta. ", "Nada é automatizado antes de o fluxo estar validado; parâmetros fiscais são conferidos antes de qualquer automação."),
        ("Confirmação humana. ", "Pesquisar, resumir e conferir podem ser automáticos; criar tarefa ou preparar mensagem exige confirmação e registro; pagar, protocolar, excluir e decidir é sempre humano."),
        ("Ativos da Surcin. ", "Arquivos e materiais contratados ficam com a Surcin, com acesso de administrador ao que for dela. A R2 mantém a metodologia pré-existente."),
        ("Segurança e LGPD. ", "Confidencialidade, minimização e segregação de dados por cliente, testes com dados anonimizados e credenciais em ambiente seguro."),
        ("Continuidade. ", "Cada rotina tem alternativa manual e pode ser operada sem o consultor."),
    ])

    h(d, "11. Responsabilidades")
    h(d, "Da R2 Tech Consultoria", 3)
    lista(d, [
        "Conduzir entrevistas, análises e reuniões nas datas combinadas.",
        "Trabalhar no projeto todos os dias, inclusive sábados e domingos, de 03/11 a 23/12.",
        "Entregar os documentos em formato editável, no ambiente da Surcin.",
        "Manter sigilo sobre os dados da empresa e de seus clientes, com acordo de confidencialidade.",
        "Avisar com antecedência riscos de atraso ou mudança de escopo.",
    ])
    h(d, "Da Surcin", 3)
    lista(d, [
        "Aceitar a proposta até 30/10 e liberar os acessos no início do projeto.",
        "Indicar um ponto focal para acessos e agenda.",
        "Liberar a equipe para entrevistas de cerca de 1 hora de 09 a 13/11 (sem entrevistas nos fechamentos, de 02 a 08/11).",
        "Fornecer dados autorizados para os pilotos.",
        "Responder e validar entregas em até 1 dia útil.",
        "Não há reuniões na semana de 07 a 13/12, por causa da prova da Thamires.",
    ])

    h(d, "12. Condições gerais")
    lista(d, [
        "As datas partem de um aceite até 30/10/2026. Aceite depois disso desloca o calendário.",
        "02/11 (Finados) e 20/11 (Consciência Negra) são feriados e não terão reuniões.",
        "Atrasos por falta de retorno, acesso ou dados deslocam o cronograma.",
        "Mudanças de escopo são orçadas à parte e só executadas após aprovação por escrito.",
        "Os materiais produzidos passam a ser da Surcin após a quitação de cada parcela.",
        "Validade desta proposta: até 30/10/2026.",
    ])

    h(d, "13. Próximos passos")
    lista(d, [
        "Aceite da proposta: confirmação de escopo e investimento.",
        "Contrato e confidencialidade: marcos, LGPD e propriedade formalizados.",
        "Acessos e materiais: levantamento do que a Etapa 1 precisa.",
        "Reunião de abertura em 03/11, com o aceite até 30/10.",
    ], numerada=True)
    par(d, "\nRenato Romão · R2 Tech Consultoria · r2techconsultoria@gmail.com")
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
