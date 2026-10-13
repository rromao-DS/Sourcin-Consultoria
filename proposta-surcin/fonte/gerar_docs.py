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
VERSAO = "Versão 2 · 13/10/2026 · atualizada com a transcrição da reunião · uso interno até revisão do Renato"


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
    rodape.text = "Surcin · Proposta de consultoria em organização e processos · Confidencial"
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


LEGENDA = ("Legenda: [FATO] dito pela Thamires na reunião de 12/10/2026 (o minuto da gravação aparece entre "
           "parênteses); [HIPÓTESE] leitura do consultor, a validar; [CONFIRMAR] número ou nome que apareceu "
           "de forma ambígua na transcrição automática.")

CONSULTOR = "Renato [sobrenome] · R2 Tech Consulting [confirmar marca] · [e-mail] · [telefone]"


# ---------------------------------------------------------------------------
# 01 · Diagnóstico preliminar
# ---------------------------------------------------------------------------
def diagnostico():
    d = novo_doc("Diagnóstico preliminar", "Surcin · leitura da reunião de descoberta de 12/10/2026")
    aviso(d, "Fonte: transcrição automática da reunião de 12/10/2026 (2h38). Transcrições automáticas trocam "
             "nomes e números; os pontos marcados [CONFIRMAR] devem ser conferidos com a gravação ou com a "
             "Thamires. Nada aqui foi acrescentado além do que ela disse.")
    par(d, LEGENDA, italico=True)

    h(d, "1. Resumo executivo")
    par(d, "A Surcin é um escritório pequeno que já tem processos desenhados, mas ainda depende da Thamires "
           "para quase tudo. Ela reconstruiu a empresa a partir de 2023 com passo a passos, checklists e "
           "rotinas no Trello, e recuperou cerca de 90% dos clientes que havia perdido (00:11). O gargalo "
           "atual não é falta de processo, é falta de eficiência e de autonomia da equipe: ela revisa e "
           "corrige tudo, e um erro de configuração no Domínio em agosto gerou imposto pago errado, multa, "
           "um prejuízo de cerca de R$ 10 mil e a perda de um cliente (00:26 a 00:29).")
    par(d, "Ela tem prazo pessoal e financeiro: uma prova de certificação em 13/12/2026, caixa garantido por um "
           "Pronampe até novembro e a meta de entrar em janeiro com a casa arrumada para contratar um contador "
           "e voltar a investir em vendas (00:31 a 00:37, 02:14).")
    par(d, "Frase dela que resume o objetivo: \"Hoje eu sinto que eu tenho um processo. Esse processo ele só não "
           "tá eficiente. Se eu melhorar isso, eu consigo escalar com as mesmas pessoas.\" (01:14)", italico=True)

    h(d, "2. A empresa")
    tabela(d, ["Item", "O que foi dito", "Fonte"], [
        ["Proposta de valor", "Fazer a gestão do empresário de ponta a ponta: contabilidade, financeiro (onde ela mais se encontra) e jurídico consultivo e preventivo", "[FATO] 00:05"],
        ["Estrutura societária", "Três CNPJs: contabilidade, financeiro e jurídico, separados por questão tributária", "[FATO] 01:02"],
        ["Clientes de contabilidade", "Cerca de 40; o fiscal do mês passado cobriu 44 clientes", "[FATO] 01:55 e 02:00"],
        ["Clientes de financeiro (BPO)", "Entre 12 e 16, conforme o trecho; Vitória cuida de todos", "[FATO] 00:38, 00:46, 01:02 [CONFIRMAR]"],
        ["Departamento Pessoal", "Cerca de 25 vidas; 4 ou 5 clientes com funcionários; a maioria dos clientes é PJ", "[FATO] 00:40"],
        ["Jurídico", "Cerca de 20 processos em andamento, herdados de uma sociedade desfeita, em fase final; contratos e societário (abertura de empresas). Hoje não gera receita recorrente", "[FATO] 00:43, 01:45"],
        ["Outros serviços", "Revenda de certificado digital, imposto de renda (pontual), parcerias com outras contabilidades, clientes do Lucro Presumido", "[FATO] 00:52 a 00:53"],
        ["Situação financeira", "Prejuízo de agosto; Pronampe garante caixa até novembro; dezembro apertado; pagamento começa em fevereiro", "[FATO] 00:31, 01:33"],
        ["Decisões já tomadas", "Não contratar até o fim do ano; contratar em janeiro um contador experiente no Domínio; tráfego pago pausado (cerca de R$ 1 mil em anúncios), social media mantida", "[FATO] 00:30, 01:49, 02:12"],
    ], [3.5, 9.5, 3])

    h(d, "3. Equipe atual")
    tabela(d, ["Pessoa", "Função hoje", "Observações dela", "Fonte"], [
        ["Thamires", "Direção, técnica contábil e jurídica, fiscal (absorveu após a saída da contadora), reuniões de fechamento, comercial", "Tudo passa por ela; revisa o trabalho de todos", "00:18, 00:30"],
        ["Júlia", "Secretária e braço direito: atendimento, WhatsApp, agenda, Trello, implantação de novos clientes, propostas no Canva, envio de impostos, apoio no fiscal (confere notas e XML)", "Vê a empresa inteira; candidata a supervisora em 2027, condicionado a graduação", "00:15 a 00:19, 01:04, 01:35"],
        ["Vitória", "Financeiro operacional: pagamentos (terças e sextas), emissão de notas, conciliação no Conta Azul, preparação do fechamento", "Muito boa quando o processo está desenhado; ainda precisa de ajuda na classificação de despesas. De férias até 28/10 [CONFIRMAR]", "00:13 a 00:15, 01:21, 01:34"],
        ["Tamara", "Hoje divide DP (folha), conciliações e emissão de notas; a partir de novembro, só DP", "Sem experiência anterior; está gostando do DP", "00:39 a 00:41, 02:05"],
        ["Alana", "Estagiária do jurídico: processos em andamento e apoio no societário", "Trabalha só quarta e sexta, paga por hora; tudo precisa de revisão; a permanência está em reavaliação", "00:42 a 00:43, 01:40 a 01:42, 02:18"],
    ], [2.3, 6, 5.2, 2.5])
    par(d, "A contadora contratada para assumir a contabilidade saiu depois do erro de agosto. Desde então a área "
           "não tem responsável além da Thamires (00:30).")

    h(d, "4. Ferramentas e uso real")
    tabela(d, ["Ferramenta", "Uso descrito na reunião", "Fonte"], [
        ["Trello", "Principal ferramenta de gestão: rotinas diárias e mensais por pessoa, pendências, checklists de novo cliente e de abertura de empresa. Ela atribui ao Trello a queda nos erros", "01:03 a 01:07"],
        ["OneDrive / Office", "Nuvem organizada por frente de serviço, com padrão de pastas por cliente; pasta Geral com acessos, passo a passos e modelos. Toda a equipe trabalha na nuvem", "00:52 a 00:54, 01:03"],
        ["Google Agenda", "Agenda central da operação, controlada pela Júlia", "00:51"],
        ["Veri", "Suporte à contabilidade: aplicativo do cliente com impostos, certidões e documentos, modelos de contrato. A partir de novembro a comunicação com clientes de contabilidade será só pelo aplicativo", "01:15 a 01:17"],
        ["Domínio", "Sistema contábil e fiscal. Configuração errada desde a migração; hoje o fiscal é feito direto no portal da Receita", "01:17"],
        ["Conta Azul", "Operação dos clientes do financeiro: conciliação bancária, extratos, plano de contas personalizado. A emissão de nota a partir da conciliação ainda não foi configurada", "01:20, 00:40"],
        ["Plataforma de atendimento (WhatsApp)", "Número único com vários usuários; a Júlia recebe e distribui as conversas para a equipe [CONFIRMAR se é o NetsApp citado no briefing]", "01:54 a 01:55"],
        ["Jusbrasil", "IA jurídica e modelos de petição; o monitoramento automático dos processos ainda não foi configurado", "01:43 a 01:44"],
        ["Canva", "Modelos de proposta comercial preenchidos pela Júlia", "01:22"],
        ["Claude e Lovable", "Usados pela Thamires para o fechamento financeiro: o primeiro levou 5 horas, os últimos de 1 a 2 horas, refinando o prompt a cada mês", "00:33 a 00:35"],
        ["ChatGPT", "Usado pela Júlia no atendimento", "01:55"],
    ], [3.5, 10, 2.5])
    par(d, "Ela quer recriar as contas (e-mail, nuvem, Trello, Claude, Lovable) do zero no novo domínio da Surcin, "
           "porque o pacote antigo vai expirar (00:59 a 01:00, 02:10).")

    h(d, "5. Processos que já existem")
    par(d, "Processos citados com algum nível de documentação (passo a passo, checklist ou rotina no Trello):")
    tabela(d, ["#", "Processo", "Quem executa", "Situação descrita"], [
        ["1", "Atendimento e triagem de demandas", "Júlia", "Funciona, mas concentra tudo nela"],
        ["2", "Comercial: primeiro atendimento, checklist, proposta, reunião", "Júlia e Thamires", "Checklist e modelos prontos"],
        ["3", "Implantação de novo cliente de contabilidade", "Júlia", "Checklist pronto; precisa de atualização"],
        ["4", "Implantação de novo cliente de financeiro", "Júlia e Vitória", "Checklist pronto; inclui planilha, Trello e Conta Azul"],
        ["5", "Abertura de empresa (societário)", "Júlia, Alana, Thamires", "Checklist no Trello; abertura em Campinas gravada, sem refinar"],
        ["6", "Fiscal mensal: XML, apuração, guia, recibos, envio ao cliente", "Thamires e Júlia", "Feito fora do Domínio; maior risco (erro de agosto)"],
        ["7", "Pagamentos dos clientes do financeiro (terças e sextas)", "Vitória", "Informações de pagamentos fixos desorganizadas em parte dos clientes"],
        ["8", "Emissão de notas fiscais", "Tamara e Vitória", "Feita por fora do Conta Azul"],
        ["9", "Conciliação e fechamento mensal com reunião de resultado", "Vitória e Thamires", "Conciliação concentrada no fim do mês; cerca de 15 reuniões de 1 a 2 h na primeira semana"],
        ["10", "Folha e rotinas de DP", "Tamara", "Volume baixo; pendências antigas a organizar"],
        ["11", "Acompanhamento de processos jurídicos", "Alana e Thamires", "Revisão manual de todos os processos"],
    ], [0.8, 6.2, 3.5, 5.5])

    h(d, "6. Dores, objetivos e expectativas")
    tabela(d, ["Dor ou objetivo (palavras dela)", "Área", "Fonte"], [
        ["\"Tudo tá centralizado em mim. Eu não tenho o direito de ficar doente.\"", "Gestão", "00:18"],
        ["Revisar e corrigir tudo; dúvidas simples da equipe chegam a ela", "Todas", "00:15, 00:39, 01:27"],
        ["Erro de configuração no Domínio: imposto recolhido errado, multa, cerca de R$ 10 mil e um cliente perdido", "Contabilidade", "00:26 a 00:29"],
        ["Contabilidade sem responsável desde a saída da contadora", "Contabilidade", "00:30"],
        ["Fechamento financeiro lento: conciliação no fim do mês, reuniões só na segunda ou terceira semana", "Financeiro", "01:31 a 01:32"],
        ["Escalar sem contratar: Vitória passar de 15 para 30 clientes", "Financeiro", "00:46, 01:25"],
        ["Ter tempo para estudar para a prova de 13/12", "Pessoal", "00:36, 02:14"],
        ["Equipe com mais autonomia", "Gestão", "00:44"],
        ["Avaliar a produtividade individual e criar uma remuneração variável por pontos", "Pessoas", "00:46, 01:57, 02:21"],
        ["Retomar o comercial (tráfego pago, possível agente de WhatsApp/CRM), sem atendimento robotizado", "Vendas", "00:45, 01:55"],
        ["Ter um assistente de dúvidas por setor", "Todas", "00:39"],
        ["Estruturar no futuro uma consultoria jurídica para os clientes", "Jurídico", "01:45"],
    ], [10, 3, 3])
    par(d, "Disponibilidade dela: esta semana está cheia; a partir de 19/10 pretende estudar de manhã e trabalhar à "
           "tarde, com tempo para o projeto. A primeira semana de cada mês concentra as reuniões de fechamento "
           "(02:15 a 02:17).")

    h(d, "7. Leitura do consultor")
    lista(d, [
        ("[HIPÓTESE] O ponto de partida é bom. ", "Há documentação, padrão de pastas e rotinas no Trello. O mapeamento parte do que existe e não do zero, o que reduz esforço."),
        ("[HIPÓTESE] O maior risco está no fiscal. ", "Sem contador, com o Domínio mal configurado e com execução manual, é onde um erro custa mais caro. A correção da configuração exige o suporte do Domínio ou um especialista no sistema."),
        ("[HIPÓTESE] A Júlia é ponto único de falha. ", "Ela recebe, distribui e acompanha tudo. Formalizar o papel dela e um substituto é tão importante quanto promovê-la."),
        ("[HIPÓTESE] A remuneração variável depende de papéis claros. ", "Sem descrição de função e entregas medíveis, um programa de pontos vira discussão. A estrutura organizacional é o pré-requisito."),
        ("[HIPÓTESE] Há ganhos rápidos sem automação. ", "Configurar a emissão de nota pelo Conta Azul, o monitoramento de processos no Jusbrasil e a conciliação semanal resolvem parte das dores antes de qualquer desenvolvimento."),
        ("[HIPÓTESE] Custo de IA precisa entrar na conta. ", "O uso do Claude por várias pessoas tem limites e custo; quem usa e para quê deve sair do plano de automação."),
    ])

    h(d, "8. Perguntas que ainda faltam responder")
    blocos = {
        "Números e prioridades": [
            "Quantos clientes há hoje em cada serviço (contabilidade, financeiro, DP, jurídico)?",
            "Qual processo, se resolvido primeiro, mais devolveria tempo a você: fiscal, fechamento financeiro ou implantação de clientes?",
            "Quais passo a passos estão atualizados e quais precisam de revisão?",
        ],
        "Equipe e agenda": [
            "A equipe pode participar de entrevistas antes das 10h30, no almoço ou após as 19h30?",
            "A Júlia pode ser a ponto focal do projeto? Quantas horas por semana ela pode dedicar?",
            "A Vitória volta de férias em 28/10?",
            "A Alana continua em 2027? O contador que você pretende contratar entraria no desenho da estrutura?",
        ],
        "Sistemas": [
            "Qual é o nome da plataforma de atendimento do WhatsApp? É o NetsApp?",
            "Quem vai corrigir a configuração do Domínio, e até quando?",
            "Quando será a migração das contas para o novo domínio da Surcin, e quem cuida dela?",
            "Você prefere ficar no Microsoft ou migrar para o Google?",
        ],
        "Investimento": [
            "Qual faixa de investimento cabe agora, considerando o caixa até dezembro?",
            "Há orçamento separado para ferramentas (licenças do Claude, API de WhatsApp)?",
        ],
    }
    for titulo, perguntas in blocos.items():
        h(d, titulo, 3)
        lista(d, perguntas)

    h(d, "9. Materiais a receber")
    lista(d, [
        "Gravação da reunião, apresentação e resumo da trajetória que ela ficou de enviar por e-mail (00:04, 02:36).",
        "Acesso de leitura ao Trello, à pasta Geral do OneDrive e aos passo a passos, via Júlia (02:09).",
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
             "(Etapa 2 da proposta).")

    h(d, "1. Estrutura atual (como é)")
    org_bloco(d, [
        "Thamires · direção, técnica contábil e jurídica, fiscal, comercial, reuniões de fechamento",
        "    ├── Júlia · secretária: atendimento, implantação de clientes, apoio no fiscal",
        "    ├── Vitória · financeiro (BPO): pagamentos, notas, conciliação, preparação do fechamento",
        "    ├── Tamara · DP + apoio no financeiro e notas (só DP a partir de novembro)",
        "    └── Alana · estagiária do jurídico (quarta e sexta)",
    ])
    par(d, "Pontos de atenção que ela mesma levantou:")
    lista(d, [
        "Contabilidade e fiscal sem responsável técnico além da Thamires desde a saída da contadora.",
        "Todas as dúvidas e revisões sobem para a Thamires.",
        "A Júlia acumula atendimento, distribuição de demandas, implantação, comercial e parte do fiscal.",
        "A Tamara alterna entre três áreas diferentes (até outubro).",
        "O jurídico consome revisão da Thamires e não gera receita recorrente.",
    ])

    h(d, "2. Hipótese de estrutura proposta (como poderia ser)")
    par(d, "Desenho discutido na reunião (01:38 a 01:51), organizado por fluxo do cliente: entrada, operação e revisão técnica.")
    org_bloco(d, [
        "Thamires · direção, estratégia, relacionamento com clientes-chave, jurídico consultivo",
        "    ├── Revisão técnica contábil · contador(a) sênior a contratar em 2027 [decisão dela]",
        "    │       └── Contabilidade e fiscal (operação)",
        "    ├── Entrada e relacionamento · Júlia",
        "    │       comercial, implantação de clientes, atendimento e triagem",
        "    ├── Financeiro (BPO) · Vitória",
        "    ├── Departamento Pessoal · Tamara [avaliar se absorve apoio ao societário]",
        "    └── Jurídico · processos legados [avaliar: manter estágio ou absorver com monitoramento no Jusbrasil]",
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
           "precisa: papéis, entregas e indicadores por função. O desenho do programa (pesos, metas e valores) é uma "
           "decisão dela e pode ser orçado à parte.")

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
    ], [3.5, 6, 6.5])

    h(d, "7. Critérios para propor uma automação")
    lista(d, [
        "O processo está validado e simplificado.",
        "Há volume ou risco que justifique o esforço (horas economizadas × custo da hora da equipe).",
        "Os sistemas permitem integração (verificado, não suposto); o Domínio só depois de corrigida a configuração.",
        "Existe alguém da equipe responsável por operar e acompanhar a automação.",
        "O custo recorrente de ferramentas (licenças de IA, API do WhatsApp) cabe no orçamento.",
        "O tratamento de dados pessoais está de acordo com a LGPD.",
    ])
    d.save(f"{SAIDA}/03-metodologia-mapeamento-processos.docx")


# ---------------------------------------------------------------------------
# 04 · Proposta comercial
# ---------------------------------------------------------------------------
def proposta():
    d = novo_doc("Proposta de consultoria", "Organização, estrutura e processos · Surcin")
    aviso(d, "Valores calculados com taxa de referência de cerca de R$ 180/h e capacidade de 10 h/semana do "
             "consultor, com 20% de contingência. Aguardam confirmação do Renato antes do envio.")

    h(d, "1. O que entendemos")
    par(d, "A Surcin oferece contabilidade, financeiro (BPO) e jurídico para empresários, com cerca de 40 clientes de "
           "contabilidade, um grupo de clientes de financeiro e uma equipe enxuta: Júlia na entrada e no atendimento, "
           "Vitória no financeiro, Tamara no Departamento Pessoal e Alana no jurídico.")
    par(d, "A empresa já tem processos desenhados, padrão de pastas e rotinas no Trello. O que falta é eficiência e "
           "autonomia: hoje tudo passa pela Thamires, a contabilidade está sem responsável técnico e um erro de "
           "configuração em agosto custou multa e um cliente. O objetivo é escalar com a mesma equipe, liberar tempo "
           "da Thamires até a prova de 13/12 e entrar em 2027 pronta para contratar e voltar a vender.")

    h(d, "2. Objetivos")
    lista(d, [
        "Tirar a Thamires do centro da operação: papéis claros, revisões com critério e dúvidas resolvidas sem ela.",
        "Tornar visíveis os fluxos, gargalos e dependências entre as pessoas.",
        "Redesenhar os processos que mais pesam (fiscal, fechamento financeiro, implantação de clientes, triagem).",
        "Entregar um plano de automação priorizado, com esforço e custo, pronto para orçar a implementação.",
        "Preparar a estrutura para receber um(a) contador(a) em 2027 e para um programa de remuneração variável.",
    ])

    h(d, "3. Abordagem em etapas")
    tabela(d, ["Etapa", "O que é", "Situação"], [
        ["0 · Reunião inicial e diagnóstico preliminar", "Reunião de 12/10/2026 e esta leitura", "Concluída, sem custo"],
        ["1 · Mapeamento dos processos atuais", "Coleta dos passo a passos existentes, entrevistas com a equipe, fluxos atuais, gargalos e dependências", "Nesta proposta"],
        ["2 · Estrutura organizacional", "Organograma atual e proposto, papéis, responsabilidades e indicadores por função", "Nesta proposta"],
        ["3 · Fluxos otimizados e plano de automação", "Redesenho dos processos prioritários e lista de automações com esforço e custo", "Nesta proposta (opção Completa)"],
        ["4 · Implementação e acompanhamento", "Execução das melhorias em pacotes e ajustes mensais", "Proposta futura, a partir de 2027 ou antes, se fizer sentido"],
    ], [4.5, 8, 3.5])

    h(d, "4. Escopo e entregáveis: duas opções")
    tabela(d, ["Entregável", "Essencial", "Completa (recomendada)"], [
        ["Entrevistas (cerca de 1 h cada)", "Até 4 pessoas: Thamires, Júlia, Vitória, Tamara", "Até 5 pessoas (inclui Alana ou outra pessoa indicada)"],
        ["Processos atuais mapeados e validados", "Até 5", "Até 8, entre os 11 identificados"],
        ["Gargalos e matriz de dependências", "Sim", "Sim"],
        ["Inventário das ferramentas e recursos não usados", "Sim", "Sim"],
        ["Estrutura organizacional", "Organograma e matriz de responsabilidades", "Organograma atual e proposto, descrição de papéis e indicadores por função"],
        ["Fluxos otimizados", "Não", "5 processos prioritários"],
        ["Plano de automação", "Lista priorizada, sem estimativa", "Lista priorizada com esforço e custo recorrente estimados"],
        ["Relatório e apresentação executiva", "Sim", "Sim"],
    ], [5.5, 4.5, 6])
    par(d, "Processos candidatos: fiscal mensal, conciliação e fechamento financeiro, implantação de novos clientes, "
           "atendimento e triagem, emissão de notas, pagamentos, folha, comercial, abertura de empresa e "
           "acompanhamento jurídico. A escolha final é feita com a Thamires na primeira semana.")

    h(d, "5. Fora do escopo desta proposta")
    lista(d, [
        "Desenvolvimento, configuração ou integração de automações e sistemas.",
        "Correção da configuração do Domínio (exige o suporte do sistema ou um especialista).",
        "Migração das contas para o novo domínio de e-mail da Surcin.",
        "Desenho do programa de remuneração variável (pesos, metas e valores); a estrutura entrega a base de papéis e indicadores.",
        "Recrutamento e seleção, inclusive do(a) contador(a).",
        "Suporte contínuo, plantão ou atendimento de urgência.",
        "Licenças, assinaturas e custos de ferramentas (sempre por conta da cliente).",
        "Serviços contábeis, fiscais, trabalhistas ou jurídicos.",
    ])

    h(d, "6. Esforço estimado")
    par(d, "Premissas: 2 h por entrevista (1 h de conversa e 1 h de preparação e registro), 2 h por processo mapeado, "
           "2 h por processo redesenhado e 20% de contingência. A documentação existente compensa o tempo de "
           "leitura dos materiais.")
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
    par(d, "A reunião inicial de 12/10/2026 e a preparação desta proposta não são cobradas.")
    par(d, "Referência para a etapa seguinte (não contratada agora): a implementação será orçada em pacotes de preço "
           "fechado. Como ordem de grandeza, pacotes pequenos ficam entre R$ 1.500 e R$ 2.800 e médios entre "
           "R$ 3.500 e R$ 6.500. O acompanhamento mensal, se desejado, parte de R$ 900 por mês com 4 horas.")

    h(d, "8. Cronograma (opção Completa, com aceite até 16/10/2026)")
    par(d, "Cerca de 10 horas por semana do consultor, fora do horário comercial. O calendário respeita as férias da "
           "Vitória (retorno em 28/10), a semana de fechamentos no início de cada mês e a prova da Thamires em 13/12.")
    tabela(d, ["Semana", "Atividades", "Participação da Surcin"], [
        ["19 a 25/10", "Kick-off, coleta dos passo a passos e do Trello, escolha dos processos, entrevistas com Thamires e Júlia", "Thamires 2 h, Júlia 1 h"],
        ["26/10 a 01/11", "Entrevistas com Tamara e Vitória (após o retorno), desenho dos fluxos atuais", "Tamara 1 h, Vitória 1 h"],
        ["02 a 08/11", "Desenho dos fluxos atuais (sem reuniões: semana de fechamentos)", "Nenhuma"],
        ["09 a 15/11", "Validação, gargalos e dependências; entrega do mapeamento", "Equipe 1 h, Thamires 1 h"],
        ["16 a 29/11", "Estrutura organizacional: organogramas, papéis, indicadores", "Thamires 1 h"],
        ["30/11 a 13/12", "Fluxos otimizados e plano de automação (trabalho do consultor; sem reuniões na semana da prova)", "Validação por escrito"],
        ["14 a 18/12", "Apresentação final e proposta de implementação", "Thamires 2 h"],
    ], [2.8, 9, 4.2])
    par(d, "Opção Essencial: de 19/10 a cerca de 22/11, com entrega única no fim.")

    h(d, "9. Responsabilidades")
    h(d, "Do consultor", 3)
    lista(d, [
        "Conduzir entrevistas, análises e reuniões nas datas combinadas.",
        "Entregar os documentos de cada etapa em formato editável, no OneDrive da Surcin.",
        "Manter sigilo sobre dados da empresa e de seus clientes, com acordo de confidencialidade.",
        "Avisar com antecedência qualquer risco de atraso ou mudança de escopo.",
        "Responder mensagens em até 1 dia útil.",
    ])
    h(d, "Da cliente", 3)
    lista(d, [
        "Indicar a Júlia (ou outra pessoa) como ponto focal para acessos e agenda.",
        "Liberar acesso de leitura ao Trello, à pasta Geral do OneDrive e aos passo a passos.",
        "Liberar a equipe para entrevistas de cerca de 1 hora, de preferência antes das 10h30, no almoço ou após as 19h30.",
        "Responder dúvidas em até 2 dias úteis e validar entregas em até 5 dias úteis.",
        "Tomar as decisões de priorização ao fim de cada etapa.",
    ])

    h(d, "10. Condições gerais")
    lista(d, [
        "Reuniões preferencialmente online, nas janelas acima.",
        "Atrasos por falta de retorno ou de acesso deslocam o cronograma pelo mesmo período; pausas de mais de 10 dias reagendam o projeto.",
        "Mudanças de escopo são orçadas à parte e só executadas após aprovação por escrito.",
        "Os documentos produzidos passam a ser da cliente após a quitação de cada parcela correspondente.",
        "Validade desta proposta: 15 dias a partir de 15/10/2026.",
    ])

    h(d, "11. Próximos passos")
    lista(d, [
        "Escolha da opção (Essencial ou Completa) e aceite.",
        "Assinatura do acordo de confidencialidade.",
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

    h(d, "1. O que mudou com a transcrição")
    lista(d, [
        "A equipe é de 4 pessoas além da Thamires (Júlia, Vitória, Tamara e a estagiária Alana), e não há contador.",
        "Os processos já estão em boa parte documentados no Trello e no OneDrive: o projeto parte do que existe.",
        "As dores concretas são centralização, risco no fiscal (erro de agosto), fechamento financeiro lento e falta de métricas para a remuneração variável.",
        "O cronograma agora tem datas reais: Vitória volta em 28/10, prova da Thamires em 13/12, meta de terminar antes de janeiro.",
        "O preço não mudou: 4 a 5 entrevistas e 8 processos cabem nas opções Essencial e Completa.",
    ])

    h(d, "2. Decisões e revisões que só você pode fazer")
    tabela(d, ["#", "Decisão", "Padrão adotado"], [
        ["1", "Taxa-piso da sua hora", "Cerca de R$ 180/h; R$ 220/h para hora avulsa"],
        ["2", "Capacidade semanal sustentável", "10 h/semana, com 20% de contingência"],
        ["3", "Preço das opções", "Essencial R$ 7.800; Completa R$ 14.800"],
        ["4", "Parcelamento", "Ela tem caixa só até novembro e você disse que valores são conversáveis (02:07). Considerar parcelar a Completa em 4 vezes até janeiro"],
        ["5", "Oferecer o desenho do programa de remuneração variável como adicional", "Fora do escopo; estrutura entrega a base"],
        ["6", "Horários das entrevistas", "A equipe trabalha em horário comercial; confirmar se aceitam antes das 10h30 ou no almoço"],
        ["7", "Horário da reunião de quinta à noite", "A combinar com ela pelo WhatsApp"],
        ["8", "Marca e contato na proposta", "\"R2 Tech Consulting\" aparece como seu nome na reunião; confirmar sobrenome, e-mail e telefone"],
        ["9", "Cláusula de exclusividade no seu emprego", "Verificar antes de assinar"],
    ], [0.8, 6, 9.2])

    h(d, "3. Plano até quinta")
    tabela(d, ["Quando", "O que fazer", "Tempo"], [
        ["Terça 13/10 · noite", "Ler o diagnóstico (doc 01) e conferir os pontos [CONFIRMAR]", "1 h"],
        ["Quarta 14/10 · manhã", "Revisar a estrutura (doc 02) e a proposta (doc 04)", "1 h"],
        ["Quarta 14/10 · noite", "Fechar as decisões acima e ensaiar com os slides (doc 06)", "2 h"],
        ["Quinta 15/10 · noite", "Apresentar e fazer as perguntas da seção 8 do doc 01", "1 h"],
    ], [3.5, 10, 2.5])

    h(d, "4. Roteiro da apresentação (cerca de 40 minutos)")
    lista(d, [
        ("1. Abertura (2 min). ", "Agradecer a conversa e dizer que ela já é o diagnóstico preliminar, sem custo."),
        ("2. O que eu entendi (8 min). ", "Os números, a equipe e as dores nas palavras dela. Destacar: \"você já tem processo, falta eficiência\"."),
        ("3. Como vamos trabalhar (5 min). ", "Etapas 0 a 4. Partir do que existe, entender antes de automatizar."),
        ("4. Estrutura organizacional (7 min). ", "Estrutura atual e hipótese proposta. Pedir que ela corrija."),
        ("5. Mapeamento (5 min). ", "Os 11 processos identificados e a prioridade inicial."),
        ("6. Opções e cronograma (5 min). ", "Essencial e Completa, com datas que respeitam a prova."),
        ("7. Investimento (5 min). ", "Valores, parcelamento e o que fica fora."),
        ("8. Próximos passos (3 min). ", "Aceite, confidencialidade, kick-off em 19/10."),
    ])

    h(d, "5. Possíveis objeções e respostas")
    tabela(d, ["Se ela disser", "Resposta sugerida"], [
        ["O caixa está apertado até janeiro.", "Começar pela Essencial ou parcelar a Completa. A Essencial já entrega mapeamento, gargalos e organograma antes da prova."],
        ["Já tenho os processos, por que mapear?", "Justamente por isso o trabalho é mais rápido. O mapeamento mostra onde o processo trava e o que pode sair das suas mãos."],
        ["Quero logo as automações.", "Automatizar um processo que depende de você só acelera o problema. A Completa entrega o plano com esforço e custo, para começar a implementação em seguida."],
        ["Não tenho tempo por causa da prova.", "O cronograma pede cerca de 7 horas suas no total, concentradas em outubro e novembro, sem reuniões na semana da prova."],
        ["E a remuneração por pontos?", "Ela depende de papéis e indicadores claros, que saem da Etapa 2. O desenho do programa pode vir depois."],
    ], [5.5, 10.5])
    d.save(f"{SAIDA}/05-roteiro-apresentacao-e-decisoes.docx")


if __name__ == "__main__":
    diagnostico()
    estrutura()
    metodologia()
    proposta()
    roteiro()
    print("ok")
