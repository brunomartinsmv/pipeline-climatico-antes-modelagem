# Controle de variaveis

Este controle usa variaveis ficticias para demonstrar como documentar fontes climaticas.

| Variavel | Fonte ficticia | Unidade original | Unidade padronizada | Resolucao | Observacao |
|---|---|---:|---:|---|---|
| `temperatura_c` | INMET_EXEMPLO | graus Celsius | graus Celsius | horaria | Pode conter lacunas ficticias, preenchidas por interpolacao curta. |
| `umidade_relativa_pct` | INMET_EXEMPLO | porcentagem | porcentagem | horaria | Pode conter lacunas ficticias; deve permanecer entre 0 e 100. |
| `precipitacao_mm` | INMET_EXEMPLO | milimetros | milimetros | horaria | Pode conter lacunas ficticias; acumulado no periodo informado. |
| `temperatura_2m_k` | ERA5_EXEMPLO | Kelvin | graus Celsius | 3 horas | Converter subtraindo 273,15. |
| `precipitacao_total_m` | ERA5_EXEMPLO | metros | milimetros | 3 horas | Converter multiplicando por 1000. |
| `registro_inmet_inserido` | Pipeline | booleano | booleano | horaria | Indica horario criado porque nao havia registro bruto no INMET ficticio. |
| `*_imputado` | Pipeline | booleano | booleano | horaria | Indica valor preenchido no tratamento de lacunas. |
| `registro_era5_interpolado` | Pipeline | booleano | booleano | horaria | Indica horario interpolado a partir da grade de 3 horas. |

## Campos minimos recomendados

- Nome tecnico da variavel.
- Fonte.
- Unidade original.
- Unidade padronizada.
- Resolucao temporal.
- Regra de conversao.
- Observacoes sobre lacunas ou qualidade.
