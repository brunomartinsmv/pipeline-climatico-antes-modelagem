"""Gera os CSVs fictícios de `data/raw/` de forma determinística.

Os arquivos imitam o formato de uma estação automática do INMET (horária) e de
uma série do ERA5 em um ponto de grade (3 horas). Os valores são inventados:
não representam nenhuma estação, localidade ou reanálise real.
"""

import numpy as np
import pandas as pd

from pipeline_climatico import ARQUIVO_ERA5, ARQUIVO_INMET, indice_horario_anual

SEMENTE = 20240101

# Lacunas propositais: (variável, duração em horas). A lacuna de 10 h na
# temperatura é longa demais para interpolação e deve continuar ausente.
LACUNAS_INMET = [
    ("temperatura_c", 3),
    ("temperatura_c", 5),
    ("temperatura_c", 6),
    ("temperatura_c", 10),
    ("umidade_relativa_pct", 4),
    ("umidade_relativa_pct", 6),
    ("precipitacao_mm", 2),
    ("precipitacao_mm", 5),
]
HORARIOS_SEM_REGISTRO = 11


def _ciclo_anual(dia_do_ano: np.ndarray) -> np.ndarray:
    """Vale 1 em meados de janeiro (verão austral) e -1 em meados de julho."""
    return np.cos(2 * np.pi * (dia_do_ano - 15) / 366)


def _ruido_ar1(rng: np.random.Generator, n: int, phi: float, desvio: float) -> np.ndarray:
    choques = rng.normal(0, desvio * np.sqrt(1 - phi**2), n)
    serie = np.empty(n)
    serie[0] = rng.normal(0, desvio)
    for i in range(1, n):
        serie[i] = phi * serie[i - 1] + choques[i]
    return serie


def gerar_referencia(rng: np.random.Generator) -> pd.DataFrame:
    """Série horária 'verdadeira' da qual as duas fontes fictícias derivam."""
    indice = indice_horario_anual()
    dia = indice.day_of_year.to_numpy()
    hora = indice.hour.to_numpy()
    n = len(indice)
    anual = _ciclo_anual(dia)

    media_diaria = 23.0 + 2.0 * anual
    temperatura = media_diaria + 5.0 * np.cos(2 * np.pi * (hora - 15) / 24) + _ruido_ar1(rng, n, 0.95, 1.2)
    umidade = 68 + 12 * anual - 3.0 * (temperatura - media_diaria) + _ruido_ar1(rng, n, 0.9, 4.0)

    # Chuva concentrada no verão e à tarde, como em regimes de monção sul-americana.
    prob = (0.02 + 0.10 * np.clip(anual, 0, None)) * (1 + 0.8 * np.cos(2 * np.pi * (hora - 16) / 24))
    chove = rng.random(n) < prob
    chuva = np.where(chove, rng.gamma(0.8, 2.2, n), 0.0)

    return pd.DataFrame(
        {"temperatura_c": temperatura, "umidade_relativa_pct": np.clip(umidade, 20, 100), "precipitacao_mm": chuva},
        index=indice,
    )


def gerar_inmet(referencia: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "fonte": "INMET_EXEMPLO",
            "estacao": "ESTACAO_FICTICIA",
            "temperatura_c": referencia["temperatura_c"].round(1),
            "umidade_relativa_pct": referencia["umidade_relativa_pct"].round(0),
            # Pluviômetro de báscula: resolução de 0,2 mm.
            "precipitacao_mm": (referencia["precipitacao_mm"] / 0.2).round() * 0.2,
        },
        index=referencia.index,
    )
    df["precipitacao_mm"] = df["precipitacao_mm"].round(1)

    n = len(df)
    for coluna, duracao in LACUNAS_INMET:
        inicio = int(rng.integers(24, n - 24 - duracao))
        df.iloc[inicio : inicio + duracao, df.columns.get_loc(coluna)] = np.nan

    sem_registro = rng.choice(np.arange(1, n - 1), size=HORARIOS_SEM_REGISTRO, replace=False)
    df = df.drop(df.index[sem_registro])
    return df.reset_index()


def gerar_era5(referencia: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """Saída a cada 3 h. A chuva é o acumulado das 3 horas que começam no horário indicado."""
    temperatura = referencia["temperatura_c"].rolling(3, center=True, min_periods=1).mean()
    temperatura_3h = temperatura.iloc[::3] - 0.6 + rng.normal(0, 0.4, len(temperatura) // 3)

    soma_3h = referencia["precipitacao_mm"].resample("3h").sum()
    # Reanálises tendem a espalhar a chuva em eventos mais fracos e frequentes.
    suavizada = 0.5 * soma_3h + 0.25 * soma_3h.shift(1, fill_value=0) + 0.25 * soma_3h.shift(-1, fill_value=0)
    precip_m = (0.75 * suavizada / 1000).where(lambda s: s > 1e-5, 0.0)

    return pd.DataFrame(
        {
            "data_hora": temperatura_3h.index,
            "fonte": "ERA5_EXEMPLO",
            "ponto_grade": "GRADE_FICTICIA_A",
            "temperatura_2m_k": (temperatura_3h + 273.15).round(2).to_numpy(),
            "precipitacao_total_m": precip_m.round(5).to_numpy(),
        }
    )


def gerar() -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(SEMENTE)
    referencia = gerar_referencia(rng)
    return gerar_inmet(referencia, rng), gerar_era5(referencia, rng)


def para_csv(df: pd.DataFrame) -> str:
    return df.to_csv(index=False, date_format="%Y-%m-%d %H:%M", lineterminator="\n")


def salvar() -> None:
    inmet, era5 = gerar()
    ARQUIVO_INMET.parent.mkdir(parents=True, exist_ok=True)
    ARQUIVO_INMET.write_text(para_csv(inmet), encoding="utf-8")
    ARQUIVO_ERA5.write_text(para_csv(era5), encoding="utf-8")
    print(f"INMET fictício: {len(inmet)} linhas em {ARQUIVO_INMET}")
    print(f"ERA5 fictício: {len(era5)} linhas em {ARQUIVO_ERA5}")
