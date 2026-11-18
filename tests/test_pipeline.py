import numpy as np
import pandas as pd
import pytest

from pipeline_climatico import ARQUIVO_ERA5, dados_ficticios, indice_horario_anual, inspecao, preparo


@pytest.fixture(scope="module")
def base():
    return preparo.preparar_base()


@pytest.fixture(scope="module")
def bruto():
    return pd.read_csv(ARQUIVO_ERA5, parse_dates=["valid_time"]).set_index("valid_time")


def test_csv_bruto_coincide_com_o_gerador():
    assert ARQUIVO_ERA5.read_text(encoding="utf-8") == dados_ficticios.para_csv(dados_ficticios.gerar())


def test_estrutura_do_bruto_e_valida():
    resultado = inspecao.validar()
    assert resultado["colunas_extras"] == []
    assert resultado["passos_sem_registro"] == sum(dados_ficticios.PASSOS_SEM_REGISTRO)
    assert resultado["orvalho_acima_da_temperatura"] == 0


def test_inventario_registra_unidades():
    tabela = inspecao.inventariar().set_index("variavel")
    assert tabela.loc["t2m", "unidade"] == "K"
    assert tabela.loc["tp", "unidade"] == "m"


@pytest.mark.parametrize(
    ("alteracao", "mensagem"),
    [
        (lambda linhas: linhas + [linhas[1]], "duplicadas"),
        (lambda linhas: [linhas[0], linhas[2], linhas[1]] + linhas[3:], "fora de ordem"),
        (lambda linhas: [linhas[0], "," + linhas[1].split(",", 1)[1]] + linhas[2:], "ilegíveis"),
        (lambda linhas: [linhas[0].replace(",tp", ",chuva")] + linhas[1:], "faltantes"),
    ],
)
def test_validacao_acusa_problemas(tmp_path, alteracao, mensagem):
    copia = tmp_path / ARQUIVO_ERA5.name
    linhas = ARQUIVO_ERA5.read_text(encoding="utf-8").splitlines()
    copia.write_text("\n".join(alteracao(linhas)) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match=mensagem):
        inspecao.validar(copia)


def test_base_cobre_todas_as_horas_do_ano(base):
    assert base["data_hora"].tolist() == indice_horario_anual().tolist()
    assert base.columns.tolist() == preparo.COLUNAS_BASE


def test_conversao_de_kelvin_nos_passos_originais(base, bruto):
    passo = bruto["t2m"].dropna().index[10]
    assert base.set_index("data_hora").loc[passo, "temperatura_c"] == pytest.approx(bruto.loc[passo, "t2m"] - 273.15)


def test_umidade_relativa_por_magnus():
    rh = preparo.umidade_relativa(pd.Series([25.0, 20.0]), pd.Series([25.0, 10.0]))
    assert rh.iloc[0] == pytest.approx(100)
    assert rh.iloc[1] == pytest.approx(52.5, abs=0.5)


def _total_esperado_no_ano(tp_m: pd.Series) -> float:
    tp_mm = tp_m * 1000
    # O acumulado das 00h de 01/01/2024 cobre 22h e 23h de 2023: só um terço entra no ano.
    # O das 00h de 01/01/2025 cobre 22h e 23h de 2024 e 00h de 2025: entram dois terços.
    return tp_mm.iloc[0] / 3 + tp_mm.iloc[1:-1].sum() + tp_mm.iloc[-1] * 2 / 3


def test_precipitacao_conserva_o_total(base, bruto):
    assert base["precipitacao_mm"].sum() == pytest.approx(_total_esperado_no_ano(bruto["tp"]))


def test_precipitacao_conserva_o_total_com_chuva_nas_bordas(tmp_path, bruto):
    # No CSV versionado o primeiro e o último acumulados são zero e esconderiam erros de borda.
    editado = bruto.copy()
    editado.iloc[0, editado.columns.get_loc("tp")] = 0.0045
    editado.iloc[-1, editado.columns.get_loc("tp")] = 0.003
    copia = tmp_path / ARQUIVO_ERA5.name
    editado.reset_index().to_csv(copia, index=False, date_format="%Y-%m-%d %H:%M")

    base = preparo.preparar_base(copia)
    ultimo_dia = base.set_index("data_hora").loc["2024-12-31 22:00":, "precipitacao_mm"]
    assert ultimo_dia.tolist() == pytest.approx([1.0, 1.0])
    assert base["precipitacao_mm"].iloc[0] == pytest.approx(1.5)
    assert base["precipitacao_mm"].sum() == pytest.approx(_total_esperado_no_ano(editado["tp"]))


def test_precipitacao_ausente_nao_vaza_para_vizinhos(base, bruto):
    grade = preparo.ler_bruto()
    passos_sem_chuva = grade.index[grade["tp"].isna()]
    assert base["precipitacao_mm_ausente"].sum() == 3 * len(passos_sem_chuva)
    ausentes = base.loc[base["precipitacao_mm_ausente"], "data_hora"]
    assert set(ausentes.dt.ceil("3h")) == set(passos_sem_chuva)


def test_lacuna_longa_de_temperatura_fica_inteira_ausente(base):
    ausente = base["temperatura_c"].isna()
    # 4 passos ausentes = 4 horários + as 2 horas entre cada par = 3 * 4 + 2 horas
    assert ausente.sum() == 3 * 4 + 2
    assert not (ausente & base["temperatura_c_imputado"]).any()


def test_preencher_lacunas_curtas_respeita_o_limite_em_horas():
    indice = pd.date_range("2024-01-01", periods=8, freq="3h")
    valores = [0, np.nan, 6, 9, np.nan, np.nan, np.nan, 21]
    tratada, imputado = preparo.preencher_lacunas_curtas(pd.Series(valores, index=indice, dtype=float), 6, 3)
    assert tratada.iloc[1] == 3
    assert tratada.iloc[4:7].isna().all()
    assert imputado.tolist() == [False, True] + [False] * 6


def test_flags_marcam_horas_fora_da_grade_e_passos_inseridos(base, bruto):
    assert base["hora_interpolada"].sum() == len(base) * 2 / 3
    assert base["passo_inserido"].sum() == sum(dados_ficticios.PASSOS_SEM_REGISTRO)
