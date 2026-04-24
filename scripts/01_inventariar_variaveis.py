"""Inventaria variaveis dos arquivos CSV ficticios."""

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"


def inventariar_csv(caminho: Path) -> pd.DataFrame:
    df = pd.read_csv(caminho, nrows=5)
    return pd.DataFrame(
        {
            "arquivo": caminho.name,
            "variavel": df.columns,
            "tipo_inferido": [str(tipo) for tipo in df.dtypes],
        }
    )


def main() -> None:
    arquivos = sorted(RAW_DIR.glob("exemplo_*_ficticio.csv"))
    inventario = pd.concat([inventariar_csv(caminho) for caminho in arquivos], ignore_index=True)
    print(inventario.to_string(index=False))


if __name__ == "__main__":
    main()

