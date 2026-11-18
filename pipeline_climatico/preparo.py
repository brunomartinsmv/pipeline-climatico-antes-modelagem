"""Etapas 3 a 6: padronizar, tratar lacunas, alinhar resoluções e gerar a base processada."""

import pandas as pd

from pipeline_climatico import ARQUIVO_BASE, ARQUIVO_ERA5, ARQUIVO_INMET, indice_horario_anual

LACUNA_MAXIMA_HORAS = 6
PASSO_ERA5_HORAS = 3

COLUNAS_BASE = [
    "data_hora",
    "temperatura_inmet_c",
    "umidade_relativa_inmet_pct",
    "precipitacao_inmet_mm",
    "temperatura_inmet_c_imputado",
    "umidade_relativa_inmet_pct_imputado",
    "precipitacao_inmet_mm_ausente",
    "registro_inmet_inserido",
    "temperatura_era5_c",
    "precipitacao_era5_mm",
    "registro_era5_interpolado",
]


def preencher_lacunas_curtas(serie: pd.Series, max_horas: int = LACUNA_MAXIMA_HORAS) -> tuple[pd.Series, pd.Series]:
    """Interpola no tempo apenas lacunas internas com até `max_horas` seguidas.

    Lacunas mais longas ficam inteiras como ausentes, em vez de parcialmente
    preenchidas. Retorna a série tratada e a máscara dos valores imputados.
    """
    ausente = serie.isna()
    bloco = (ausente != ausente.shift()).cumsum()
    tamanho = ausente.groupby(bloco).transform("sum")
    curta = ausente & (tamanho <= max_horas)
    interpolada = serie.interpolate(method="time", limit_area="inside")
    tratada = serie.where(~curta, interpolada)
    return tratada, curta & tratada.notna()


def preparar_inmet() -> pd.DataFrame:
    bruto = pd.read_csv(ARQUIVO_INMET, parse_dates=["data_hora"]).set_index("data_hora").sort_index()
    base = bruto.reindex(indice_horario_anual())
    base = base.rename(
        columns={
            "temperatura_c": "temperatura_inmet_c",
            "umidade_relativa_pct": "umidade_relativa_inmet_pct",
            "precipitacao_mm": "precipitacao_inmet_mm",
        }
    )
    base["registro_inmet_inserido"] = base["fonte"].isna()

    for coluna in ("temperatura_inmet_c", "umidade_relativa_inmet_pct"):
        base[coluna], base[f"{coluna}_imputado"] = preencher_lacunas_curtas(base[coluna])
    base["umidade_relativa_inmet_pct"] = base["umidade_relativa_inmet_pct"].clip(0, 100)

    # Chuva não é interpolada nem trocada por zero: uma hora sem registro não é uma hora seca.
    base["precipitacao_inmet_mm_ausente"] = base["precipitacao_inmet_mm"].isna()
    return base


def preparar_era5() -> pd.DataFrame:
    bruto = pd.read_csv(ARQUIVO_ERA5, parse_dates=["data_hora"]).set_index("data_hora").sort_index()
    indice = indice_horario_anual()

    temperatura = (bruto["temperatura_2m_k"] - 273.15).reindex(indice)
    interpolado = temperatura.isna()
    temperatura = temperatura.interpolate(method="time", limit_direction="both")

    # Acumulado de 3 h (m) -> mm, repartido igualmente entre as 3 horas que ele cobre.
    # Interpolar um acumulado multiplicaria o total anual pelo número de passos.
    precipitacao = (bruto["precipitacao_total_m"] * 1000).reindex(indice, method="ffill") / PASSO_ERA5_HORAS

    return pd.DataFrame(
        {
            "temperatura_era5_c": temperatura,
            "precipitacao_era5_mm": precipitacao,
            "registro_era5_interpolado": interpolado,
        },
        index=indice,
    )


def preparar_base() -> pd.DataFrame:
    base = preparar_inmet().join(preparar_era5(), how="inner")
    return base.reset_index()[COLUNAS_BASE]


def executar() -> pd.DataFrame:
    base = preparar_base()
    ARQUIVO_BASE.parent.mkdir(parents=True, exist_ok=True)
    base.to_csv(ARQUIVO_BASE, index=False, date_format="%Y-%m-%d %H:%M")
    print(f"Base fictícia processada: {len(base)} linhas em {ARQUIVO_BASE}")
    return base
