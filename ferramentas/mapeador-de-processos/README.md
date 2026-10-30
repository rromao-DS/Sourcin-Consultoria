# Mapeador de processos

[![Python](https://img.shields.io/badge/Python-3.11%2B-0F5C55?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Licença: MIT](https://img.shields.io/badge/Licen%C3%A7a-MIT-0F5C55?style=flat-square)](LICENSE)
[![Testes](https://img.shields.io/badge/testes-16%20passando-0F5C55?style=flat-square)](#testes)

Transforma a **descrição de um processo de negócio** em três coisas:

1. um **diagrama BPMN 2.0** que abre no [bpmn.io](https://bpmn.io/) ou no Camunda Modeler;
2. um **relatório de análise** com tempos, gargalos e oportunidades de automação;
3. um **painel de indicadores** para abrir no navegador.

A ideia é simples: a mesma descrição que serve de ata de reunião vira diagrama e
números, sem ninguém desenhar caixinha à mão.

---

## O problema que isso resolve

Mapear processo costuma virar uma planilha que envelhece na primeira mudança, ou um
diagrama desenhado à mão que ninguém consegue reproduzir.

Aqui, o processo é **texto**. Se ele está no texto, dá para versionar, revisar em
reunião, comparar o antes e o depois — e o desenho e os indicadores saem sozinhos.

## Exemplo: um chamado de suporte de TI

A descrição do processo (`processos/chamado-suporte-ti.toml`) gera isto:

```
Abertura e tratamento de chamado de suporte de TI
  lead time ............. 2.1 dias
  trocas de área ........ 5
  etapas automatizáveis . 3 de 7
  ganho estimado ........ 13 min por ciclo
```

E o relatório abre assim:

| Indicador | Valor |
| --- | --- |
| Tempo de execução (mão de obra) | 2.9 h |
| Tempo de espera | 2.0 dias |
| **Lead time total** | **2.1 dias** |
| Trocas de área (handoffs) | 5 |
| Etapas automatizáveis | 3 de 7 (43%) |

O diagrama correspondente é este (gerado, abrível no bpmn.io):

```
Usuário            ┌────────┐   ┌──────────────┐
                   │Problema│──▶│Abrir chamado │
                   └────────┘   └──────┬───────┘
                                         │
Service Desk       ┌────────────────────▼─────┐   ┌──────────┐      Sim   ┌───────────┐
                   │Triar e classificar       │──▶│Resolvido?│────────────▶│  Resolver │
                   └──────────────────────────┘   └────┬─────┘            └─────┬─────┘
                                                       Não                     │
                                     ┌───────────────────┘                      │
                                     ▼                                          │
Equipe Técnica     ┌──────────────────┐   ┌──────────────────┐    Não           │
                   │Encaminhar (N2)   │──▶│Diagnosticar      │──▶ ...           │
                   └──────────────────┘   └────────┬─────────┘                  │
                                                     │ Sim                      │
Gestão de TI       ┌──────────────────────────────────▼───┐                    │
                   │Comprar peça ou acionar fornecedor     │                    │
                   └───────────────────────┬───────────────┘                   │
                                            ▼                                   ▼
Service Desk                          ┌──────────────────────────────────────────┐
                                      │ Encerrar o chamado e confirmar com o usuário│──▶ Fim
                                      └──────────────────────────────────────────┘
```

> O desenho de verdade é o arquivo `.bpmn`. O esquema acima é só para você entender a
> ideia sem abrir nada.

---

## Como usar

Precisa só de **Python 3.11 ou superior**. Não tem nada para instalar.

```bash
python mapeador.py processos/chamado-suporte-ti.toml
```

Isso cria, na pasta `saida/`:

| Arquivo | Para que serve |
| --- | --- |
| `chamado-suporte-ti.bpmn` | O diagrama. Abra em <https://bpmn.io/> (arraste o arquivo para a página) |
| `chamado-suporte-ti.md` | O relatório de análise, em Markdown |
| `chamado-suporte-ti.html` | O painel de indicadores. Abra com dois cliques |

Para gerar vários processos de uma vez:

```bash
python mapeador.py "processos/*.toml" --saida saida
```

> O curinga `*` funciona no Linux, no macOS e também no Windows — a ferramenta expande
> o padrão internamente.

## Os dois exemplos que vêm no projeto

| Processo | O que mostra |
| --- | --- |
| `processos/chamado-suporte-ti.toml` | Um processo de suporte, comentado linha a linha — é o melhor para aprender o formato |
| `processos/compra-de-equipamento.toml` | Uma compra de equipamento, mais enxuto — mostra que a ferramenta serve para qualquer processo, não só TI |

## Um caso analisado do começo ao fim

Se quiser ver a ferramenta sendo usada de verdade — leitura do AS-IS, identificação do
gargalo, propostas de melhoria e os indicadores para acompanhar — leia
[`docs/caso-de-uso.md`](docs/caso-de-uso.md).

O resumo: no processo de exemplo, o chamado leva 2,1 dias para ser resolvido, mas só 2,9
horas disso é trabalho de alguém. Mais de 95% do tempo o chamado está parado. E quase
toda essa espera está em um único ponto — a compra de peça.

## Como descrever um processo

O processo é um arquivo **TOML** — texto simples, com seções entre colchetes. Veja
`processos/chamado-suporte-ti.toml`, que está todo comentado. Os campos são:

**No topo do arquivo**, antes de qualquer seção:

```toml
raias = ["Usuário", "Service Desk (N1)", "Equipe Técnica (N2)"]
```

As **raias** são as faixas horizontais do diagrama: quem executa cada etapa. A ordem
aqui é a ordem de cima para baixo no desenho.

**A seção `[processo]`** tem o nome e a descrição:

```toml
[processo]
nome = "Abertura de chamado de suporte de TI"
descricao = "Como o chamado nasce, é tratado e encerrado."
```

**Cada etapa é um bloco `[[etapas]]`:**

| Campo | Obrigatório | Para que serve |
| --- | --- | --- |
| `id` | sim | Nome curto, único, sem espaços. É como as etapas se referenciam |
| `nome` | sim | O que aparece escrito no diagrama |
| `tipo` | sim | `inicio`, `tarefa`, `decisao` ou `fim` |
| `raia` | sim | Quem executa (precisa estar na lista `raias`) |
| `tempo_min` | não | Tempo de trabalho, em minutos |
| `espera_min` | não | Tempo parado em fila ou aguardando terceiros, em minutos |
| `sistema` | não | Ferramenta usada naquela etapa |
| `automatizavel` | não | `true` se dá para automatizar |
| `proximo` | não | Para onde o processo vai depois (lista de `id`). Se omitir, vai para a etapa seguinte |
| `rotulos` | não | Texto das setas de saída de uma decisão, ex.: `{ resolver = "Sim", comprar = "Não" }` |

Exemplo de uma etapa:

```toml
[[etapas]]
id = "triagem"
nome = "Triar e classificar o chamado"
tipo = "tarefa"
raia = "Service Desk (N1)"
tempo_min = 8
sistema = "Service Desk"
automatizavel = true
```

Os nomes podem ter acento, cedilha e vírgula — o arquivo é lido em UTF-8.

## Os conceitos, explicados sem jargão

| Termo | O que quer dizer, na prática |
| --- | --- |
| **BPMN** | Uma forma padronizada de desenhar processos. Como uma planta baixa: qualquer pessoa do ramo lê e entende, mesmo que tenha sido outra que desenhou |
| **Raia (lane)** | A faixa do diagrama que mostra **quem** faz cada etapa. Serve para enxergar quantas vezes o processo troca de mão |
| **AS-IS** | O processo como ele é **hoje**. Primeiro se desenha o AS-IS, depois se propõe o TO-BE (como deveria ser) |
| **Lead time** | O tempo total, do pedido até a entrega. É o que o usuário sente |
| **Tempo de execução** | O trabalho efetivo, com alguém agindo |
| **Tempo de espera** | O tempo parado: fila, aguardando resposta, aguardando peça. Costuma ser o maior vilão |
| **Handoff** | Cada vez que o processo passa de uma área para outra. Quanto mais trocas, maior a chance de retrabalho e de informação se perder |
| **Gargalo** | A etapa que segura todo o resto. Aqui, o relatório aponta as etapas com a maior espera |
| **KPI** | Indicador de desempenho. É o número que se acompanha mês a mês para saber se a melhoria pegou |
| **Automação** | Trocar trabalho manual repetitivo por sistema. O `automatizavel = true` marca as candidatas |

## Abrindo o diagrama

1. Vá em <https://bpmn.io/>
2. Arraste o arquivo `saida/chamado-suporte-ti.bpmn` para a página
3. O diagrama abre editável: dá para mover, renomear e exportar como imagem

O mesmo arquivo abre no **Camunda Modeler**, no **Bizagi** e no **draw.io**, porque é o
formato padrão BPMN 2.0.

## Testando

```bash
python -m unittest discover -s testes -v
```

São 16 testes: validação da descrição, estrutura do BPMN gerado (todo fluxo aponta para
um nó que existe, todo nó tem forma no desenho) e a matemática dos indicadores.

## Estrutura do projeto

```
mapeador-de-processos/
├── mapeador.py                              # o programa (só biblioteca padrão)
├── processos/
│   ├── chamado-suporte-ti.toml              # exemplo 1, comentado linha a linha
│   └── compra-de-equipamento.toml           # exemplo 2, mais enxuto
├── docs/
│   └── caso-de-uso.md                       # análise completa de um processo
├── saida/                                   # resultados já gerados (exemplos)
│   ├── chamado-suporte-ti.bpmn / .md / .html
│   └── compra-de-equipamento.bpmn / .md / .html
├── testes/
│   └── test_mapeador.py
├── LICENSE
└── README.md
```

## Decisões de projeto

**Por que Python sem nenhuma biblioteca?** Para quem for rodar não precisar instalar
nada. O programa gera o BPMN montando o XML, que é texto — não precisa de dependência
para isso.

**Por que TOML, e não Excel ou YAML?** O TOML é texto puro, versão no controle de
código, e o Python já sabe ler de fábrica. Um processo em texto entra em revisão de
reunião como qualquer outro documento.

**Por que gerar o desenho, e não só o XML?** Sem a parte gráfica, o bpmn.io abre o
arquivo e diz "não há diagrama para mostrar". O posicionamento das caixas é calculado
por uma grade simples: cada etapa avança um passo na horizontal, e cada raia é uma
faixa na vertical.

**Por que a automação vira `serviceTask`?** No BPMN, `userTask` é tarefa humana e
`serviceTask` é atendida por sistema. Marcar `automatizavel = true` já troca o tipo do
elemento — o diagrama conta a história antes do relatório.

## Licença

MIT — veja [LICENSE](LICENSE).
