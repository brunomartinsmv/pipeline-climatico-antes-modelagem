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


def _atrasar_uma_hora(linha: str) -> str:
    data, resto = linha.split(",", 1)
    return f"{pd.Timestamp(data) + pd.Timedelta(hours=1):%Y-%m-%d %H:%M},{resto}"


@pytest.mark.parametrize(
    ("alteracao", "mensagem"),
    [
        (lambda linhas: linhas + [linhas[1]], "duplicadas"),
        (lambda linhas: [linhas[0], linhas[2], linhas[1]] + linhas[3:], "fora de ordem"),
        (lambda linhas: [linhas[0], "," + linhas[1].split(",", 1)[1]] + linhas[2:], "ilegíveis"),
        (lambda linhas: [linhas[0].replace(",tp", ",chuva")] + linhas[1:], "faltantes"),
        (lambda linhas: [linhas[0]] + [_atrasar_uma_hora(linha) for linha in linhas[1:]], "fora da grade"),
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
    # A base guarda a chuva no horário em que a hora começa. As horas de 2024 terminam de
    # 01h de 01/01/2024 a 00h de 01/01/2025: entram todos os passos, menos o primeiro,
    # cujo acumulado cobre 21h a 00h de 2023.
    return tp_m.iloc[1:].sum() * 1000


def test_precipitacao_conserva_o_total(base, bruto):
    assert base["precipitacao_mm"].sum() == pytest.approx(_total_esperado_no_ano(bruto["tp"]))


def test_precipitacao_conserva_o_total_com_chuva_nas_bordas(tmp_path, bruto):
    # No CSV versionado os acumulados das bordas são zero e esconderiam erros.
    editado = bruto.copy()
    editado.loc["2024-01-01 00:00", "tp"] = 0.009  # chuva de 2023: não pode entrar
    editado.loc["2024-01-01 03:00", "tp"] = 0.0045
    editado.loc["2025-01-01 00:00", "tp"] = 0.003
    copia = tmp_path / ARQUIVO_ERA5.name
    editado.reset_index().to_csv(copia, index=False, date_format="%Y-%m-%d %H:%M")

    chuva = preparo.preparar_base(copia).set_index("data_hora")["precipitacao_mm"]
    assert chuva.loc[:"2024-01-01 02:00"].tolist() == pytest.approx([1.5, 1.5, 1.5])
    assert chuva.loc["2024-12-31 21:00":].tolist() == pytest.approx([1.0, 1.0, 1.0])
    assert chuva.sum() == pytest.approx(_total_esperado_no_ano(editado["tp"]))


def test_precipitacao_fica_no_mes_em_que_cai(tmp_path, bruto):
    # Chuva das 21h às 00h de 31/01 pertence a janeiro, embora o passo seja 01/02 00h.
    editado = bruto.copy()
    editado["tp"] = 0.0
    editado.loc["2024-02-01 00:00", "tp"] = 0.003
    copia = tmp_path / ARQUIVO_ERA5.name
    editado.reset_index().to_csv(copia, index=False, date_format="%Y-%m-%d %H:%M")

    chuva = preparo.preparar_base(copia).set_index("data_hora")["precipitacao_mm"]
    mensal = chuva.resample("MS").sum()
    assert mensal.loc["2024-01-01"] == pytest.approx(3.0)
    assert mensal.loc["2024-02-01"] == pytest.approx(0.0)


def test_precipitacao_ausente_nao_vaza_para_vizinhos(base, bruto):
    grade = preparo.ler_bruto()
    passos_sem_chuva = grade.index[grade["tp"].isna()]
    assert base["precipitacao_mm_ausente"].sum() == 3 * len(passos_sem_chuva)
    ausentes = base.loc[base["precipitacao_mm_ausente"], "data_hora"]
    assert set((ausentes + pd.Timedelta(hours=1)).dt.ceil("3h")) == set(passos_sem_chuva)


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


def test_ponto_grade_vazio_nao_vira_passo_inserido(tmp_path, bruto):
    editado = bruto.copy()
    editado["ponto_grade"] = editado["ponto_grade"].astype(object)
    editado.iloc[10, editado.columns.get_loc("ponto_grade")] = None
    copia = tmp_path / ARQUIVO_ERA5.name
    editado.reset_index().to_csv(copia, index=False, date_format="%Y-%m-%d %H:%M")

    grade = preparo.ler_bruto(copia)
    assert grade["passo_inserido"].sum() == sum(dados_ficticios.PASSOS_SEM_REGISTRO)
    assert not grade.loc[editado.index[10], "passo_inserido"]
