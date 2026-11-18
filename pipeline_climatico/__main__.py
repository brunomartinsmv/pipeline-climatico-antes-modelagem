"""Executa as etapas do pipeline: `python -m pipeline_climatico <etapa>`."""

import argparse


def _gerar_dados() -> None:
    from pipeline_climatico import dados_ficticios

    dados_ficticios.salvar()


def _inventariar() -> None:
    from pipeline_climatico import inspecao

    inspecao.executar_inventario()


def _validar() -> None:
    from pipeline_climatico import inspecao

    inspecao.executar_validacao()


def _preparar() -> None:
    from pipeline_climatico import preparo

    preparo.executar()


def _graficos() -> None:
    from pipeline_climatico import graficos

    graficos.executar()


ETAPAS = {
    "inventariar": (_inventariar, "lista variáveis, tipos e ausências dos CSVs brutos"),
    "validar": (_validar, "confere colunas, datas duplicadas e ordem temporal"),
    "preparar": (_preparar, "gera data/processed/base_climatica_ficticia_processada.csv"),
    "graficos": (_graficos, "gera os painéis mensais em figures/"),
    "gerar-dados": (_gerar_dados, "recria os CSVs fictícios de data/raw/ a partir da semente"),
}
FLUXO = ["inventariar", "validar", "preparar", "graficos"]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="python -m pipeline_climatico", description=__doc__)
    sub = parser.add_subparsers(dest="etapa", required=True)
    sub.add_parser("tudo", help="executa inventariar, validar, preparar e graficos, nessa ordem")
    for nome, (_, ajuda) in ETAPAS.items():
        sub.add_parser(nome, help=ajuda)
    etapa = parser.parse_args(argv).etapa

    for nome in FLUXO if etapa == "tudo" else [etapa]:
        print(f"\n== {nome} ==")
        ETAPAS[nome][0]()


if __name__ == "__main__":
    main()
