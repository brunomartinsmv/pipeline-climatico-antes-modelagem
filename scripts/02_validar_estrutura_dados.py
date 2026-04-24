"""Valida a estrutura minima dos dados ficticios."""

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"

COLUNAS_ESPERADAS = {
    "exemplo_inmet_ficticio.csv": {
        "data_hora",
        "fonte",
        "estacao",
        "temperatura_c",
        "umidade_relativa_pct",
        "precipitacao_mm",
    },
    "exemplo_era5_ficticio.csv": {
        "data_hora",
        "fonte",
        "ponto_grade",
        "temperatura_2m_k",
        "precipitacao_total_m",
    },
}


def validar_arquivo(nome: str, colunas_esperadas: set[str]) -> None:
    caminho = RAW_DIR / nome
    df = pd.read_csv(caminho)
    colunas_encontradas = set(df.columns)
    faltantes = sorted(colunas_esperadas - colunas_encontradas)
    extras = sorted(colunas_encontradas - colunas_esperadas)

    if faltantes:
        raise ValueError(f"{nome}: colunas faltantes: {faltantes}")

    print(f"{nome}: estrutura valida; colunas extras: {extras or 'nenhuma'}")


def main() -> None:
    for nome, colunas in COLUNAS_ESPERADAS.items():
        validar_arquivo(nome, colunas)


if __name__ == "__main__":
    main()

