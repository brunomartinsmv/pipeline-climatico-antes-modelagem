# Visão geral do pipeline climático

Este documento descreve o fluxo didático para preparar dados climáticos antes de qualquer etapa de modelagem.

## Objetivo

Transformar um ano de dados fictícios no formato do ERA5, com passo de 3 horas, em uma base horária rastreável, na qual cada transformação é explícita e pode ser repetida.

## Etapas

| Etapa | Comando | Módulo |
|---|---|---|
| 1. Inventariar variáveis, unidades e ausências | `python -m pipeline_climatico inventariar` | `inspecao.py` |
| 2. Validar colunas, datas e passos | `python -m pipeline_climatico validar` | `inspecao.py` |
| 3. Inserir passos ausentes e tratar lacunas | `python -m pipeline_climatico preparar` | `preparo.py` |
| 4. Converter unidades e derivar a umidade | `python -m pipeline_climatico preparar` | `preparo.py` |
| 5. Passar de 3 h para 1 h | `python -m pipeline_climatico preparar` | `preparo.py` |
| 6. Gerar a base em `data/processed/` | `python -m pipeline_climatico preparar` | `preparo.py` |
| 7. Gerar painéis mensais em `figures/` | `python -m pipeline_climatico graficos` | `graficos.py` |

`python -m pipeline_climatico tudo` executa as etapas em ordem. As decisões de cada etapa ficam em [`decisoes_metodologicas.md`](decisoes_metodologicas.md).

## Princípio central

O pipeline deve deixar claro como a base final foi construída. A modelagem só entra depois que origem, unidade, frequência, lacunas e regras de transformação estiverem documentadas.
