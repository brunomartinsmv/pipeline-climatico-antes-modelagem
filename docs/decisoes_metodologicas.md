# Decisoes metodologicas

Este arquivo registra decisoes estaveis do exemplo didatico.

## Dados brutos

Os arquivos em `data/raw/` devem ser tratados como entrada imutavel. Qualquer correcao, filtro ou conversao deve gerar uma nova saida em `data/interim/` ou `data/processed/`.

## Datas

As colunas de tempo devem ser convertidas para `datetime` no inicio do fluxo. O formato textual usado nos CSVs ficticios e `YYYY-MM-DD HH:MM`.

## Unidades

Variaveis de temperatura devem ser comparadas em graus Celsius. Variaveis de precipitacao devem ser comparadas em milimetros.

## Resolucao temporal

Fontes com resolucoes diferentes nao devem ser combinadas sem explicitar a regra de agregacao ou alinhamento. Neste exemplo, o INMET ficticio e horario, enquanto o ERA5 ficticio esta em intervalos de 3 horas. Para fins didaticos, o ERA5 e interpolado para a grade horaria antes da combinacao.

## Lacunas no INMET ficticio

O arquivo INMET ficticio simula um problema comum em dados observacionais: horarios ausentes e valores vazios em algumas variaveis. O script de preparacao insere a grade horaria completa de 2024, marca registros inseridos em `registro_inmet_inserido` e preenche lacunas curtas por interpolacao temporal limitada a 6 horas.

As colunas `temperatura_inmet_c_imputado`, `umidade_relativa_pct_imputado` e `precipitacao_mm_imputado` indicam quais valores foram preenchidos. Essa marcacao evita que a base processada esconda a existencia de falhas na entrada.

## Modelagem

Este repositorio nao executa modelagem. A preparacao da base e o produto final do exemplo.
