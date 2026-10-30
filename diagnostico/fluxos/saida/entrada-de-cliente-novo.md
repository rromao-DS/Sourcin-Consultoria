# Análise do processo: Entrada de cliente novo (contabilidade e financeiro) · rascunho

Do primeiro contato à criação das tarefas no Trello. Checklist já existe no Trello e,
segundo a Thamires, precisa ser atualizado. O cliente do financeiro tem passos a mais:
planilha, Trello e Conta Azul (00:55:16).


> Relatório gerado automaticamente pelo `mapeador.py` a partir da descrição do
> processo em TOML. O diagrama correspondente está no arquivo `.bpmn`.

## Indicadores

| Indicador | Valor |
| --- | --- |
| Etapas mapeadas | 15 |
| Tempo de execução (mão de obra) | 0 min |
| Tempo de espera | 0 min |
| **Lead time total** | **0 min** |
| Trocas de área (handoffs) | 6 |
| Etapas automatizáveis | 0 de 9 (0%) |
| Ganho estimado com automação | 0 min por ciclo |

## Etapas

| # | Etapa | Área | Tipo | Execução | Espera | Sistema |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Cliente chega | Cliente | Início | 0 min | 0 min | - |
| 2 | Marcar reunião de apresentação | Júlia | Tarefa | 0 min | 0 min | Google Agenda [hipótese] |
| 3 | Preparar a proposta | Júlia | Tarefa | 0 min | 0 min | Canva |
| 4 | Fazer a reunião e enviar a proposta | Thamires | Tarefa | 0 min | 0 min | - |
| 5 | Cliente fechou? | Cliente | Decisão | 0 min | 0 min | - |
| 6 | Enviar os dados para o contrato e reforçar os serviços | Júlia | Tarefa | 0 min | 0 min | - |
| 7 | Criar o grupo com o cliente | Júlia | Tarefa | 0 min | 0 min | WhatsApp / Nestzap |
| 8 | Abrir a pasta do cliente e salvar a documentação | Júlia | Tarefa | 0 min | 0 min | OneDrive |
| 9 | Falta algum documento? | Júlia | Decisão | 0 min | 0 min | - |
| 10 | Pedir o que falta [hipótese: canal não informado] | Cliente | Tarefa | 0 min | 0 min | - |
| 11 | É cliente do financeiro? | Júlia | Decisão | 0 min | 0 min | - |
| 12 | Abrir planilha, criar no Trello e abrir o Conta Azul | Júlia | Tarefa | 0 min | 0 min | Planilha, Trello, Conta Azul |
| 13 | Criar a tarefa no Trello por responsável | Júlia | Tarefa | 0 min | 0 min | Trello |
| 14 | Não fechou | Cliente | Fim | 0 min | 0 min | - |
| 15 | Cliente implantado | Júlia | Fim | 0 min | 0 min | - |

## Oportunidades de automação

Nenhuma etapa foi marcada como automatizável na descrição.

## Gargalos (maior tempo de espera)

Nenhuma etapa tem tempo de espera acima da média das tarefas.

## Como ler estes números

- **Tempo de execução** é o trabalho efetivo; **espera** é o tempo parado em fila
  ou aguardando terceiros. O lead time é a soma dos dois — e é o que o usuário
  sente.
- **Handoff** é cada passagem do processo de uma área para outra. Quanto mais
  trocas, maior a chance de retrabalho e de perda de informação.
- **Ganho estimado** é conservador: considera 70% do tempo da etapa automatizada.
