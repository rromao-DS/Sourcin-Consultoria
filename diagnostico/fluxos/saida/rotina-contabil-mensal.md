# Análise do processo: Rotina mensal da contabilidade · rascunho

Captura dos XML, apuração, contabilidade, emissão da guia e conferência do pagamento.
No "mundo ideal" tudo seria feito no Domínio, com a Veri nos envios ao cliente (01:18:43).


> Relatório gerado automaticamente pelo `mapeador.py` a partir da descrição do
> processo em TOML. O diagrama correspondente está no arquivo `.bpmn`.

## Indicadores

| Indicador | Valor |
| --- | --- |
| Etapas mapeadas | 9 |
| Tempo de execução (mão de obra) | 0 min |
| Tempo de espera | 0 min |
| **Lead time total** | **0 min** |
| Trocas de área (handoffs) | 3 |
| Etapas automatizáveis | 0 de 6 (0%) |
| Ganho estimado com automação | 0 min por ciclo |

## Etapas

| # | Etapa | Área | Tipo | Execução | Espera | Sistema |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Início do mês | Júlia | Início | 0 min | 0 min | - |
| 2 | Retirar os arquivos XML no portal | Júlia | Tarefa | 0 min | 0 min | Portal (qual, a confirmar) |
| 3 | Fazer a apuração | Thamires | Tarefa | 0 min | 0 min | Domínio ou por fora |
| 4 | Fazer a contabilidade | Thamires | Tarefa | 0 min | 0 min | Domínio ou por fora |
| 5 | Tirar o imposto (DAS) e disponibilizar ao cliente | Thamires | Tarefa | 0 min | 0 min | Veri |
| 6 | Pagar a guia | Cliente | Tarefa | 0 min | 0 min | Aplicativo da Veri |
| 7 | Cliente pagou? | Thamires | Decisão | 0 min | 0 min | Veri |
| 8 | Cobrar o cliente | Thamires | Tarefa | 0 min | 0 min | - |
| 9 | Obrigação feita e atualizada | Thamires | Fim | 0 min | 0 min | - |

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
