"""Gera o CSV fictício de `data/raw/` de forma determinística.

O arquivo imita uma série do ERA5 extraída para um ponto de grade, com passo de
3 horas e os nomes curtos de variável usados pelo Copernicus (`t2m`, `d2m`,
`tp`). Os valores são inventados: não representam nenhuma localidade real.
"""

import numpy as np
import pandas as pd

from pipeline_climatico import ARQUIVO_ERA5, PASSO_ERA5_HORAS, indice_era5

SEMENTE = 20240101

# Falhas propositais, em passos de 3 h. Simulam arquivos que não baixaram ou
# vieram corrompidos. A falha de 4 passos (12 h) em t2m é longa demais para
# interpolação e deve continuar ausente.
LACUNAS = [
    ("t2m", 1),
    ("t2m", 2),
    ("t2m", 4),
    ("d2m", 1),
    ("d2m", 2),
    ("tp", 1),
    ("tp", 2),
]
PASSOS_SEM_REGISTRO = [1, 1, 1, 2]  # blocos de passos inteiros que faltam no arquivo


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


def ponto_de_orvalho(temperatura_c, umidade_pct):
    """Inverte a fórmula de Magnus (Alduchov e Eskridge, 1996)."""
    gama = np.log(umidade_pct / 100) + 17.625 * temperatura_c / (243.04 + temperatura_c)
    return 243.04 * gama / (17.625 - gama)


def gerar_referencia(rng: np.random.Generator) -> pd.DataFrame:
    """Série horária contínua da qual o arquivo de 3 h é amostrado."""
    passos = indice_era5()
    indice = pd.date_range(passos[0] - pd.Timedelta(hours=PASSO_ERA5_HORAS - 1), passos[-1], freq="h")
    dia = indice.day_of_year.to_numpy()
    hora = indice.hour.to_numpy()
    n = len(indice)
    anual = _ciclo_anual(dia)

    media_diaria = 23.0 + 2.0 * anual
    temperatura = media_diaria + 5.0 * np.cos(2 * np.pi * (hora - 15) / 24) + _ruido_ar1(rng, n, 0.95, 1.2)
    umidade = 68 + 12 * anual - 3.0 * (temperatura - media_diaria) + _ruido_ar1(rng, n, 0.9, 4.0)

    # Chuva concentrada no verão e à tarde, como em regimes de monção sul-americana.
    prob = (0.03 + 0.12 * np.clip(anual, 0, None)) * (1 + 0.8 * np.cos(2 * np.pi * (hora - 16) / 24))
    chuva = np.where(rng.random(n) < prob, rng.gamma(0.8, 2.0, n), 0.0)

    return pd.DataFrame(
        {
            "temperatura_c": temperatura,
            "orvalho_c": ponto_de_orvalho(temperatura, np.clip(umidade, 20, 99)),
            "precipitacao_mm": chuva,
        },
        index=indice,
    )


def gerar_era5(referencia: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    passos = indice_era5()
    # Como no ERA5 real, o acumulado rotulado em t cobre as 3 horas que terminam em t.
    acumulado = referencia["precipitacao_mm"].rolling(PASSO_ERA5_HORAS).sum().reindex(passos)

    df = pd.DataFrame(
        {
            "valid_time": passos,
            "ponto_grade": "GRADE_FICTICIA_A",
            "t2m": (referencia["temperatura_c"].reindex(passos) + 273.15).round(2).to_numpy(),
            "d2m": (referencia["orvalho_c"].reindex(passos) + 273.15).round(2).to_numpy(),
            "tp": (acumulado / 1000).round(5).to_numpy(),
        }
    )

    n = len(df)
    for coluna, passos_falha in LACUNAS:
        inicio = int(rng.integers(8, n - 8 - passos_falha))
        df.iloc[inicio : inicio + passos_falha, df.columns.get_loc(coluna)] = np.nan

    sem_registro = []
    for tamanho in PASSOS_SEM_REGISTRO:
        inicio = int(rng.integers(8, n - 8 - tamanho))
        sem_registro.extend(range(inicio, inicio + tamanho))
    return df.drop(index=sorted(set(sem_registro))).reset_index(drop=True)


def gerar() -> pd.DataFrame:
    rng = np.random.default_rng(SEMENTE)
    return gerar_era5(gerar_referencia(rng), rng)


def para_csv(df: pd.DataFrame) -> str:
    return df.to_csv(index=False, date_format="%Y-%m-%d %H:%M", lineterminator="\n")


def salvar() -> None:
    era5 = gerar()
    ARQUIVO_ERA5.parent.mkdir(parents=True, exist_ok=True)
    ARQUIVO_ERA5.write_text(para_csv(era5), encoding="utf-8")
    print(f"ERA5 fictício: {len(era5)} linhas em {ARQUIVO_ERA5}")
