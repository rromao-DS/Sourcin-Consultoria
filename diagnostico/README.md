# Base do diagnóstico · Surcin

Montada em 30/10/2026, antes do início em 03/11, com o que já temos: a reunião de 12/10 (transcrição, que prevalece), o briefing de 14 páginas, as anotações do Gemini, a exportação do Trello de 14/10 e os documentos 01 a 05 da proposta. Nenhum acesso aos sistemas da Surcin foi usado.

A ideia é ir alimentando esta base a cada entrevista, demonstração e check-in, sem refazer nada.

## O que tem aqui

| Arquivo | Para quê |
|---|---|
| `00-pauta-reuniao-abertura.md` | Pauta da reunião de abertura com a Thamires (03/11) |
| `pedido-de-acessos-julia.md` | Texto pronto do pedido de acessos à Júlia, para enviar depois do contrato assinado |
| `como-gravar-e-registrar.md` | Como gravar as conversas e gerar os registros pelo Claude na aba Registros do Acompanhamento |
| `entrevistas/roteiros-por-pessoa.md` | Roteiro comum e perguntas específicas para Thamires, Júlia, Vitória, Tamara e Alana |
| `fichas/modelo-ficha-de-processo.md` | Ficha a preencher para cada processo mapeado (até 8) |
| `fluxos/rascunhos/*.toml` | Fluxos atuais em rascunho, descritos a partir da reunião |
| `fluxos/saida/` | Diagrama BPMN, relatório e painel gerados de cada rascunho |

## Onde fica a base

A base viva (fatos, hipóteses, dúvidas, riscos e processos) fica na aba **Registros** do [Acompanhamento Surcin](https://claude.ai/artifact/17KBx6snPCL7ziRDyNhECe), alimentada pelas transcrições das conversas. A planilha inicial foi migrada para lá em 30/10 e removida.

## Regras para alimentar

1. Todo item novo leva um rótulo: **FATO** (alguém da Surcin disse ou mostrou), **HIPÓTESE** (leitura nossa, a confirmar) ou **DÚVIDA** (pergunta em aberto).
2. Todo item leva a fonte: reunião com minuto (ex.: `12/10 01:20`), entrevista com nome e data, briefing com seção, demonstração com sistema e data.
3. Se duas fontes divergem, vale o que a pessoa disse na reunião ou na entrevista. A divergência fica registrada na aba Fatos, com as duas versões.
4. Uma dúvida respondida vira fato: muda o status para "respondida", anota a resposta e a fonte, e copia para Fatos.
5. Tempos só entram quando a pessoa informar ou quando medirmos numa demonstração. Nada de estimativa sem rótulo.
6. Dados de clientes da Surcin não entram aqui. Use nomes genéricos (Cliente A, Cliente B).
7. Questões de pessoal e de caixa da empresa ficam fora de qualquer material que vá para a equipe.

## Fluxos (mapeador de processos)

Os fluxos ficam em TOML, um arquivo por processo, no formato do [mapeador-de-processos](../ferramentas/mapeador-de-processos/ORIGEM.md) (MIT). Para gerar de novo depois de editar:

```
python3 ferramentas/mapeador-de-processos/mapeador.py diagnostico/fluxos/rascunhos/*.toml --saida diagnostico/fluxos/saida
```

Os três rascunhos atuais não têm tempos, porque a reunião não informou. Os totais dos relatórios saem zerados por isso. Depois da entrevista, preencha `tempo_min` e `espera_min` e rode de novo.

| Rascunho | Fonte | Falta confirmar |
|---|---|---|
| Entrada de cliente novo | 12/10 00:55:16, 01:22:40 | Quem faz cada passo antes do fechamento; canal do pedido de documentos; tempos |
| Rotina mensal da contabilidade | 12/10 01:18:43 a 01:20:00 | Divisão entre Júlia e Thamires; qual portal; tempos por etapa |
| Conciliação e pagamentos do financeiro | 12/10 01:20:00 a 01:22:40 | Onde fica o controle de pagamentos fixos; formato do resumo ao cliente; tempos |

## Próximos fluxos (Etapa 1, até 8 no total)

Ordem pela prioridade inicial do documento 03: fiscal mensal em detalhe, fechamento financeiro com reunião de resultado, atendimento e triagem de demandas, emissão de notas, folha e DP. A escolha final sai das entrevistas, validada com a Thamires.
