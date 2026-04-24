# Pipeline climático antes da modelagem

Este repositório é um exemplo didático de organização de um pipeline de dados climáticos antes de qualquer etapa de modelagem ou machine learning. Ele usa dados fictícios e pequenos para demonstrar boas práticas de estrutura, rastreabilidade e preparação de bases inspiradas em fontes meteorológicas públicas, como INMET e ERA5.

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
4. Comparar resoluções temporais.
5. Gerar uma base processada fictícia.
6. Registrar decisões para manter rastreabilidade.

## Limites do exemplo

Os arquivos em `data/raw/` são inventados. Eles não representam uma estação, período, localidade ou reanálise real. O notebook não contém modelagem, validação científica, desempenho de algoritmos ou conclusões.

