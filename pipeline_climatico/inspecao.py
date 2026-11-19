"""Etapas 1 e 2: inventariar variáveis e validar a estrutura do arquivo bruto."""

from pathlib import Path

import pandas as pd

from pipeline_climatico import ARQUIVO_ERA5, indice_era5

COLUNAS_ESPERADAS = {"valid_time", "ponto_grade", "t2m", "d2m", "tp"}

# Metadados que o CSV não carrega e que precisam ser registrados à parte.
METADADOS = {
    "valid_time": ("tempo de validade", "UTC", "instantâneo"),
    "ponto_grade": ("identificador do ponto", "-", "-"),
    "t2m": ("temperatura do ar a 2 m", "K", "instantânea"),
    "d2m": ("ponto de orvalho a 2 m", "K", "instantâneo"),
    "tp": ("precipitação total", "m", "acumulada nas 3 h que terminam em valid_time (neste arquivo)"),
}


def inventariar(caminho: Path = ARQUIVO_ERA5) -> pd.DataFrame:
    """Lista colunas, significado, unidade, tipo inferido e valores ausentes."""
    df = pd.read_csv(caminho)
    return pd.DataFrame(
        {
            "variavel": df.columns,
            "significado": [METADADOS.get(c, ("?",))[0] for c in df.columns],
            "unidade": [METADADOS.get(c, ("", "?"))[1] for c in df.columns],
            "natureza": [METADADOS.get(c, ("", "", "?"))[2] for c in df.columns],
            "tipo_inferido": [str(tipo) for tipo in df.dtypes],
            "ausentes": df.isna().sum().to_numpy(),
        }
    )


def validar(caminho: Path = ARQUIVO_ERA5) -> dict:
    """Confere colunas e datas válidas, únicas, ordenadas e na grade de 3 h. Levanta ValueError se algo falhar."""
    nome = caminho.name
    df = pd.read_csv(caminho)
    faltantes = sorted(COLUNAS_ESPERADAS - set(df.columns))
    if faltantes:
        raise ValueError(f"{nome}: colunas faltantes: {faltantes}")

    tempo = pd.to_datetime(df["valid_time"], errors="coerce")
    if tempo.isna().any():
        raise ValueError(f"{nome}: {int(tempo.isna().sum())} datas vazias ou ilegíveis")
    if tempo.duplicated().any():
        raise ValueError(f"{nome}: existem datas duplicadas")
    if not tempo.is_monotonic_increasing:
        raise ValueError(f"{nome}: datas fora de ordem")

    # A grade esperada é fixa (passos de 3 h do ano). Um horário fora dela seria descartado no preparo.
    esperados = indice_era5()
    fora_da_grade = pd.DatetimeIndex(tempo).difference(esperados)
    if len(fora_da_grade):
        raise ValueError(f"{nome}: {len(fora_da_grade)} horários fora da grade de 3 h, como {fora_da_grade[0]}")

    passo = tempo.diff().mode().iloc[0]
    return {
        "arquivo": nome,
        "linhas": len(df),
        "inicio": tempo.min(),
        "fim": tempo.max(),
        "passo_mais_comum": passo,
        "passos_sem_registro": len(esperados.difference(pd.DatetimeIndex(tempo))),
        "valores_ausentes": int(df[["t2m", "d2m", "tp"]].isna().sum().sum()),
        "orvalho_acima_da_temperatura": int((df["d2m"] > df["t2m"] + 0.05).sum()),
        "colunas_extras": sorted(set(df.columns) - COLUNAS_ESPERADAS),
    }


def executar_inventario() -> None:
    print(inventariar().to_string(index=False))


def executar_validacao() -> None:
    r = validar()
    print(
        f"{r['arquivo']}: estrutura válida; {r['linhas']} linhas de {r['inicio']} a {r['fim']}; "
        f"passo {r['passo_mais_comum']}; {r['passos_sem_registro']} passos sem registro; "
        f"{r['valores_ausentes']} valores ausentes; "
        f"{r['orvalho_acima_da_temperatura']} casos de orvalho acima da temperatura; "
        f"colunas extras: {r['colunas_extras'] or 'nenhuma'}"
    )
