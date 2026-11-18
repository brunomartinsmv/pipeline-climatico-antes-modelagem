# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Unreleased]

## [0.2.0] - 2026-11-18

Preparação para a cópia pública.

### Added
- Pacote `pipeline_climatico` com uma etapa por módulo e comando único `python -m pipeline_climatico <etapa>`.
- Gerador determinístico do CSV fictício e guia dos dados em `data/README.md`.
- Ponto de orvalho (`d2m`) no dado bruto e umidade relativa derivada pela fórmula de Magnus.
- Testes de validação, unidades, conservação da chuva, regra de lacunas, marcações e correspondência entre gerador e CSV.
- Auditoria da cópia pública (`scripts/auditar_publicacao.py`) e CI com lint, testes e execução do pipeline.
- `LICENSE` (CC BY 4.0), `LICENSE-CODE` (MIT), `CONTRIBUTING.md`, `CITATION.cff`, `AGENTS.md` e `pyproject.toml`.

### Changed
- O exemplo passou a usar uma única fonte, o ERA5 fictício, com os nomes curtos do Copernicus (`valid_time`, `t2m`, `d2m`, `tp`) e as falhas antes atribuídas à estação.
- O acumulado de chuva segue a convenção do ERA5 real: cobre as 3 horas que terminam em `valid_time`. O arquivo inclui o passo de 01/01/2025 00h para fechar o ano.
- Notebook reescrito sobre as funções do pacote, com a demonstração do erro de interpolar acumulados.
- Documentação revisada com acentuação e com a distinção entre grandezas instantâneas e acumuladas.
- `graficos.py` não altera mais o backend nem o estilo global do matplotlib ao ser importado.

### Fixed
- A chuva de 3 h era interpolada linearmente para 1 h, o que triplicava o total anual. Agora o acumulado é repartido entre as 3 horas e o total é preservado.
- Chuva ausente era interpolada e o restante trocado por zero. Agora fica ausente e marcada.
- Lacunas maiores que 6 h eram preenchidas parcialmente. Agora ficam inteiras como ausentes.
- As últimas horas do ano eram extrapoladas repetindo o último valor. Agora ficam entre dois passos reais.

### Removed
- Série fictícia de estação meteorológica.
- Scripts numerados, substituídos pelo comando do pacote.
- Pasta `src/` vazia, `data/interim/` sem uso e rascunhos de postagem.

## [0.1.0] - 2026-04-24

### Added
- Estrutura didática inicial com dados fictícios de estação meteorológica e de reanálise, scripts de inventário, validação, preparo e gráficos, notebook e documentação metodológica.
