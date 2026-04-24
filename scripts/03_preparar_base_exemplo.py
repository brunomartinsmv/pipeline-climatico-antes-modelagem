"""Prepara uma base processada ficticia a partir dos exemplos brutos."""

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
ANO_EXEMPLO = 2024


def indice_horario_anual() -> pd.DatetimeIndex:
    return pd.date_range(
        f"{ANO_EXEMPLO}-01-01 00:00",
        f"{ANO_EXEMPLO}-12-31 23:00",
        freq="h",
    )


def carregar_inmet() -> pd.DataFrame:
    df = pd.read_csv(RAW_DIR / "exemplo_inmet_ficticio.csv", parse_dates=["data_hora"])
    df = df.rename(columns={"temperatura_c": "temperatura_inmet_c"})
    return df.set_index("data_hora").sort_index()


def preencher_lacunas_inmet(df: pd.DataFrame) -> pd.DataFrame:
    """Insere horas faltantes e preenche lacunas curtas por interpolacao temporal."""
    base = df.reindex(indice_horario_anual())
    colunas_numericas = ["temperatura_inmet_c", "umidade_relativa_pct", "precipitacao_mm"]

    for coluna in colunas_numericas:
        base[f"{coluna}_imputado"] = base[coluna].isna()

    base["registro_inmet_inserido"] = base["fonte"].isna()
    base["fonte"] = base["fonte"].fillna("INMET_EXEMPLO")
    base["estacao"] = base["estacao"].fillna("ESTACAO_FICTICIA")

    base[colunas_numericas] = base[colunas_numericas].interpolate(
        method="time",
        limit=6,
        limit_direction="both",
    )
    base["precipitacao_mm"] = base["precipitacao_mm"].fillna(0)
    base["umidade_relativa_pct"] = base["umidade_relativa_pct"].clip(lower=0, upper=100)
    base.index.name = "data_hora"
    return base.reset_index()


def carregar_era5() -> pd.DataFrame:
    df = pd.read_csv(RAW_DIR / "exemplo_era5_ficticio.csv", parse_dates=["data_hora"])
    df["temperatura_era5_c"] = df["temperatura_2m_k"] - 273.15
    df["precipitacao_era5_mm"] = df["precipitacao_total_m"] * 1000
    return df.set_index("data_hora")[["temperatura_era5_c", "precipitacao_era5_mm"]].sort_index()


def interpolar_era5_para_horario(df: pd.DataFrame) -> pd.DataFrame:
    base = df.reindex(indice_horario_anual())
    base["registro_era5_interpolado"] = base["temperatura_era5_c"].isna()
    base[["temperatura_era5_c", "precipitacao_era5_mm"]] = base[
        ["temperatura_era5_c", "precipitacao_era5_mm"]
    ].interpolate(method="time", limit_direction="both")
    base.index.name = "data_hora"
    return base.reset_index()


def preparar_base() -> pd.DataFrame:
    inmet = preencher_lacunas_inmet(carregar_inmet())
    era5 = interpolar_era5_para_horario(carregar_era5())
    base = inmet.merge(era5, on="data_hora", how="inner")
    return base[
        [
            "data_hora",
            "temperatura_inmet_c",
            "umidade_relativa_pct",
            "precipitacao_mm",
            "temperatura_inmet_c_imputado",
            "umidade_relativa_pct_imputado",
            "precipitacao_mm_imputado",
            "registro_inmet_inserido",
            "temperatura_era5_c",
            "precipitacao_era5_mm",
            "registro_era5_interpolado",
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
