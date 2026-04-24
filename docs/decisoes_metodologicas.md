# Decisoes metodologicas

Este arquivo registra decisoes estaveis do exemplo didatico.

## Dados brutos

Os arquivos em `data/raw/` devem ser tratados como entrada imutavel. Qualquer correcao, filtro ou conversao deve gerar uma nova saida em `data/interim/` ou `data/processed/`.

## Datas

As colunas de tempo devem ser convertidas para `datetime` no inicio do fluxo. O formato textual usado nos CSVs ficticios e `YYYY-MM-DD HH:MM`.

## Unidades

Variaveis de temperatura devem ser comparadas em graus Celsius. Variaveis de precipitacao devem ser comparadas em milimetros.

## Resolucao temporal

Fontes com resolucoes diferentes nao devem ser combinadas sem explicitar a regra de agregacao ou alinhamento. Neste exemplo, a fonte horaria e a fonte de 3 horas sao apenas alinhadas por horarios comuns.

## Modelagem

Este repositorio nao executa modelagem. A preparacao da base e o produto final do exemplo.

