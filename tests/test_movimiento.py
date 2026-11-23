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

from yoshis_battle.modelo import movimiento  # noqa: E402,F401


class TestMovimiento(unittest.TestCase):
    @unittest.skip("PENDIENTE")
    def test_esquina_tiene_dos_saltos(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_centro_tiene_ocho_saltos(self):
        pass

    @unittest.skip("PENDIENTE")
    def test_ningun_salto_sale_del_tablero(self):
        pass


if __name__ == "__main__":
    unittest.main()
