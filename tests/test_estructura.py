"""
Archivo:       tests/test_estructura.py
Objetivo:      Verificar que el esqueleto se puede importar completo y que las constantes
               del enunciado estan bien. Esta prueba ya corre; las demas estan
               marcadas como pendientes hasta que se implemente cada modulo.
"""
import importlib
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from yoshis_battle import constantes  # noqa: E402

MODULOS = [
    "yoshis_battle.constantes",
    "yoshis_battle.modelo.estado",
    "yoshis_battle.modelo.movimiento",
    "yoshis_battle.juego.generador",
    "yoshis_battle.juego.reglas",
    "yoshis_battle.ia.heuristica",
    "yoshis_battle.ia.minimax",
    "yoshis_battle.controlador.partida",
    "yoshis_battle.main",
]


class TestEstructura(unittest.TestCase):
    def test_modulos_sin_gui_se_importan(self):
        for nombre in MODULOS:
            with self.subTest(modulo=nombre):
                importlib.import_module(nombre)

    def test_constantes_del_enunciado(self):
        self.assertEqual(constantes.TAMANO_TABLERO, 8)
        self.assertEqual(len(constantes.CASILLAS_ESPECIALES), 4)
        self.assertEqual(constantes.VALOR_MONEDA_ESPECIAL, 3)
        self.assertEqual(constantes.VALOR_MONEDA_NORMAL, 1)
        self.assertEqual(constantes.CANTIDAD_MONEDAS_NORMALES, 9)
        self.assertEqual(constantes.JUGADOR_INICIAL, constantes.VERDE)
        self.assertEqual(sorted(constantes.PROFUNDIDAD_POR_NIVEL.values()), [2, 4, 6])


if __name__ == "__main__":
    unittest.main()
