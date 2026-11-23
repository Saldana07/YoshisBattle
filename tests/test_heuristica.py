"""
Archivo:       tests/test_heuristica.py
Objetivo:      Verificar ia/heuristica.py.
QUE VERIFICARA:
    - distancia_caballo: 0 a la misma casilla, 1 a un salto, 6 de (0,0) a (7,7).
    - evaluar da +UTILIDAD_VICTORIA / -UTILIDAD_VICTORIA / 0 en estados terminales.
    - Un estado no terminal nunca alcanza UTILIDAD_VICTORIA en valor absoluto.
    - Con todo igual, tener mas puntos que el rival da un valor mayor.
    - Con todo igual, estar mas cerca de una moneda especial da un valor mayor.
"""
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from yoshis_battle.ia import heuristica  # noqa: E402,F401


class TestHeuristica(unittest.TestCase):
    @unittest.skip("PENDIENTE")
    def test_distancia_caballo(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_valores_terminales(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_no_terminal_acotado(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_mas_puntos_es_mejor(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_mas_cerca_de_especial_es_mejor(self):
        pass


if __name__ == "__main__":
    unittest.main()
