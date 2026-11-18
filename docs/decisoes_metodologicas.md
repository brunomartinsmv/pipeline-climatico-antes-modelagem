# Decisões metodológicas

Este arquivo registra as decisões estáveis do exemplo didático.

## Dados brutos

Os arquivos em `data/raw/` são entrada imutável. Qualquer correção, filtro ou conversão gera uma nova saída em `data/processed/`. Os brutos fictícios só mudam por meio do gerador documentado em [`data/README.md`](../data/README.md).

## Datas

As colunas de tempo são convertidas para `datetime` no início do fluxo. O formato textual dos CSVs é `YYYY-MM-DD HH:MM`. A referência é a grade horária completa de 2024, com 8 784 horas.

## Unidades

Temperatura é comparada em graus Celsius e precipitação em milímetros.

## Resolução temporal

O INMET fictício é horário; o ERA5 fictício tem passo de 3 horas. Para combinar as fontes na grade horária:

- a temperatura do ERA5, grandeza instantânea, é interpolada no tempo;
- a precipitação do ERA5, acumulada, é repartida igualmente entre as 3 horas que o valor cobre. O total anual é preservado.

Neste arquivo fictício, o acumulado cobre as 3 horas que começam no horário indicado. No ERA5 real, acumulados se referem ao período que termina no horário indicado; a regra de repartição mudaria de lado.

## Lacunas no INMET fictício

O INMET fictício simula falhas comuns em dados observacionais: horas inteiras sem registro e valores vazios. O preparo:

1. insere as horas ausentes e as marca em `registro_inmet_inserido`;
2. interpola temperatura e umidade apenas em lacunas internas de até 6 horas seguidas, marcando os valores em `*_imputado`;
3. mantém lacunas mais longas inteiras como ausentes, em vez de preencher só o começo delas;
4. não preenche precipitação. Horas sem registro de chuva ficam ausentes e marcadas em `precipitacao_inmet_mm_ausente`.

As marcações evitam que a base processada esconda as falhas da entrada.

## Modelagem

Este repositório não executa modelagem. A base processada é o produto final do exemplo.
