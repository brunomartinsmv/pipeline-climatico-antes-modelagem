# Visão geral do pipeline climático

Este documento descreve o fluxo didático para preparar dados climáticos antes de qualquer etapa de modelagem.

## Objetivo

Organizar um ano de dados meteorológicos fictícios em um processo rastreável, no qual cada transformação é explícita e pode ser repetida.

## Etapas

| Etapa | Comando | Módulo |
|---|---|---|
| 1. Inventariar variáveis, tipos e ausências | `python -m pipeline_climatico inventariar` | `inspecao.py` |
| 2. Validar colunas e datas | `python -m pipeline_climatico validar` | `inspecao.py` |
| 3. Padronizar datas e unidades | `python -m pipeline_climatico preparar` | `preparo.py` |
| 4. Inserir horas ausentes e marcar imputações | `python -m pipeline_climatico preparar` | `preparo.py` |
| 5. Alinhar as resoluções de 1 h e 3 h | `python -m pipeline_climatico preparar` | `preparo.py` |
| 6. Gerar a base em `data/processed/` | `python -m pipeline_climatico preparar` | `preparo.py` |
| 7. Gerar painéis mensais em `figures/` | `python -m pipeline_climatico graficos` | `graficos.py` |

`python -m pipeline_climatico tudo` executa as etapas em ordem. As decisões de cada etapa ficam em [`decisoes_metodologicas.md`](decisoes_metodologicas.md).

## Princípio central

O pipeline deve deixar claro como a base final foi construída. A modelagem só entra depois que origem, unidade, frequência, lacunas e regras de transformação estiverem documentadas.
