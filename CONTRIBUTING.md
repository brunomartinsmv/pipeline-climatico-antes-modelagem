# Como contribuir

Abra uma [issue](https://github.com/brunomartinsmv/pipeline-climatico-antes-modelagem/issues) para relatar um erro ou sugerir uma etapa nova. Para propor uma mudança, trabalhe em um ramo próprio e abra um pull request.

## Ambiente

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev,notebook]"
```

## Antes de abrir o pull request

Execute na raiz:

```bash
python -m ruff check .
python -m pytest
python -m pipeline_climatico tudo
python scripts/auditar_publicacao.py
```

A auditoria rejeita binários não liberados, arquivos grandes e notebooks com saídas. Limpe as saídas do notebook antes de salvar.

## Regras do material

- Escreva em português, com frases curtas, e explique cada regra no ponto em que ela é aplicada.
- Dados brutos não são editados à mão. Mudanças nos CSVs fictícios passam pelo gerador em `pipeline_climatico/dados_ficticios.py`, seguidas de `python -m pipeline_climatico gerar-dados`.
- Toda nova transformação deixa uma marcação na base processada e é registrada em `docs/decisoes_metodologicas.md` e `docs/controle_variaveis.md`.
- Não acrescente dados reais ou de terceiros sem registrar a fonte e as condições de distribuição.
- Se as figuras mudarem, regenere-as com `python -m pipeline_climatico graficos` e confira o README.
- Registre a mudança em `CHANGELOG.md`, na seção `[Unreleased]`.

Ao contribuir, você concorda em publicar seu texto sob CC BY 4.0 e seu código sob a licença MIT, as mesmas do repositório, descritas no [README](README.md#licença).
