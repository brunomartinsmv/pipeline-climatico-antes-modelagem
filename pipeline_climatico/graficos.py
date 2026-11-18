"""Etapa 7: painéis mensais da base processada e das falhas tratadas."""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from pipeline_climatico import ANO_EXEMPLO, ARQUIVO_BASE, FIGURAS

COR_TEMPERATURA = "#a65335"
COR_ORVALHO = "#1f5a85"
COR_UMIDADE = "#3f7f58"
COR_CHUVA = "#1f5a85"
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]

ESTILO = {
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


def _eixo_mensal(ax: plt.Axes) -> None:
    ax.set_xlim(pd.Timestamp(f"{ANO_EXEMPLO}-01-01"), pd.Timestamp(f"{ANO_EXEMPLO + 1}-01-01"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=15))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: MESES[mdates.num2date(x).month - 1]))
    ax.grid(True, axis="y", color="#d9d9d9", linewidth=0.8)


def _mensal(df: pd.DataFrame, colunas: list[str], regra: str) -> pd.DataFrame:
    agrupado = df.set_index("data_hora")[colunas].resample("MS")
    mensal = agrupado.sum(min_count=1) if regra == "soma" else agrupado.mean()
    # Cada valor mensal é desenhado no meio do mês a que se refere.
    return mensal.set_axis(mensal.index + pd.Timedelta(days=14))


def painel_variaveis(df: pd.DataFrame) -> plt.Figure:
    fig, (ax_t, ax_u, ax_p) = plt.subplots(3, 1, figsize=(10, 9.5), sharex=True)

    temp = _mensal(df, ["temperatura_c", "ponto_orvalho_c"], "media")
    ax_t.plot(temp.index, temp["temperatura_c"], marker="o", color=COR_TEMPERATURA, label="temperatura (t2m)")
    ax_t.plot(temp.index, temp["ponto_orvalho_c"], marker="s", color=COR_ORVALHO, label="ponto de orvalho (d2m)")
    ax_t.set_ylabel("°C")
    ax_t.set_title("(a) Temperatura e ponto de orvalho a 2 m, média mensal", loc="left", weight="bold")
    ax_t.legend(loc="lower left", ncols=2)

    umid = _mensal(df, ["umidade_relativa_pct"], "media")
    ax_u.plot(umid.index, umid["umidade_relativa_pct"], marker="o", color=COR_UMIDADE)
    ax_u.set_ylabel("%")
    ax_u.set_title("(b) Umidade relativa derivada de t2m e d2m, média mensal", loc="left", weight="bold")

    chuva = _mensal(df, ["precipitacao_mm"], "soma")
    ax_p.bar(chuva.index, chuva["precipitacao_mm"], width=22, color=COR_CHUVA)
    ax_p.set_ylabel("mm")
    ax_p.set_title("(c) Precipitação total (tp), soma mensal", loc="left", weight="bold")

    for ax in (ax_t, ax_u, ax_p):
        _eixo_mensal(ax)
    fig.suptitle("ERA5 fictício processado, agregado por mês", fontsize=14, weight="bold")
    fig.text(
        0.5,
        0.935,
        "Dados inventados para fins didáticos. Horas com chuva ausente ficam fora do total.",
        ha="center",
        color="#444444",
    )
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.05, top=0.89, hspace=0.35)
    return fig


def painel_falhas(df: pd.DataFrame) -> plt.Figure:
    df = df.assign(temperatura_c_ausente=df["temperatura_c"].isna())
    series = {
        "passo_inserido": ("passo inserido na grade", "#4a4a4a"),
        "temperatura_c_imputado": ("temperatura interpolada", COR_TEMPERATURA),
        "ponto_orvalho_c_imputado": ("orvalho interpolado", COR_ORVALHO),
        "temperatura_c_ausente": ("temperatura mantida ausente", "#e0a98f"),
        "precipitacao_mm_ausente": ("chuva mantida ausente", COR_UMIDADE),
    }
    mensal = df.set_index("data_hora")[list(series)].resample("MS").sum()

    fig, ax = plt.subplots(figsize=(10, 4.8))
    largura = 0.16
    meses = range(len(mensal))
    for i, (coluna, (rotulo, cor)) in enumerate(series.items()):
        ax.bar([m + (i - 2) * largura for m in meses], mensal[coluna], width=largura, color=cor, label=rotulo)
    ax.set_title("Falhas tratadas no ERA5 fictício", loc="left", fontsize=13, weight="bold")
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
    plt.switch_backend("Agg")
    with plt.rc_context(ESTILO):
        for nome, desenhar in (
            ("painel_mensal_variaveis_processadas.png", painel_variaveis),
            ("painel_mensal_falhas_era5.png", painel_falhas),
        ):
            fig = desenhar(df)
            saida = FIGURAS / nome
            fig.savefig(saida, dpi=150, metadata={"Software": None})
            plt.close(fig)
            print(f"Figura salva em: {saida}")
