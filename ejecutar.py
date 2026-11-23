"""Lanzador de Yoshi's Battle: permite arrancar el juego desde la raiz del repositorio.

    python ejecutar.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from yoshis_battle.main import punto_de_entrada  # noqa: E402

if __name__ == "__main__":
    sys.exit(punto_de_entrada())
