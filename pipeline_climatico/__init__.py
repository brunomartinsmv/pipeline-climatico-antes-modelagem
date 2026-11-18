"""Exemplo didático de pipeline de dados climáticos antes da modelagem."""

from pathlib import Path

import pandas as pd

__version__ = "0.2.0"

RAIZ = Path(__file__).resolve().parents[1]
DADOS_BRUTOS = RAIZ / "data" / "raw"
DADOS_PROCESSADOS = RAIZ / "data" / "processed"
FIGURAS = RAIZ / "figures"

ARQUIVO_ERA5 = DADOS_BRUTOS / "exemplo_era5_ficticio.csv"
ARQUIVO_BASE = DADOS_PROCESSADOS / "base_climatica_ficticia_processada.csv"

ANO_EXEMPLO = 2024
PASSO_ERA5_HORAS = 3


def indice_horario_anual(ano: int = ANO_EXEMPLO) -> pd.DatetimeIndex:
    """Grade horária completa do ano, usada como referência temporal da base."""
    return pd.date_range(f"{ano}-01-01 00:00", f"{ano}-12-31 23:00", freq="h", name="data_hora")


def indice_era5(ano: int = ANO_EXEMPLO) -> pd.DatetimeIndex:
    """Passos de 3 h do ano, mais 00h do ano seguinte, que fecha o acumulado das 22h e 23h."""
    return pd.date_range(f"{ano}-01-01 00:00", f"{ano + 1}-01-01 00:00", freq=f"{PASSO_ERA5_HORAS}h", name="valid_time")
