# Pipeline climático antes da modelagem

[![Testes](https://github.com/brunomartinsmv/pipeline-climatico-antes-modelagem/actions/workflows/testes.yml/badge.svg)](https://github.com/brunomartinsmv/pipeline-climatico-antes-modelagem/actions/workflows/testes.yml)

Exemplo didático, em português, de como preparar dados climáticos antes de qualquer modelo ou machine learning. Um ano de dados **fictícios** no formato do ERA5, com passo de 3 horas, passa por inventário, validação, tratamento de lacunas, conversão de unidades e passagem para a grade horária até virar uma base processada e rastreável.

O objetivo não é produzir resultado científico. É mostrar o trabalho de bastidor que torna uma análise reproduzível.

![Painel mensal da base processada](figures/painel_mensal_variaveis_processadas.png)

## Por que o pipeline vem antes do modelo?

Dados de reanálise parecem prontos, mas não chegam prontos para análise. Antes de treinar qualquer modelo, é preciso responder:

- Em que unidade está cada variável? `t2m` vem em kelvin, `tp` em metros.
- A grandeza é instantânea ou acumulada? Acumulada em que intervalo, e rotulada no início ou no fim?
- Quais passos faltam e o que foi feito com eles?
- O dado bruto foi preservado e a base final pode ser reconstruída?

Um exemplo do que dá errado sem essas perguntas: interpolar para a grade horária a chuva acumulada em 3 horas triplica o total anual. O [notebook](notebooks/00_visao_geral_pipeline.ipynb) mostra esse erro e a correção.

## Comece aqui

```bash
git clone https://github.com/brunomartinsmv/pipeline-climatico-antes-modelagem.git
cd pipeline-climatico-antes-modelagem
python -m venv .venv
source .venv/bin/activate          # no Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt

python -m pipeline_climatico tudo
```

O último comando inventaria e valida o arquivo bruto, gera `data/processed/base_climatica_ficticia_processada.csv` e salva os painéis em `figures/`. Depois, abra o notebook para acompanhar cada etapa:

```bash
jupyter notebook notebooks/00_visao_geral_pipeline.ipynb
```

## Etapas

| Etapa | Comando |
|---|---|
| Inventariar variáveis, unidades e ausências | `python -m pipeline_climatico inventariar` |
| Validar colunas, datas e passos ausentes | `python -m pipeline_climatico validar` |
| Tratar lacunas, converter unidades e passar de 3 h para 1 h | `python -m pipeline_climatico preparar` |
| Gerar painéis mensais | `python -m pipeline_climatico graficos` |
| Recriar o dado fictício a partir da semente | `python -m pipeline_climatico gerar-dados` |

As regras de cada etapa estão em [decisões metodológicas](docs/decisoes_metodologicas.md). O [controle de variáveis](docs/controle_variaveis.md) descreve cada coluna bruta e processada.

![Falhas tratadas no ERA5 fictício](figures/painel_mensal_falhas_era5.png)

## Estrutura

```text
pipeline_climatico/   código do pipeline, uma etapa por módulo
notebooks/            percurso guiado pelas etapas
data/raw/             CSV fictício versionado e imutável
data/processed/       base gerada localmente (não versionada)
docs/                 decisões, controle de variáveis e boas práticas
figures/              painéis gerados pelo pipeline (versionados para este README)
scripts/              auditoria da cópia pública
tests/                testes do pipeline e da publicação
```

## Limites do exemplo

O dado de `data/raw/` é inventado, como explica o [guia dos dados](data/README.md). Ele não representa nenhuma localidade nem a reanálise real, e as falhas foram inseridas de propósito: o ERA5 real não tem lacunas. As regras de preenchimento servem para demonstrar o fluxo; em um projeto real, dependeriam da variável, da duração da falha e do objetivo da análise. Não há modelagem, validação científica ou conclusão.

## Contribuição e citação

Para propor mudanças, veja [como contribuir](CONTRIBUTING.md). O [CHANGELOG](CHANGELOG.md) registra as versões. Para citar o material, use os metadados de [CITATION.cff](CITATION.cff).

## Licença

Os textos, as figuras e o dado fictício estão sob [CC BY 4.0](LICENSE): você pode copiar, adaptar e redistribuir, desde que dê o crédito a Bruno Martins e indique as alterações. O código em `pipeline_climatico/`, `scripts/`, `tests/` e nas células do notebook está sob a [licença MIT](LICENSE-CODE).

ERA5 e Copernicus são citados apenas como referência de formato. Nenhum dado dessas fontes acompanha o repositório.
