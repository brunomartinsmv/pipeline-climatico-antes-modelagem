"""Gera paineis mensais da base processada ficticia e das imputacoes."""

import os
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
FIGURES_DIR = BASE_DIR / "figures"
MPL_CACHE_DIR = FIGURES_DIR / ".matplotlib-cache"
MPL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE_DIR))
os.environ.setdefault("XDG_CACHE_HOME", str(MPL_CACHE_DIR))

import matplotlib
import matplotlib.dates as mdates

matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROCESSED_BASE = PROCESSED_DIR / "base_climatica_ficticia_processada.csv"

plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#222222",
        "axes.labelcolor": "#222222",
        "axes.titlecolor": "#111111",
        "xtick.color": "#222222",
        "ytick.color": "#222222",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "savefig.facecolor": "white",
    }
)


VARIAVEIS_PROCESSADAS = {
    "temperatura_inmet_c": {
        "rotulo": "Temperatura INMET",
        "unidade": "graus C",
        "agregacao": "mean",
        "cor": "#1f5a85",
    },
    "umidade_relativa_pct": {
        "rotulo": "Umidade relativa INMET",
        "unidade": "%",
        "agregacao": "mean",
        "cor": "#3f7f58",
    },
    "precipitacao_mm": {
        "rotulo": "Precipitacao INMET",
        "unidade": "mm",
        "agregacao": "sum",
        "cor": "#8a6238",
    },
    "temperatura_era5_c": {
        "rotulo": "Temperatura ERA5",
        "unidade": "graus C",
        "agregacao": "mean",
        "cor": "#6e609e",
    },
    "precipitacao_era5_mm": {
        "rotulo": "Precipitacao ERA5",
        "unidade": "mm",
        "agregacao": "sum",
        "cor": "#a65335",
    },
}

FLAGS_IMPUTACAO = [
    "temperatura_inmet_c_imputado",
    "umidade_relativa_pct_imputado",
    "precipitacao_mm_imputado",
    "registro_inmet_inserido",
]


def garantir_base_processada() -> None:
    if PROCESSED_BASE.exists():
        return

    import importlib.util

    script = BASE_DIR / "scripts" / "03_preparar_base_exemplo.py"
    spec = importlib.util.spec_from_file_location("preparar_base_exemplo", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Nao foi possivel carregar o script de preparo da base.")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    modulo.preparar_base().to_csv(PROCESSED_BASE, index=False)


def agregar_mensal(df: pd.DataFrame, coluna: str, agregacao: str) -> pd.Series:
    serie = df.set_index("data_hora")[coluna]
    if agregacao == "sum":
        return serie.resample("MS").sum()
    return serie.resample("MS").mean()


def configurar_eixo(ax: plt.Axes) -> None:
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.grid(True, axis="y", color="#d9d9d9", linewidth=0.8, alpha=0.65)
    ax.grid(False, axis="x")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.9)
    ax.spines["bottom"].set_linewidth(0.9)
    ax.tick_params(axis="x", rotation=0, length=3)
    ax.tick_params(axis="y", length=3)


def gerar_painel_variaveis(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(3, 2, figsize=(14, 10.5), constrained_layout=False)
    axes_lista = axes.ravel()
    letras = ["a", "b", "c", "d", "e"]

    for indice, (ax, (coluna, config)) in enumerate(zip(axes_lista, VARIAVEIS_PROCESSADAS.items())):
        mensal = agregar_mensal(df, coluna, config["agregacao"])
        ax.plot(
            mensal.index,
            mensal.values,
            marker="o",
            markersize=4.6,
            linewidth=1.9,
            color=config["cor"],
        )
        ax.set_title(f"({letras[indice]}) {config['rotulo']}", loc="left", pad=12, weight="bold")
        ax.set_ylabel(config["unidade"])
        configurar_eixo(ax)

    axes_lista[-1].axis("off")
    fig.suptitle(
        "Comportamento mensal das variaveis processadas",
        fontsize=16,
        weight="bold",
        y=0.975,
    )
    fig.text(
        0.5,
        0.94,
        "Exemplo didatico com dados ficticios; precipitacao agregada por soma mensal e demais variaveis por media mensal.",
        ha="center",
        va="center",
        fontsize=10,
        color="#444444",
    )
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.065, top=0.885, hspace=0.55, wspace=0.22)

    saida = FIGURES_DIR / "painel_mensal_variaveis_processadas.png"
    fig.savefig(saida, dpi=220)
    plt.close(fig)
    print(f"Painel salvo em: {saida}")


def gerar_painel_imputacoes(df: pd.DataFrame) -> None:
    mensal = df.set_index("data_hora")[FLAGS_IMPUTACAO].resample("MS").sum()
    rotulos = {
        "temperatura_inmet_c_imputado": "temperatura",
        "umidade_relativa_pct_imputado": "umidade",
        "precipitacao_mm_imputado": "precipitacao",
        "registro_inmet_inserido": "horario inserido",
    }

    fig, ax = plt.subplots(figsize=(12.5, 5.8), constrained_layout=False)
    largura = 4.5
    deslocamentos = [-7.0, -2.3, 2.3, 7.0]
    cores = ["#1f5a85", "#3f7f58", "#8a6238", "#4a4a4a"]

    for coluna, deslocamento, cor in zip(FLAGS_IMPUTACAO, deslocamentos, cores):
        x = mensal.index + pd.to_timedelta(deslocamento, unit="D")
        ax.bar(x, mensal[coluna], width=largura, color=cor, label=rotulos[coluna], alpha=0.9)

    ax.set_title("Falhas tratadas no INMET ficticio", loc="left", fontsize=15, weight="bold", pad=18)
    ax.set_ylabel("Quantidade de registros")
    ax.set_xlabel("Mes de 2024")
    configurar_eixo(ax)
    ax.legend(frameon=False, ncols=4, loc="upper center", bbox_to_anchor=(0.5, 1.08))
    fig.text(
        0.08,
        0.9,
        "Barras indicam registros inseridos ou valores preenchidos durante o preparo da base.",
        ha="left",
        va="center",
        fontsize=10,
        color="#444444",
    )
    fig.subplots_adjust(left=0.08, right=0.985, bottom=0.14, top=0.78)

    saida = FIGURES_DIR / "painel_mensal_imputacoes_inmet.png"
    fig.savefig(saida, dpi=220)
    plt.close(fig)
    print(f"Painel salvo em: {saida}")


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    garantir_base_processada()

    df = pd.read_csv(PROCESSED_BASE, parse_dates=["data_hora"])
    gerar_painel_variaveis(df)
    gerar_painel_imputacoes(df)


if __name__ == "__main__":
    main()
