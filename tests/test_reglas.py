"""
Archivo:       tests/test_reglas.py
Objetivo:      Verificar juego/reglas.py.
QUE VERIFICARA:
    - movimientos_validos nunca incluye la casilla del rival.
    - aplicar_movimiento suma 3 al tomar una especial y 1 al tomar una normal, quita
      la moneda del tablero y cambia el turno.
    - aplicar_movimiento no modifica el estado original.
    - aplicar_movimiento lanza ValueError con un destino invalido.
    - es_terminal es verdadero solo cuando no quedan monedas.
    - ganador retorna VERDE, ROJO o EMPATE segun los puntos, y None si no ha terminado.
"""
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from yoshis_battle.juego import reglas  # noqa: E402,F401


class TestReglas(unittest.TestCase):
    @unittest.skip("PENDIENTE")
    def test_no_se_puede_saltar_sobre_el_rival(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_tomar_moneda_especial_suma_tres(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_tomar_moneda_normal_suma_uno(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_aplicar_no_modifica_el_original(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_destino_invalido_lanza_error(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_fin_y_ganador(self):
        pass


if __name__ == "__main__":
    unittest.main()
