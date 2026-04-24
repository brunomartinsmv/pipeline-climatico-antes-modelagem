# Visao geral do pipeline climatico

Este documento descreve um fluxo didatico para preparar dados climaticos antes de qualquer etapa de modelagem.

## Objetivo

Organizar dados meteorologicos ficticios em um processo rastreavel, no qual cada transformacao seja explicita e possa ser repetida.

## Etapas principais

1. Preservar os dados brutos em `data/raw/`.
2. Inventariar variaveis, unidades, fontes e resolucao temporal.
3. Validar nomes de colunas e tipos esperados.
4. Padronizar datas e unidades.
5. Produzir bases intermediarias em `data/interim/`, quando necessario.
6. Gerar uma base processada em `data/processed/`.
7. Registrar decisoes metodologicas em `docs/`.

## Principio central

O pipeline deve deixar claro como a base final foi construida. A modelagem so deve entrar depois que origem, unidade, frequencia, lacunas e regras de transformacao estiverem documentadas.

