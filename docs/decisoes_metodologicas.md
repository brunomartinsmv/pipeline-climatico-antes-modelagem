# Decisões metodológicas

Este arquivo registra as decisões estáveis do exemplo didático.

## Dado bruto

`data/raw/exemplo_era5_ficticio.csv` é entrada imutável. Qualquer correção, filtro ou conversão gera uma nova saída em `data/processed/`. O arquivo fictício só muda por meio do gerador documentado em [`data/README.md`](../data/README.md).

## Datas

`valid_time` é convertido para `datetime` no início do fluxo. Datas vazias, repetidas, fora de ordem ou fora da grade de 3 h de 2024 interrompem a validação. Um horário fora da grade, como 01h, seria descartado em silêncio no preparo; por isso é tratado como erro. A base final usa a grade horária completa de 2024, com 8 784 horas.

## Unidades

Temperatura e ponto de orvalho passam de kelvin para graus Celsius. Precipitação passa de metros para milímetros. A umidade relativa é derivada pela fórmula de Magnus (Alduchov e Eskridge, 1996).

## Lacunas no passo de 3 h

O arquivo é colocado na grade completa de 3 h. Horários que não existiam no arquivo são inseridos e marcados em `passo_inserido`. Uma coluna vazia em um horário que existe não conta como passo inserido. Depois:

1. temperatura e orvalho são interpolados no tempo apenas em lacunas internas de até 6 horas (2 passos seguidos);
2. lacunas mais longas ficam inteiras como ausentes, em vez de preenchidas só no começo;
3. precipitação nunca é preenchida.

## De 3 h para 1 h

- Temperatura e orvalho, grandezas instantâneas, são interpolados nas 2 horas entre passos vizinhos. A interpolação nunca atravessa uma lacuna mantida.
- A precipitação, acumulada nas 3 horas que terminam em `valid_time`, é dividida igualmente entre essas 3 horas. Um passo ausente deixa suas 3 horas ausentes e nunca toma a chuva do vizinho.
- Na base, a chuva fica no horário em que a hora **começa**: a linha das 23h guarda a chuva das 23h às 00h. O dado bruto rotula pelo fim do intervalo; a base troca o rótulo para que somas por dia, mês ou ano peguem exatamente as horas daquele período. Sem essa troca, a chuva das 23h às 00h de 31/01 cairia em fevereiro.
- Por isso, o acumulado das 00h de 01/01/2024, que cobre 21h a 00h de 2023, fica fora da base. O passo das 00h de 01/01/2025 entra inteiro: cobre 21h, 22h e 23h de 31/12/2024.
- Esta receita vale para acumulados de 3 h. No ERA5 horário, `tp` cobre só a hora que termina em `valid_time` e não precisa ser repartido; basta trocar o rótulo para o início da hora.

As marcações evitam que a base processada esconda as falhas da entrada.

## Modelagem

Este repositório não executa modelagem. A base processada é o produto final do exemplo.
