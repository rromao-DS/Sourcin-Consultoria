# Origem

Cópia do projeto [mapeador-de-processos](https://github.com/Maicon-Gomes-Messias/mapeador-de-processos), de Maicon Gomes Messias, sob licença MIT (arquivo `LICENSE`, mantido sem alteração).

Trazido em 30/10/2026 para gerar os fluxos atuais (AS-IS) da Surcin a partir de arquivos TOML. O código não foi modificado.

Uso, a partir da raiz do repositório:

```
python3 ferramentas/mapeador-de-processos/mapeador.py diagnostico/fluxos/rascunhos/*.toml --saida diagnostico/fluxos/saida
```

Gera, para cada processo, o diagrama BPMN 2.0 (`.bpmn`, abre no bpmn.io), um relatório (`.md`) e um painel (`.html`).
