# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Unreleased]

## [0.2.0] - 2026-11-18

Preparação para a cópia pública.

### Added
- Pacote `pipeline_climatico` com uma etapa por módulo e comando único `python -m pipeline_climatico <etapa>`.
- Gerador determinístico dos CSVs fictícios e guia dos dados em `data/README.md`.
- Testes de conversão de unidades, conservação da chuva, regra de lacunas, flags e correspondência entre gerador e CSVs.
- Auditoria da cópia pública (`scripts/auditar_publicacao.py`) e CI com lint, testes e execução do pipeline.
- `LICENSE` (CC BY 4.0), `LICENSE-CODE` (MIT), `CONTRIBUTING.md`, `CITATION.cff`, `AGENTS.md` e `pyproject.toml`.

### Changed
- Notebook reescrito sobre as funções do pacote, com a demonstração do erro de interpolar acumulados.
- Painéis comparam INMET e ERA5 no mesmo eixo e mostram também as lacunas mantidas ausentes.
- Colunas processadas renomeadas com o sufixo da fonte (`umidade_relativa_inmet_pct`, `precipitacao_inmet_mm`).
- Documentação revisada com acentuação e com a distinção entre grandezas instantâneas e acumuladas.
- CSVs fictícios recriados pelo novo gerador.

### Fixed
- A chuva do ERA5 era interpolada linearmente de 3 h para 1 h, o que triplicava o total anual. Agora o acumulado é repartido entre as 3 horas e o total é preservado.
- A chuva do INMET era interpolada e o restante trocado por zero. Agora horas sem registro ficam ausentes e marcadas.
- Lacunas maiores que 6 h eram preenchidas parcialmente. Agora ficam inteiras como ausentes.

### Removed
- Scripts numerados, substituídos pelo comando do pacote.
- Pasta `src/` vazia, `data/interim/` sem uso e rascunhos de postagem.

## [0.1.0] - 2026-04-24

### Added
- Estrutura didática inicial com dados fictícios do INMET e do ERA5, scripts de inventário, validação, preparo e gráficos, notebook e documentação metodológica.
