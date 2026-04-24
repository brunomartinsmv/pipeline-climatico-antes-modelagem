# Pipeline climático antes da modelagem

Este repositório é um exemplo didático de organização de um pipeline de dados climáticos antes de qualquer etapa de modelagem ou machine learning. Ele usa um ano de dados fictícios para demonstrar boas práticas de estrutura, rastreabilidade e preparação de bases inspiradas em fontes meteorológicas públicas, como INMET e ERA5.

O objetivo não é apresentar resultados científicos. O foco é mostrar o trabalho de bastidor que torna uma análise reproduzível: inventariar variáveis, preservar dados brutos, padronizar datas e unidades, registrar decisões metodológicas e produzir uma base processada com regras claras.

## Por que o pipeline vem antes do modelo?

Modelos dependem da qualidade da base que recebem. Em dados climáticos, essa base raramente nasce pronta: fontes diferentes podem ter resoluções temporais distintas, unidades incompatíveis, formatos variados, lacunas, metadados incompletos e convenções de nomes pouco padronizadas.

Antes de treinar qualquer modelo, é preciso responder perguntas simples e decisivas:

- De onde veio cada variável?
- Qual é a unidade original?
- A resolução é horária, diária, mensal ou outra?
- Quais transformações foram aplicadas?
- O dado bruto foi preservado?
- A base processada pode ser reconstruída?

Este repositório ilustra esse fluxo em escala mínima, usando apenas exemplos fictícios.

## Estrutura

```text
data/
  raw/          dados brutos fictícios
  interim/      saídas intermediárias geradas localmente
  processed/    bases finais de exemplo geradas localmente
docs/           documentação metodológica didática
figures/        figuras geradas localmente
notebooks/      exploração guiada do pipeline
posts/linkedin/ rascunhos de postagem
scripts/        scripts esqueleto do fluxo
src/            código reutilizável
```

## Fluxo didático sugerido

1. Inventariar variáveis e metadados.
2. Validar a estrutura dos arquivos de entrada.
3. Padronizar datas, nomes e unidades.
4. Identificar falhas no exemplo INMET e inserir horários ausentes.
5. Comparar resoluções temporais.
6. Gerar uma base processada fictícia.
7. Registrar decisões para manter rastreabilidade.

## Gráficos

Os scripts abaixo geram figuras locais em `figures/`:

```bash
python3 scripts/05_graficos_painel_mensal_pipeline.py
```

O script cria um painel mensal da base processada e um painel de falhas tratadas no INMET fictício. As figuras foram pensadas como material visual de apoio, sem apresentar conclusões científicas.

## Limites do exemplo

Os arquivos em `data/raw/` são inventados. Eles não representam uma estação, localidade ou reanálise real. O ano de 2024 foi usado apenas para criar uma sequência temporal completa de exemplo. O notebook não contém modelagem, validação científica, desempenho de algoritmos ou conclusões.
