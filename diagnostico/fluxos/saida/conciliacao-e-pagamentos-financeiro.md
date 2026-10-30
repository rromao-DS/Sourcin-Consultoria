# Análise do processo: Financeiro: conciliação e pagamentos · rascunho

Configurar os bancos no Conta Azul, conciliar, importar o extrato e organizar entradas,
saídas e plano de contas personalizado. Nos dias de pagamento, ver o que vence, pagar e
mandar o resumo ao cliente. Pagamentos fixos de cada cliente ainda não estão 100% no Conta Azul.


> Relatório gerado automaticamente pelo `mapeador.py` a partir da descrição do
> processo em TOML. O diagrama correspondente está no arquivo `.bpmn`.

## Indicadores

| Indicador | Valor |
| --- | --- |
| Etapas mapeadas | 10 |
| Tempo de execução (mão de obra) | 0 min |
| Tempo de espera | 0 min |
| **Lead time total** | **0 min** |
| Trocas de área (handoffs) | 2 |
| Etapas automatizáveis | 0 de 7 (0%) |
| Ganho estimado com automação | 0 min por ciclo |

## Etapas

| # | Etapa | Área | Tipo | Execução | Espera | Sistema |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Mês do cliente em aberto | Vitória | Início | 0 min | 0 min | - |
| 2 | Configurar os bancos do cliente | Vitória | Tarefa | 0 min | 0 min | Conta Azul |
| 3 | Conciliar e importar o extrato | Vitória | Tarefa | 0 min | 0 min | Conta Azul |
| 4 | Classificar entradas e saídas no plano de contas personalizado | Vitória | Tarefa | 0 min | 0 min | Conta Azul |
| 5 | É terça ou sexta (dia de pagamento)? | Vitória | Decisão | 0 min | 0 min | - |
| 6 | Ver o que há para pagar (valor, forma, chave) | Vitória | Tarefa | 0 min | 0 min | Controle por cliente, fora do Conta Azul |
| 7 | Fazer os pagamentos | Vitória | Tarefa | 0 min | 0 min | - |
| 8 | Montar e enviar o resumo do dia (a pagar e saldo) | Vitória | Tarefa | 0 min | 0 min | - |
| 9 | Receber o resumo | Cliente | Tarefa | 0 min | 0 min | - |
| 10 | Dia encerrado | Vitória | Fim | 0 min | 0 min | - |

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
