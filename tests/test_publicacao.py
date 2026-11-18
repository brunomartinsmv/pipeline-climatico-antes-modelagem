import importlib.util

from pipeline_climatico import RAIZ


def test_copia_publica_sem_binarios_ou_saidas_de_notebook():
    spec = importlib.util.spec_from_file_location("auditar_publicacao", RAIZ / "scripts" / "auditar_publicacao.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    _, falhas = modulo.auditar()
    assert falhas == []
