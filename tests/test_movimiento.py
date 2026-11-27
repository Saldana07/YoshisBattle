"""
Archivo:       tests/test_movimiento.py
Objetivo:      Verificar modelo/movimiento.py.
QUE VERIFICARA:
    - Desde una esquina (0, 0) solo hay 2 saltos: (1, 2) y (2, 1).
    - Desde el centro (3, 3) hay 8 saltos.
    - Ningun salto sale del tablero.
    - El orden de los saltos es el de SALTOS_CABALLO.
"""
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from yoshis_battle import constantes  # noqa: E402
from yoshis_battle.modelo import movimiento  # noqa: E402


class TestMovimiento(unittest.TestCase):
    def test_esquina_tiene_dos_saltos(self):
        self.assertEqual(movimiento.saltos_desde((0, 0)), [(1, 2), (2, 1)])

    def test_centro_tiene_ocho_saltos(self):
        self.assertEqual(len(movimiento.saltos_desde((3, 3))), 8)

    def test_ningun_salto_sale_del_tablero(self):
        n = constantes.TAMANO_TABLERO
        for fila in range(n):
            for columna in range(n):
                for f, c in movimiento.saltos_desde((fila, columna)):
                    self.assertTrue(0 <= f < n and 0 <= c < n)

    def test_el_orden_es_el_de_saltos_caballo(self):
        # Desde (3, 3) todos caben, asi que el orden debe coincidir con SALTOS_CABALLO.
        esperado = [(3 + df, 3 + dc) for df, dc in movimiento.SALTOS_CABALLO]
        self.assertEqual(movimiento.saltos_desde((3, 3)), esperado)

    def test_dentro_del_tablero(self):
        self.assertTrue(movimiento.dentro_del_tablero((0, 0)))
        self.assertTrue(movimiento.dentro_del_tablero((7, 7)))
        self.assertFalse(movimiento.dentro_del_tablero((-1, 0)))
        self.assertFalse(movimiento.dentro_del_tablero((0, 8)))


if __name__ == "__main__":
    unittest.main()
