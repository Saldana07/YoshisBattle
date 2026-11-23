"""
Archivo:       tests/test_generador.py
Objetivo:      Verificar juego/generador.py con muchas semillas distintas.
QUE VERIFICARA:
    - Las 4 monedas especiales estan siempre en CASILLAS_ESPECIALES con valor 3.
    - Hay exactamente 9 monedas normales, de valor 1, en casillas distintas entre si y
      distintas de las especiales.
    - Los Yoshis estan en casillas distintas y sin moneda.
    - Puntos en 0 y turno de VERDE.
    - Con la misma semilla se obtiene el mismo estado.
"""
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from yoshis_battle.juego import generador  # noqa: E402,F401


class TestGenerador(unittest.TestCase):
    @unittest.skip("PENDIENTE")
    def test_monedas_especiales_en_el_centro(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_nueve_monedas_normales_sin_repetir(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_yoshis_en_casillas_libres_y_distintas(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_empieza_la_maquina_con_cero_puntos(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_misma_semilla_mismo_estado(self):
        pass


if __name__ == "__main__":
    unittest.main()
