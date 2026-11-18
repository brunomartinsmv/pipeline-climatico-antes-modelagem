# Dados do exemplo

Os dois arquivos de `raw/` são **inventados**. Eles imitam o formato de fontes meteorológicas públicas, mas não representam nenhuma estação, localidade ou reanálise real. Não use esses valores em análises.

| Arquivo | Imita | Resolução | Período |
|---|---|---|---|
| `raw/exemplo_inmet_ficticio.csv` | estação automática do INMET | 1 hora | 2024 |
| `raw/exemplo_era5_ficticio.csv` | série do ERA5 em um ponto de grade | 3 horas | 2024 |

## Como foram gerados

O módulo [`pipeline_climatico/dados_ficticios.py`](../pipeline_climatico/dados_ficticios.py) cria uma série horária de referência com ciclo anual, ciclo diário, ruído autocorrelacionado e chuva concentrada no verão e à tarde. Cada fonte deriva dessa série com características próprias:

- **INMET**: temperatura com uma casa decimal, umidade inteira, chuva com resolução de 0,2 mm, como em um pluviômetro de báscula. O gerador apaga 11 horas inteiras e abre lacunas de 2 a 10 horas em algumas variáveis.
- **ERA5**: temperatura suavizada, cerca de 0,6 °C mais fria e em kelvin; chuva em metros, acumulada nas 3 horas que **começam** no horário indicado, mais espalhada e menor que a do INMET.

A semente é fixa. Para recriar os arquivos, execute na raiz:

```bash
python -m pipeline_climatico gerar-dados
```

O teste `test_csvs_brutos_coincidem_com_o_gerador` garante que os CSVs versionados são exatamente os que o gerador produz.

## Saídas

`processed/` recebe a base gerada por `python -m pipeline_climatico preparar`. Ela não é versionada; o pipeline a recria em segundos.

## Licença

Os dados fictícios são autorais e distribuídos sob [CC BY 4.0](../LICENSE).
