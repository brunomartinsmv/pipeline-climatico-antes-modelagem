# Antes do machine learning, vem o pipeline

## Versao curta

Antes de pensar em modelo, metrica ou algoritmo, vem uma etapa menos chamativa e muito mais decisiva: o pipeline de dados.

Em dados climaticos, fontes como INMET e ERA5 podem ter resolucoes temporais, unidades, formatos e metadados diferentes. Se isso nao estiver organizado, o modelo aprende em cima de uma base fragil.

Pipeline bem feito nao e burocracia. E o que permite saber de onde cada variavel veio, como foi transformada e se a base final pode ser reconstruida.

## Versao media

Antes do machine learning, vem o pipeline.

Em projetos com dados climaticos, a maior parte do trabalho serio acontece antes do modelo: organizar arquivos, preservar dados brutos, checar colunas, padronizar datas, converter unidades, lidar com lacunas e registrar decisoes.

Fontes como INMET e ERA5 sao valiosas, mas nao chegam automaticamente prontas para analise conjunta. Uma pode estar em escala horaria, outra em outra frequencia; uma variavel pode vir em Celsius, outra em Kelvin; um acumulado pode estar em milimetros ou metros.

Sem rastreabilidade, fica dificil explicar a base final. Com um pipeline claro, cada etapa deixa evidencias: entrada, transformacao, saida e decisao metodologica.

Modelagem e importante. Mas ela precisa vir depois de uma pergunta mais basica: a base esta organizada o suficiente para sustentar a analise?

## Versao mais tecnica

Antes de treinar qualquer modelo com dados climaticos, eu gosto de separar uma etapa especifica para o pipeline.

Essa etapa nao serve para produzir resultado cientifico imediato. Ela serve para reduzir ambiguidade: quais variaveis entram, quais unidades foram convertidas, qual resolucao temporal foi adotada, como lacunas foram tratadas e onde cada transformacao ficou registrada.

Esse cuidado e especialmente importante quando combinamos fontes meteorologicas distintas. Dados observacionais e reanalises podem representar tempos, espacamentos e convencoes diferentes. Se essas diferencas forem ignoradas, o problema aparece depois como ruido, inconsistencia ou interpretacao fragil do modelo.

Um bom pipeline separa:

- `data/raw/` para entradas preservadas;
- `data/interim/` para etapas intermediarias;
- `data/processed/` para bases prontas para analise;
- `docs/` para decisoes metodologicas;
- `scripts/` e `notebooks/` para tornar o processo reproduzivel.

O modelo pode mudar. A base precisa continuar explicavel.

## Sugestao de carrossel com 5 slides

### Slide 1

Antes do machine learning, vem o pipeline.

### Slide 2

Dados climaticos raramente chegam prontos: fontes diferentes, formatos diferentes, resolucoes diferentes.

### Slide 3

O pipeline organiza o essencial: datas, unidades, colunas, lacunas, metadados e versoes da base.

### Slide 4

Preservar dados brutos e registrar transformacoes torna a analise rastreavel.

### Slide 5

Um modelo pode ser trocado. Uma base mal documentada compromete todo o fluxo.

