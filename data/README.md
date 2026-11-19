# Dados do exemplo

O arquivo `raw/exemplo_era5_ficticio.csv` é **inventado**. Ele imita uma série do ERA5 extraída para um ponto de grade, mas não representa nenhuma localidade nem a reanálise real. Não use esses valores em análises.

| Coluna | Significado | Unidade | Natureza |
|---|---|---|---|
| `valid_time` | tempo de validade | UTC | instante |
| `ponto_grade` | identificador fictício do ponto | - | - |
| `t2m` | temperatura do ar a 2 m | K | instantânea |
| `d2m` | ponto de orvalho a 2 m | K | instantâneo |
| `tp` | precipitação total | m | acumulada nas 3 h que **terminam** em `valid_time` |

O passo é de 3 horas, de 01/01/2024 00h a 01/01/2025 00h. O último passo existe porque é ele que contém a chuva das 21h às 00h de 31/12/2024.

## A janela de acumulação depende do produto

No ERA5 horário, o produto mais usado, `tp` é o acumulado da **1 hora** que termina em `valid_time`. A janela de 3 horas aparece em produtos com passo de 3 h, como os membros do ensemble do ERA5, e neste arquivo fictício. Antes de reaproveitar a receita do exemplo, confira na documentação do produto baixado qual é a janela e se o rótulo marca o início ou o fim do intervalo.

## Como foi gerado

O módulo [`pipeline_climatico/dados_ficticios.py`](../pipeline_climatico/dados_ficticios.py) cria uma série horária de referência com ciclo anual, ciclo diário, ruído autocorrelacionado e chuva concentrada no verão e à tarde. O arquivo de 3 h é amostrado dessa série:

- `t2m` e `d2m` são os valores no instante do passo, em kelvin. O ponto de orvalho sai da umidade de referência pela fórmula de Magnus.
- `tp` é a soma das 3 horas que terminam no passo, em metros, como nos produtos de 3 h do ERA5.
- Para exercitar o tratamento de falhas, o gerador remove 5 passos inteiros e apaga 13 valores em blocos de 1 a 4 passos. As falhas simulam arquivos que não baixaram ou vieram corrompidos; o ERA5 real não tem lacunas.

A semente é fixa. Para recriar o arquivo, execute na raiz:

```bash
python -m pipeline_climatico gerar-dados
```

O teste `test_csv_bruto_coincide_com_o_gerador` garante que o CSV versionado é exatamente o que o gerador produz.

## Saídas

`processed/` recebe a base gerada por `python -m pipeline_climatico preparar`. Ela não é versionada; o pipeline a recria em segundos.

## Licença

Os dados fictícios são autorais e distribuídos sob [CC BY 4.0](../LICENSE). ERA5 e Copernicus são citados apenas como referência de formato.
