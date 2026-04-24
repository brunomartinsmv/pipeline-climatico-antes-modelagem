"""Prepara uma base processada ficticia a partir dos exemplos brutos."""

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def carregar_inmet() -> pd.DataFrame:
    df = pd.read_csv(RAW_DIR / "exemplo_inmet_ficticio.csv", parse_dates=["data_hora"])
    return df.rename(columns={"temperatura_c": "temperatura_inmet_c"})


def carregar_era5() -> pd.DataFrame:
    df = pd.read_csv(RAW_DIR / "exemplo_era5_ficticio.csv", parse_dates=["data_hora"])
    df["temperatura_era5_c"] = df["temperatura_2m_k"] - 273.15
    df["precipitacao_era5_mm"] = df["precipitacao_total_m"] * 1000
    return df[["data_hora", "temperatura_era5_c", "precipitacao_era5_mm"]]


def preparar_base() -> pd.DataFrame:
    inmet = carregar_inmet()
    era5 = carregar_era5()
    base = inmet.merge(era5, on="data_hora", how="inner")
    return base[
        [
            "data_hora",
            "temperatura_inmet_c",
            "umidade_relativa_pct",
            "precipitacao_mm",
            "temperatura_era5_c",
            "precipitacao_era5_mm",
        ]
    ]


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    base = preparar_base()
    saida = PROCESSED_DIR / "base_climatica_ficticia_processada.csv"
    base.to_csv(saida, index=False)
    print(f"Base ficticia criada em: {saida}")


if __name__ == "__main__":
    main()

