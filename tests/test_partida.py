"""
Archivo:       tests/test_partida.py
Objetivo:      Verificar controlador/partida.py jugando partidas completas sin GUI.
QUE VERIFICARA:
    - La primera jugada siempre es de la maquina.
    - Los turnos se alternan maquina / humano.
    - Una partida completa (humano que juega al azar) siempre termina, con la suma de
      puntos igual a 4 x 3 + 9 x 1 = 21, y tiene ganador.
    - jugar_humano con un destino invalido lanza ValueError y no cambia el estado.
"""
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from yoshis_battle.controlador import partida  # noqa: E402,F401


class TestPartida(unittest.TestCase):
    @unittest.skip("PENDIENTE")
    def test_empieza_la_maquina(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_turnos_alternados(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_partida_completa_reparte_21_puntos(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_jugada_humana_invalida(self):
        pass


if __name__ == "__main__":
    unittest.main()
