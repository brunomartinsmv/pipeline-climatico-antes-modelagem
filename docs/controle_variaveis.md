# Controle de variáveis

Este controle usa as variáveis fictícias do exemplo para mostrar como documentar fontes climáticas.

## Dados brutos

| Variável | Fonte fictícia | Unidade original | Resolução | Observação |
|---|---|---|---|---|
| `temperatura_c` | INMET_EXEMPLO | °C | 1 h | Instantânea; contém lacunas. |
| `umidade_relativa_pct` | INMET_EXEMPLO | % | 1 h | Instantânea; deve ficar entre 0 e 100. |
| `precipitacao_mm` | INMET_EXEMPLO | mm | 1 h | Acumulado na hora; resolução de 0,2 mm. |
| `temperatura_2m_k` | ERA5_EXEMPLO | K | 3 h | Instantânea, a 2 m da superfície. |
| `precipitacao_total_m` | ERA5_EXEMPLO | m | 3 h | Acumulado nas 3 h que começam no horário indicado. |

## Base processada

| Coluna | Unidade | Origem | Regra |
|---|---|---|---|
| `temperatura_inmet_c` | °C | INMET | Lacunas internas de até 6 h interpoladas no tempo; maiores ficam ausentes. |
| `umidade_relativa_inmet_pct` | % | INMET | Mesma regra da temperatura; limitada a 0–100. |
| `precipitacao_inmet_mm` | mm | INMET | Sem preenchimento. |
| `temperatura_era5_c` | °C | ERA5 | K − 273,15; interpolada de 3 h para 1 h. |
| `precipitacao_era5_mm` | mm | ERA5 | m × 1000; acumulado de 3 h dividido igualmente entre as 3 horas. |
| `temperatura_inmet_c_imputado` | booleano | pipeline | Valor interpolado. |
| `umidade_relativa_inmet_pct_imputado` | booleano | pipeline | Valor interpolado. |
| `precipitacao_inmet_mm_ausente` | booleano | pipeline | Chuva sem registro na hora. |
| `registro_inmet_inserido` | booleano | pipeline | Hora criada porque não existia no bruto. |
| `registro_era5_interpolado` | booleano | pipeline | Hora fora da grade de 3 h do ERA5. |

## Campos mínimos recomendados

- Nome técnico da variável.
- Fonte.
- Unidade original e padronizada.
- Resolução temporal e se a grandeza é instantânea ou acumulada.
- Regra de conversão.
- Observações sobre lacunas ou qualidade.
