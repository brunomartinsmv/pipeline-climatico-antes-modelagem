import numpy as np
import pandas as pd
import pytest

from pipeline_climatico import ARQUIVO_ERA5, ARQUIVO_INMET, dados_ficticios, indice_horario_anual, inspecao, preparo


@pytest.fixture(scope="module")
def base():
    return preparo.preparar_base()


def test_csvs_brutos_coincidem_com_o_gerador():
    inmet, era5 = dados_ficticios.gerar()
    assert ARQUIVO_INMET.read_text(encoding="utf-8") == dados_ficticios.para_csv(inmet)
    assert ARQUIVO_ERA5.read_text(encoding="utf-8") == dados_ficticios.para_csv(era5)


@pytest.mark.parametrize("arquivo", [ARQUIVO_INMET, ARQUIVO_ERA5])
def test_estrutura_dos_brutos_e_valida(arquivo):
    assert inspecao.validar(arquivo)["colunas_extras"] == []


def test_validacao_acusa_datas_duplicadas(tmp_path):
    copia = tmp_path / ARQUIVO_INMET.name
    linhas = ARQUIVO_INMET.read_text(encoding="utf-8").splitlines()
    copia.write_text("\n".join(linhas + [linhas[1]]) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="duplicadas"):
        inspecao.validar(copia)


def test_base_cobre_todas_as_horas_do_ano(base):
    assert base["data_hora"].tolist() == indice_horario_anual().tolist()
    assert base.columns.tolist() == preparo.COLUNAS_BASE


def test_conversoes_de_unidade_do_era5(base):
    bruto = pd.read_csv(ARQUIVO_ERA5, parse_dates=["data_hora"]).set_index("data_hora")
    primeira = bruto.index[0]
    linha = base.set_index("data_hora").loc[primeira]
    assert linha["temperatura_era5_c"] == pytest.approx(bruto.loc[primeira, "temperatura_2m_k"] - 273.15)


def test_precipitacao_era5_conserva_o_total(base):
    bruto = pd.read_csv(ARQUIVO_ERA5)
    assert base["precipitacao_era5_mm"].sum() == pytest.approx(bruto["precipitacao_total_m"].sum() * 1000)


def test_precipitacao_inmet_nao_e_inventada(base):
    bruto = pd.read_csv(ARQUIVO_INMET)
    ausentes = len(base) - len(bruto) + bruto["precipitacao_mm"].isna().sum()
    assert base["precipitacao_inmet_mm_ausente"].sum() == ausentes
    assert base["precipitacao_inmet_mm"].isna().sum() == ausentes
    assert base["precipitacao_inmet_mm"].sum() == pytest.approx(bruto["precipitacao_mm"].sum())


def test_lacuna_longa_de_temperatura_fica_inteira_ausente(base):
    ausente = base["temperatura_inmet_c"].isna()
    assert ausente.sum() == 10
    assert not (ausente & base["temperatura_inmet_c_imputado"]).any()


def test_preencher_lacunas_curtas_respeita_o_limite():
    indice = pd.date_range("2024-01-01", periods=12, freq="h")
    valores = [0, np.nan, np.nan, 3, 4, np.nan, np.nan, np.nan, np.nan, 9, 10, np.nan]
    tratada, imputado = preparo.preencher_lacunas_curtas(pd.Series(valores, index=indice, dtype=float), max_horas=3)
    assert tratada.iloc[1:3].tolist() == [1, 2]
    assert tratada.iloc[5:9].isna().all()
    assert np.isnan(tratada.iloc[11])
    assert imputado.tolist() == [False, True, True] + [False] * 9


def test_flags_de_imputacao_batem_com_os_valores(base):
    bruto = pd.read_csv(ARQUIVO_INMET, parse_dates=["data_hora"]).set_index("data_hora")
    bruto = bruto.reindex(indice_horario_anual())
    tratada = base.set_index("data_hora")
    esperado = bruto["temperatura_c"].isna() & tratada["temperatura_inmet_c"].notna()
    assert (tratada["temperatura_inmet_c_imputado"] == esperado).all()
