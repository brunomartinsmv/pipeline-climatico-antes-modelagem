# Controle de variáveis

Este controle usa as variáveis fictícias do exemplo para mostrar como documentar uma fonte climática.

## Dado bruto

| Variável | Unidade | Resolução | Natureza | Observação |
|---|---|---|---|---|
| `valid_time` | UTC | 3 h | instante | 01/01/2024 00h a 01/01/2025 00h; 5 passos faltam. |
| `ponto_grade` | - | - | - | Identificador fictício do ponto. |
| `t2m` | K | 3 h | instantânea | Temperatura do ar a 2 m; contém lacunas. |
| `d2m` | K | 3 h | instantânea | Ponto de orvalho a 2 m; contém lacunas. |
| `tp` | m | 3 h | acumulada | Total das 3 h que terminam em `valid_time`; contém lacunas. No ERA5 horário, a janela é de 1 h. |

## Base processada

| Coluna | Tipo | Regra |
|---|---|---|
| `data_hora` | UTC, horária | Grade completa de 2024, 8 784 horas. Para a chuva, marca o início da hora. |
| `temperatura_c` | °C | `t2m` − 273,15; lacunas de até 6 h interpoladas no passo de 3 h; depois interpolada para 1 h entre passos vizinhos. |
| `ponto_orvalho_c` | °C | `d2m` − 273,15; mesma regra da temperatura. |
| `umidade_relativa_pct` | % | Derivada de temperatura e orvalho pela fórmula de Magnus; limitada a 100. |
| `precipitacao_mm` | mm | `tp` × 1000, dividido igualmente entre as 3 horas que o passo cobre e rotulado no início de cada hora; nunca preenchida. |
| `hora_interpolada` | booleano | Hora fora da grade de 3 h: temperatura e orvalho interpolados. |
| `passo_inserido` | booleano | Horário de 3 h ausente do arquivo bruto (a linha inteira faltava). |
| `temperatura_c_imputado` | booleano | Valor que só existe por causa do preenchimento de uma lacuna. |
| `ponto_orvalho_c_imputado` | booleano | Idem, para o ponto de orvalho. |
| `precipitacao_mm_ausente` | booleano | Hora coberta por um passo sem `tp`. |

## Campos mínimos recomendados

- Nome técnico da variável e nome padronizado.
- Fonte e versão.
- Unidade original e padronizada.
- Resolução temporal e se a grandeza é instantânea ou acumulada, com a convenção de tempo.
- Regra de conversão.
- Observações sobre lacunas ou qualidade.
