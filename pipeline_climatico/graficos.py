"""Etapa 7: painéis mensais da base processada e das falhas tratadas."""

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from pipeline_climatico import ANO_EXEMPLO, ARQUIVO_BASE, FIGURAS  # noqa: E402

COR_INMET = "#1f5a85"
COR_ERA5 = "#a65335"
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]

plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#222222",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.size": 10,
        "axes.titlesize": 11,
        "legend.fontsize": 9,
        "legend.frameon": False,
        "savefig.facecolor": "white",
    }
)


def _eixo_mensal(ax: plt.Axes) -> None:
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: MESES[mdates.num2date(x).month - 1]))
    ax.grid(True, axis="y", color="#d9d9d9", linewidth=0.8)


def _mensal(df: pd.DataFrame, colunas: list[str], regra: str) -> pd.DataFrame:
    agrupado = df.set_index("data_hora")[colunas].resample("MS")
    return agrupado.sum(min_count=1) if regra == "soma" else agrupado.mean()


def painel_variaveis(df: pd.DataFrame) -> plt.Figure:
    fig, (ax_t, ax_u, ax_p) = plt.subplots(3, 1, figsize=(10, 9.5), sharex=True)

    temp = _mensal(df, ["temperatura_inmet_c", "temperatura_era5_c"], "media")
    ax_t.plot(temp.index, temp["temperatura_inmet_c"], marker="o", color=COR_INMET, label="INMET")
    ax_t.plot(temp.index, temp["temperatura_era5_c"], marker="s", color=COR_ERA5, label="ERA5")
    ax_t.set_ylabel("°C")
    ax_t.set_title("(a) Temperatura do ar, média mensal", loc="left", weight="bold")
    ax_t.legend(loc="upper center", ncols=2)

    umid = _mensal(df, ["umidade_relativa_inmet_pct"], "media")
    ax_u.plot(umid.index, umid["umidade_relativa_inmet_pct"], marker="o", color=COR_INMET)
    ax_u.set_ylabel("%")
    ax_u.set_title("(b) Umidade relativa INMET, média mensal", loc="left", weight="bold")

    chuva = _mensal(df, ["precipitacao_inmet_mm", "precipitacao_era5_mm"], "soma")
    deslocamento = pd.to_timedelta(5, unit="D")
    ax_p.bar(chuva.index - deslocamento, chuva["precipitacao_inmet_mm"], width=9, color=COR_INMET, label="INMET")
    ax_p.bar(chuva.index + deslocamento, chuva["precipitacao_era5_mm"], width=9, color=COR_ERA5, label="ERA5")
    ax_p.set_ylabel("mm")
    ax_p.set_title("(c) Precipitação, total mensal", loc="left", weight="bold")
    ax_p.legend(loc="upper center", ncols=2)

    for ax in (ax_t, ax_u, ax_p):
        _eixo_mensal(ax)
    fig.suptitle("Base processada fictícia, agregada por mês", fontsize=14, weight="bold")
    fig.text(
        0.5,
        0.935,
        "Dados inventados para fins didáticos. Horas sem registro de chuva no INMET ficam fora do total.",
        ha="center",
        color="#444444",
    )
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.05, top=0.89, hspace=0.35)
    return fig


def painel_falhas(df: pd.DataFrame) -> plt.Figure:
    df = df.assign(temperatura_inmet_c_ausente=df["temperatura_inmet_c"].isna())
    series = {
        "registro_inmet_inserido": ("horário inserido", "#4a4a4a"),
        "temperatura_inmet_c_imputado": ("temperatura interpolada", COR_INMET),
        "umidade_relativa_inmet_pct_imputado": ("umidade interpolada", "#3f7f58"),
        "temperatura_inmet_c_ausente": ("temperatura mantida ausente", "#9bb7d0"),
        "precipitacao_inmet_mm_ausente": ("chuva mantida ausente", "#8a6238"),
    }
    mensal = df.set_index("data_hora")[list(series)].resample("MS").sum()

    fig, ax = plt.subplots(figsize=(10, 4.8))
    largura = 0.16
    meses = range(len(mensal))
    for i, (coluna, (rotulo, cor)) in enumerate(series.items()):
        ax.bar([m + (i - 2) * largura for m in meses], mensal[coluna], width=largura, color=cor, label=rotulo)
    ax.set_title("Falhas tratadas no INMET fictício", loc="left", fontsize=13, weight="bold")
    ax.set_ylabel("horas no mês")
    ax.set_xlabel(f"mês de {ANO_EXEMPLO}")
    ax.set_xticks(list(meses), [MESES[d.month - 1] for d in mensal.index])
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.grid(True, axis="y", color="#d9d9d9", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(ncols=3, loc="upper center", bbox_to_anchor=(0.5, -0.18))
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.3, top=0.9)
    return fig


def executar() -> None:
    if not ARQUIVO_BASE.exists():
        from pipeline_climatico import preparo

        preparo.executar()
    df = pd.read_csv(ARQUIVO_BASE, parse_dates=["data_hora"])
    FIGURAS.mkdir(parents=True, exist_ok=True)
    for nome, fig in (
        ("painel_mensal_variaveis_processadas.png", painel_variaveis(df)),
        ("painel_mensal_falhas_inmet.png", painel_falhas(df)),
    ):
        saida = FIGURAS / nome
        fig.savefig(saida, dpi=150, metadata={"Software": None})
        plt.close(fig)
        print(f"Figura salva em: {saida}")
