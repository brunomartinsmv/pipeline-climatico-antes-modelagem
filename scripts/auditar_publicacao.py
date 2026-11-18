#!/usr/bin/env python3
"""Confere os arquivos que o Git incluiria na cópia pública, sem alterá-los."""

import json
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
BINARIOS_LIBERADOS = {
    "figures/painel_mensal_variaveis_processadas.png",
    "figures/painel_mensal_falhas_inmet.png",
}
EXTENSOES_BINARIAS = {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".nc", ".grib", ".xlsx", ".zip"}
LIMITE_BYTES = 2_000_000


def auditar() -> tuple[list[str], list[str]]:
    resultado = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=RAIZ,
        check=True,
        capture_output=True,
    )
    caminhos = sorted(set(resultado.stdout.decode().split("\0")) - {""})
    falhas = []
    for nome in caminhos:
        caminho = RAIZ / nome
        if not caminho.exists():
            continue
        if caminho.is_symlink():
            falhas.append(f"{nome}: link simbólico exige revisão")
            continue
        if caminho.suffix.lower() in EXTENSOES_BINARIAS and nome not in BINARIOS_LIBERADOS:
            falhas.append(f"{nome}: binário sem liberação para a cópia pública")
        if caminho.stat().st_size > LIMITE_BYTES:
            falhas.append(f"{nome}: maior que {LIMITE_BYTES // 1_000_000} MB")
        if caminho.suffix == ".ipynb":
            notebook = json.loads(caminho.read_text(encoding="utf-8"))
            for celula in notebook["cells"]:
                if celula.get("outputs") or celula.get("execution_count") is not None or celula.get("attachments"):
                    falhas.append(f"{nome}: saídas ou anexos embutidos")
                    break
    return caminhos, falhas


if __name__ == "__main__":
    caminhos, falhas = auditar()
    for falha in falhas:
        print(falha)
    print(f"{len(caminhos)} arquivos conferidos; {len(falhas)} impedimentos.")
    raise SystemExit(bool(falhas))
