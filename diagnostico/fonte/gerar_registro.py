# -*- coding: utf-8 -*-
"""Gera a planilha inicial do diagnóstico da Surcin (30/10/2026).

Uso: python gerar_registro.py <arquivo .xlsx de saída>
Dados semeados a partir do diagnóstico preliminar (doc 01) e da metodologia (doc 03), com fonte em cada linha.
Depois de gerada, a planilha é alimentada à mão; rodar de novo sobrescreve tudo.
"""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation

SAIDA = sys.argv[1] if len(sys.argv) > 1 else "registro-diagnostico.xlsx"
AZUL = PatternFill("solid", fgColor="1F3A5F")
ROTULOS = '"FATO,HIPÓTESE,DÚVIDA"'

FATOS = [
    ["F01", "Empresa", "Três CNPJs: contabilidade, financeiro e jurídico", "FATO", "12/10 01:02", ""],
    ["F02", "Carteira", "Cerca de 40 a 45 empresas no fiscal/contábil; o fiscal do mês passado cobriu 44", "FATO", "12/10 01:55, 02:00; briefing 3", ""],
    ["F03", "Carteira", "Clientes do financeiro: 12 (00:38); 11, 13 e 16 na contagem do Trello (01:02); briefing diz 14 a 15", "DÚVIDA", "12/10 00:38, 01:02; briefing", "Confirmar com a Vitória"],
    ["F04", "Carteira", "DP: cerca de 25 vidas, em 4 ou 5 clientes com funcionários", "FATO", "12/10 00:40", ""],
    ["F05", "Carteira", "Jurídico: cerca de 20 processos legados em fase final", "FATO", "12/10 00:43, 01:45", ""],
    ["F06", "Fiscal", "Desde agosto a Thamires executa o fiscal; não há ninguém na contabilidade", "FATO", "12/10 00:30, 00:40, 02:00", ""],
    ["F07", "Fiscal", "Fiscal de 44 clientes feito em 3 dias, 3 a 4 h por dia", "FATO", "12/10 02:00", "Gemini diz 3 h fracionadas; vale a reunião"],
    ["F08", "Sistemas", "Domínio com parametrização errada desde a migração; fiscal feito direto no portal", "FATO", "12/10 01:17", ""],
    ["F09", "Financeiro", "Conciliação toda pelo Conta Azul; antes era planilha manual", "FATO", "12/10 01:20:00", ""],
    ["F10", "Financeiro", "Pagamentos toda terça e sexta-feira", "FATO", "12/10 01:21:27", ""],
    ["F11", "Financeiro", "Pagamentos fixos de cada cliente ainda não estão 100% no Conta Azul", "FATO", "12/10 01:21:27", ""],
    ["F12", "Financeiro", "Plano de contas personalizado por cliente, a partir de um padrão", "FATO", "12/10 01:21:27", ""],
    ["F13", "Financeiro", "Conciliação passa a ser semanal", "FATO", "12/10 (decisões já tomadas, doc 01 seção 2)", ""],
    ["F14", "Financeiro", "Fechamento com IA caiu de 5 h para 1 a 2 h", "FATO", "12/10 00:34", "Gemini diz 1 h 30; vale a reunião"],
    ["F15", "Implantação", "Checklist de novo cliente pronto no Trello; precisa atualizar. Depois do fechamento, quem faz é a Júlia", "FATO", "12/10 00:55:16", ""],
    ["F16", "Implantação", "Cliente do financeiro exige planilha, Trello e Conta Azul além dos passos comuns", "FATO", "12/10 00:55:16", ""],
    ["F17", "Comercial", "Júlia faz as propostas no Canva, a partir de modelos", "FATO", "12/10 01:22:40", ""],
    ["F18", "Atendimento", "Comunicação com clientes de contabilidade só pelo aplicativo da Veri a partir de novembro", "FATO", "12/10 01:16", ""],
    ["F19", "Acessos", "A Thamires indicou a Júlia para dar acessos e informações", "FATO", "12/10 02:09:48", ""],
    ["F20", "Acessos", "A Thamires quer recriar tudo no domínio novo da Surcin (hoje Trello, nuvem e Claude estão como RT)", "FATO", "12/10 02:09:48, 02:10:41", ""],
    ["F21", "Pessoas", "Vitória assume o financeiro integralmente a partir de novembro", "FATO", "12/10 01:34; briefing 5", ""],
    ["F22", "Pessoas", "Tamara fica exclusiva no DP a partir de novembro", "FATO", "12/10 00:41", "Briefing inclui notas; confirmar quem emite"],
]

PROCESSOS = [
    ["P01", "Atendimento e triagem de demandas (WhatsApp, Nestzap, Veri)", "Júlia", "Pedidos podem se perder em grupos e planilhas", "Alta", "Diário", "Médio", "2"],
    ["P02", "Comercial: primeiro atendimento, proposta, reunião, contrato", "Júlia e Thamires", "Checklist e modelos prontos; retomada em 2027", "Média", "Baixo agora", "Baixo", "3"],
    ["P03", "Implantação de novo cliente (contábil e financeiro)", "Júlia e Vitória", "Checklists prontos, a atualizar · rascunho de fluxo pronto", "Média", "Cresce com vendas", "Médio", "2"],
    ["P04", "Abertura, alteração e baixa de empresas", "Júlia, Alana, Thamires", "Checklist no Trello; abertura em Campinas gravada", "Baixa", "Eventual", "Médio", "3"],
    ["P05", "Fiscal mensal: captura, conferência, apuração, guia, envio, evidência", "Thamires e Júlia", "Maior risco: parâmetros (ISS, regime, Fator R) · rascunho de fluxo pronto", "Alta", "44 clientes/mês", "Alto (multa)", "1"],
    ["P06", "Pedidos de pagamento e pagamentos dos clientes do financeiro", "Vitória", "Pedidos por WhatsApp; risco de guia do cliente errado · rascunho de fluxo pronto", "Média", "2x por semana", "Médio", "3"],
    ["P07", "Emissão de notas fiscais", "Tamara e Vitória", "Feita por fora do Conta Azul", "Média", "Recorrente", "Médio", "2"],
    ["P08", "Conciliação e fechamento mensal com reunião de resultado", "Vitória e Thamires", "Passando a semanal · rascunho de conciliação pronto", "Alta", "12 a 16 clientes/mês", "Médio", "1"],
    ["P09", "Folha, admissões, rescisões, eSocial", "Tamara", "Volume baixo; pendências antigas", "Baixa", "25 vidas", "Médio", "3"],
    ["P10", "Acompanhamento de processos jurídicos", "Alana e Thamires", "Revisão manual", "Baixa", "20 processos", "Alto (prazos)", "3"],
    ["P11", "Rotinas transversais: EFD-Reinf, IRPF, parcelamentos", "A definir", "Citadas no briefing", "Baixa", "Anual e mensal", "Médio", "3"],
]

SISTEMAS = [
    ["Trello", "Rotinas por pessoa, pendências, checklists", "Exportação de 14/10 (só leitura, sem atualização)", "Convite de observador", "Júlia"],
    ["OneDrive / Microsoft 365", "Pastas por serviço e por cliente, passo a passos, modelos", "Nenhum", "Link de leitura da pasta Geral", "Júlia"],
    ["Google Agenda", "Agenda central da operação", "Nenhum", "Não precisa", "Júlia"],
    ["WhatsApp + Nestzap", "Número único com vários usuários; grupos com clientes", "Nenhum", "Demonstração em tela", "Júlia"],
    ["Veri", "Aplicativo do cliente: guias, certidões, documentos", "Nenhum", "Demonstração em tela", "Júlia ou Thamires"],
    ["Domínio", "Contábil, fiscal e folha; parametrização com erro", "Nenhum", "Demonstração em tela", "Thamires"],
    ["Portal da Receita", "Fiscal feito direto no portal", "Nenhum", "Demonstração em tela", "Thamires ou Júlia"],
    ["Conta Azul", "Conciliação e dados dos clientes do financeiro", "Nenhum", "Demonstração em tela", "Vitória"],
    ["Jusbrasil", "IA jurídica e modelos; monitoramento não configurado", "Nenhum", "Demonstração em tela", "Alana"],
    ["CITAX", "Em avaliação para captura e apuração fiscal", "Nenhum", "Só se entrar na decisão do Domínio", "Thamires"],
    ["Canva e PowerPoint", "Propostas (Canva) e fechamentos (PowerPoint)", "Nenhum", "Exemplos, se úteis", "Júlia"],
    ["Claude e Lovable", "Testes do fechamento financeiro, em conta RT; plano de ambiente novo Surcin", "Nenhum", "Ver o prompt atual do fechamento", "Thamires"],
]

PESSOAS = [
    ["Thamires", "Direção, clientes, jurídico, societário, análises financeiras e execução do fiscal", "Precisa reduzir o envolvimento operacional", "12/10 00:18, 00:30", "[agendar]"],
    ["Júlia", "Secretaria, atendimento, agenda, OneDrive, Trello, propostas, implantação, apoio fiscal e societário", "Ponto focal indicado; ponto único de falha [hipótese]", "12/10 00:15 a 00:19, 02:09:48", "[agendar]"],
    ["Vitória", "Financeiro: pagamentos, notas, conciliação, preparação dos fechamentos", "Assume o financeiro integral em novembro", "12/10 00:13, 01:34", "[agendar]"],
    ["Tamara", "DP a partir de novembro (em outubro também conciliação e notas)", "Confirmar quem emite as notas", "12/10 00:41", "[agendar]"],
    ["Alana", "Estagiária do jurídico e do societário, dois dias por semana", "", "12/10 00:42, 01:40", "[agendar]"],
]

DUVIDAS = [
    ["D01", "Quantos clientes o financeiro atende hoje, sem contar as três empresas da Thamires?", "Vitória", "entrevista"],
    ["D02", "A partir de novembro, quem emite as notas dos clientes contábeis: Tamara ou Vitória?", "Thamires", "abertura"],
    ["D03", "Qual processo, resolvido primeiro, mais devolve o tempo da Thamires?", "Thamires", "abertura"],
    ["D04", "A Júlia confirma como ponto focal do projeto?", "Thamires", "abertura"],
    ["D05", "Os convites de acesso vão para o e-mail da R2 ou para uma conta no domínio novo da Surcin?", "Thamires", "abertura"],
    ["D06", "Quem corrige a parametrização do Domínio, e até quando? O CITAX entra na decisão?", "Thamires", "entrevista"],
    ["D07", "Quando o ambiente novo da Surcin (e-mail, Claude, Lovable) será criado e por quem?", "Thamires", "abertura"],
    ["D08", "Na rotina contábil, como se dividem hoje as etapas entre Júlia e Thamires?", "Júlia e Thamires", "entrevista"],
    ["D09", "De quais portais saem os XML, e para quantos clientes?", "Júlia", "entrevista"],
    ["D10", "Onde ficam os pagamentos fixos de cada cliente fora do Conta Azul?", "Vitória", "entrevista"],
    ["D11", "Qual o formato do resumo de pagamentos enviado ao cliente?", "Vitória", "entrevista"],
    ["D12", "Na entrada de cliente novo, quem marca a reunião e por qual canal se pede o documento que falta?", "Júlia", "entrevista"],
    ["D13", "Como os prazos dos processos jurídicos são acompanhados hoje?", "Alana", "entrevista"],
    ["D14", "Quais horários, entre 9h e 12h, cada pessoa tem livres de 09 a 13/11?", "Júlia", "pedido de acessos"],
]

RISCOS = [
    ["R01", "Parâmetro fiscal errado (ISS de outro município, regime municipal, Fator R) gera imposto errado e multa", "Fiscal", "FATO (ocorreu)", "12/10 00:26 a 00:29; briefing 4.1", "Separar execução de conferência; checklist de parâmetros"],
    ["R02", "Guia de um cliente salva na pasta de outro, encontrada só na hora de pagar", "Documentos e pagamentos", "FATO (ocorreu)", "briefing 4.2", "Conferência de guia antes de pagar"],
    ["R03", "Cartão do Trello concluído sem documento, ou documento sem cartão atualizado", "Controle", "FATO", "briefing 4.3", "Evidência obrigatória para concluir"],
    ["R04", "Revisões e dúvidas concentradas na Thamires", "Gestão", "FATO", "12/10 00:18", "Critérios escritos; registro das dúvidas"],
    ["R05", "Júlia como ponto único de falha na triagem e na implantação", "Operação", "HIPÓTESE", "doc 01 seção 9", "Substituto e passo a passo"],
    ["R06", "Pedidos de pagamento por WhatsApp podem se perder", "Financeiro", "HIPÓTESE", "doc 01 seção 5", "Canal único por tipo de demanda"],
    ["R07", "Fechamento financeiro concentrado no fim do mês, reuniões de resultado atrasadas", "Financeiro", "FATO", "12/10 01:31", "Conciliação semanal"],
]


def aba(wb, titulo, cabecalho, linhas, larguras, col_rotulo=None, primeira=False):
    ws = wb.active if primeira else wb.create_sheet()
    ws.title = titulo
    ws.append(cabecalho)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = AZUL
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for linha in linhas:
        ws.append(linha)
    for i, w in enumerate(larguras):
        ws.column_dimensions[chr(65 + i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
    if col_rotulo:
        dv = DataValidation(type="list", formula1=ROTULOS, allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(f"{col_rotulo}2:{col_rotulo}500")
    return ws


def main():
    wb = Workbook()
    aba(wb, "Fatos", ["ID", "Tema", "Fato", "Rótulo", "Fonte", "Observação / divergência"],
        FATOS, [6, 14, 60, 11, 28, 34], col_rotulo="D", primeira=True)
    ws = aba(wb, "Processos",
             ["ID", "Processo", "Quem executa", "Situação", "Dor (doc 03)", "Volume (doc 03)", "Risco (doc 03)",
              "Prioridade inicial [HIPÓTESE]", "Dor 1-5", "Volume 1-5", "Risco 1-5", "Facilidade 1-5", "Total",
              "Mapear na Etapa 1?", "Fonte"],
             [p + ["", "", "", "", "", "", "doc 01 seção 5; doc 03 seção 3"] for p in PROCESSOS],
             [6, 44, 18, 40, 9, 16, 13, 12, 8, 9, 8, 10, 8, 11, 24])
    for r in range(2, len(PROCESSOS) + 2):
        ws[f"M{r}"] = f'=IF(COUNT(I{r}:L{r})=4,SUM(I{r}:L{r}),"")'
    aba(wb, "Sistemas e acessos", ["Sistema", "Uso atual", "Acesso que a R2 tem hoje", "Acesso a pedir", "Quem libera",
                                    "Status", "Data"],
        [s + ["pendente", ""] for s in SISTEMAS], [22, 44, 26, 26, 16, 12, 12])
    aba(wb, "Pessoas", ["Pessoa", "Função", "Observação", "Fonte", "Entrevista (data e hora)", "Processos que executa"],
        [p + [""] for p in PESSOAS], [12, 50, 36, 22, 18, 30])
    aba(wb, "Dúvidas", ["ID", "Pergunta", "Para quem", "Quando perguntar", "Status", "Resposta", "Fonte da resposta"],
        [d + ["aberta", "", ""] for d in DUVIDAS], [6, 60, 16, 16, 11, 40, 20])
    aba(wb, "Riscos", ["ID", "Risco", "Área", "Rótulo", "Fonte", "Controle provável [HIPÓTESE]"],
        RISCOS, [6, 56, 18, 14, 26, 36])
    wb.save(SAIDA)
    print("ok", SAIDA)


if __name__ == "__main__":
    main()
