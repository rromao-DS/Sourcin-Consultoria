# Repositórios de referência

Instalados em 30/10/2026 como submódulos do git (apontam para o repositório original, sem cópia do código). Para baixar depois de clonar este repositório:

```
git submodule update --init --depth 1
```

| Pasta | Repositório | Licença | Para que usamos |
|---|---|---|---|
| `../mapeador-de-processos/` | Maicon-Gomes-Messias/mapeador-de-processos | MIT | Copiado (não é submódulo). Gera BPMN, relatório e painel dos fluxos da pasta `diagnostico/fluxos/` |
| `claude-skills-borghei/` | borghei/Claude-Skills | MIT + Commons Clause | Consulta interna. `business-operations/process-mapper` (mapeamento), `project-management/agile-coach`, `scrum-master` e `sprint-retrospective` (rito ágil do Acompanhamento) |
| `accounting-workflow-skills/` | Denymbird/accounting-workflow-skills | MIT | Modelos de rotina para a implantação: `onboarding-workflow` (entrada de cliente), `monthly-query-chase` (cobrança de documentos do mês), `client-email-desk` (triagem de demandas), `management-pack-commentary` (comentário do fechamento) |

## Cuidados

- **Commons Clause (borghei):** pode usar como referência e adaptar ideias, mas não pode revender o material nem entregá-lo à cliente como produto. As rotinas do Claude da Surcin são escritas do zero, em português, para os processos dela.
- As rotinas de referência são de escritórios de contabilidade de outros países (Reino Unido, em boa parte). Servem de estrutura, não de regra fiscal. Nenhuma regra tributária vem delas.
- Nada de dado de cliente da Surcin entra nestas pastas.
