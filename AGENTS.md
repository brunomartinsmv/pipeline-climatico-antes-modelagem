# AGENTS.md

Exemplo didático de pipeline climático em Python, em português. Não há servidores nem banco de dados: tudo roda como comando em lote a partir da raiz.

## Comandos

- Instalar: `python -m pip install -e ".[dev,notebook]"`
- Lint: `python -m ruff check .`
- Testes: `python -m pytest`
- Pipeline completo: `MPLCONFIGDIR=/tmp/matplotlib-cache python -m pipeline_climatico tudo`
- Auditoria da cópia pública: `python scripts/auditar_publicacao.py`

## Cuidados

- Os CSVs de `data/raw/` são gerados por `pipeline_climatico/dados_ficticios.py`. Nunca edite os CSVs à mão; altere o gerador e rode `python -m pipeline_climatico gerar-dados`. Um teste compara os dois.
- Precipitação é grandeza acumulada: não interpole, não troque ausência por zero.
- `figures/*.png` é versionado e aparece no README. Rodar `graficos` regrava os PNGs; descarte com `git checkout -- figures/` se a mudança não fizer parte do trabalho.
- O notebook é versionado sem saídas.
- Textos para o leitor ficam em português com acentuação; identificadores de código ficam sem acento.
