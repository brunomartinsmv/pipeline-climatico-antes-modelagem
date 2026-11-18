"""Etapas 1 e 2: inventariar variáveis e validar a estrutura dos arquivos brutos."""

from pathlib import Path

import pandas as pd

from pipeline_climatico import ARQUIVO_ERA5, ARQUIVO_INMET

COLUNAS_ESPERADAS = {
    ARQUIVO_INMET.name: {
        "data_hora",
        "fonte",
        "estacao",
        "temperatura_c",
        "umidade_relativa_pct",
        "precipitacao_mm",
    },
    ARQUIVO_ERA5.name: {
        "data_hora",
        "fonte",
        "ponto_grade",
        "temperatura_2m_k",
        "precipitacao_total_m",
    },
}


def inventariar(caminho: Path) -> pd.DataFrame:
    """Lista colunas, tipo inferido e quantidade de valores ausentes de um CSV."""
    df = pd.read_csv(caminho)
    return pd.DataFrame(
        {
            "arquivo": caminho.name,
            "variavel": df.columns,
            "tipo_inferido": [str(tipo) for tipo in df.dtypes],
            "ausentes": df.isna().sum().to_numpy(),
        }
    )


def validar(caminho: Path) -> dict:
    """Confere colunas, datas únicas e ordenadas. Levanta ValueError se algo falhar."""
    nome = caminho.name
    df = pd.read_csv(caminho, parse_dates=["data_hora"])
    faltantes = sorted(COLUNAS_ESPERADAS[nome] - set(df.columns))
    if faltantes:
        raise ValueError(f"{nome}: colunas faltantes: {faltantes}")
    if df["data_hora"].duplicated().any():
        raise ValueError(f"{nome}: existem datas duplicadas")
    if not df["data_hora"].is_monotonic_increasing:
        raise ValueError(f"{nome}: datas fora de ordem")

    return {
        "arquivo": nome,
        "linhas": len(df),
        "inicio": df["data_hora"].min(),
        "fim": df["data_hora"].max(),
        "passo_mais_comum": df["data_hora"].diff().mode().iloc[0],
        "valores_ausentes": int(df.isna().sum().sum()),
        "colunas_extras": sorted(set(df.columns) - COLUNAS_ESPERADAS[nome]),
    }


def executar_inventario() -> None:
    tabela = pd.concat([inventariar(ARQUIVO_INMET), inventariar(ARQUIVO_ERA5)], ignore_index=True)
    print(tabela.to_string(index=False))


def executar_validacao() -> None:
    for caminho in (ARQUIVO_INMET, ARQUIVO_ERA5):
        r = validar(caminho)
        print(
            f"{r['arquivo']}: estrutura válida; {r['linhas']} linhas de {r['inicio']} a {r['fim']}; "
            f"passo {r['passo_mais_comum']}; {r['valores_ausentes']} valores ausentes; "
            f"colunas extras: {r['colunas_extras'] or 'nenhuma'}"
        )
