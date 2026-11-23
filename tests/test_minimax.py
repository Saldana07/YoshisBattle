"""
Archivo:       tests/test_minimax.py
Objetivo:      Verificar ia/minimax.py.
QUE VERIFICARA:
    - La jugada elegida siempre es una de reglas.movimientos_validos.
    - Si hay una moneda especial a un salto y nada mejor, la maquina la toma.
    - Con y sin poda alfa-beta se obtiene el mismo valor (alfa-beta expande menos nodos).
    - decidir_por_nivel usa profundidad 2, 4 y 6.
    - En experto, una jugada tarda menos de unos segundos (limite a acordar).
"""
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from yoshis_battle.ia import minimax  # noqa: E402,F401


class TestMinimax(unittest.TestCase):
    @unittest.skip("PENDIENTE")
    def test_jugada_es_valida(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_toma_moneda_especial_cercana(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_alfa_beta_no_cambia_el_valor(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_profundidad_por_nivel(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_tiempo_en_experto(self):
        pass


if __name__ == "__main__":
    unittest.main()
