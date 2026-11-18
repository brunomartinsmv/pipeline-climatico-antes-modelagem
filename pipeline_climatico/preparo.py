"""Etapas 3 a 6: padronizar, tratar lacunas, passar de 3 h para 1 h e gerar a base processada."""

from pathlib import Path

import numpy as np
import pandas as pd

from pipeline_climatico import ARQUIVO_BASE, ARQUIVO_ERA5, PASSO_ERA5_HORAS, indice_era5, indice_horario_anual

LACUNA_MAXIMA_HORAS = 6

COLUNAS_BASE = [
    "data_hora",
    "temperatura_c",
    "ponto_orvalho_c",
    "umidade_relativa_pct",
    "precipitacao_mm",
    "hora_interpolada",
    "passo_inserido",
    "temperatura_c_imputado",
    "ponto_orvalho_c_imputado",
    "precipitacao_mm_ausente",
]


def preencher_lacunas_curtas(
    serie: pd.Series, max_horas: float = LACUNA_MAXIMA_HORAS, passo_horas: float = 1
) -> tuple[pd.Series, pd.Series]:
    """Interpola no tempo apenas lacunas internas de até `max_horas`.

    A série precisa estar em grade regular de `passo_horas`; a duração de uma
    lacuna é o número de valores ausentes seguidos vezes o passo. Lacunas mais
    longas ficam inteiras como ausentes, em vez de parcialmente preenchidas.
    Retorna a série tratada e a máscara dos valores imputados.
    """
    ausente = serie.isna()
    bloco = (ausente != ausente.shift()).cumsum()
    duracao = ausente.groupby(bloco).transform("sum") * passo_horas
    curta = ausente & (duracao <= max_horas)
    interpolada = serie.interpolate(method="time", limit_area="inside")
    tratada = serie.where(~curta, interpolada)
    return tratada, curta & tratada.notna()


def umidade_relativa(temperatura_c: pd.Series, orvalho_c: pd.Series) -> pd.Series:
    """Umidade relativa (%) pela fórmula de Magnus (Alduchov e Eskridge, 1996)."""

    def pressao_vapor(t):
        return np.exp(17.625 * t / (243.04 + t))

    return (100 * pressao_vapor(orvalho_c) / pressao_vapor(temperatura_c)).clip(upper=100)


def ler_bruto(caminho: Path = ARQUIVO_ERA5) -> pd.DataFrame:
    """Lê o CSV e o coloca na grade completa de 3 h, marcando os passos que faltavam."""
    bruto = pd.read_csv(caminho, parse_dates=["valid_time"]).set_index("valid_time").sort_index()
    grade = bruto.reindex(indice_era5())
    grade["passo_inserido"] = grade["ponto_grade"].isna()
    return grade


def _para_horario(serie_3h: pd.Series, indice: pd.DatetimeIndex) -> pd.Series:
    """Grandeza instantânea: preenche as 2 horas entre passos vizinhos, sem atravessar lacunas."""
    horaria = serie_3h.reindex(indice)
    return preencher_lacunas_curtas(horaria, max_horas=PASSO_ERA5_HORAS - 1)[0]


def preparar_base(caminho: Path = ARQUIVO_ERA5) -> pd.DataFrame:
    grade = ler_bruto(caminho)
    estendido = pd.date_range(grade.index[0], grade.index[-1], freq="h")
    ano = indice_horario_anual()

    base = pd.DataFrame(index=ano)
    for origem, destino in (("t2m", "temperatura_c"), ("d2m", "ponto_orvalho_c")):
        celsius = grade[origem] - 273.15
        tratada, _ = preencher_lacunas_curtas(celsius, passo_horas=PASSO_ERA5_HORAS)
        base[destino] = _para_horario(tratada, estendido).reindex(ano)
        sem_tratamento = _para_horario(celsius, estendido).reindex(ano)
        base[f"{destino}_imputado"] = sem_tratamento.isna() & base[destino].notna()

    base["umidade_relativa_pct"] = umidade_relativa(base["temperatura_c"], base["ponto_orvalho_c"])

    # Acumulado de 3 h (m -> mm) repartido igualmente entre as 3 horas que terminam no passo.
    # O preenchimento para trás tem limite de 2 h: um passo ausente nunca empresta chuva ao vizinho.
    acumulado_mm = grade["tp"] * 1000
    base["precipitacao_mm"] = acumulado_mm.reindex(ano, method="bfill", limit=PASSO_ERA5_HORAS - 1) / PASSO_ERA5_HORAS
    base["precipitacao_mm_ausente"] = base["precipitacao_mm"].isna()

    base["hora_interpolada"] = ano.hour % PASSO_ERA5_HORAS != 0
    base["passo_inserido"] = grade["passo_inserido"].reindex(ano, fill_value=False)
    return base.reset_index()[COLUNAS_BASE]


def executar() -> pd.DataFrame:
    base = preparar_base()
    ARQUIVO_BASE.parent.mkdir(parents=True, exist_ok=True)
    base.to_csv(ARQUIVO_BASE, index=False, date_format="%Y-%m-%d %H:%M")
    print(f"Base fictícia processada: {len(base)} linhas em {ARQUIVO_BASE}")
    return base
