"""
Archivo:       tests/test_estado.py
Objetivo:      Verificar modelo/estado.py (consultas del Estado e inmutabilidad).
"""
import dataclasses
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from yoshis_battle import constantes  # noqa: E402
from yoshis_battle.modelo.estado import Estado  # noqa: E402


def un_estado():
    return Estado(pos_verde=(0, 0), pos_rojo=(7, 7),
                  monedas=frozenset({((3, 3), 3), ((1, 1), 1)}))


class TestEstado(unittest.TestCase):
    def test_posicion_de(self):
        estado = un_estado()
        self.assertEqual(estado.posicion_de(constantes.VERDE), (0, 0))
        self.assertEqual(estado.posicion_de(constantes.ROJO), (7, 7))

    def test_valor_moneda_en(self):
        estado = un_estado()
        self.assertEqual(estado.valor_moneda_en((3, 3)), 3)
        self.assertEqual(estado.valor_moneda_en((1, 1)), 1)
        self.assertEqual(estado.valor_moneda_en((6, 6)), 0)

    def test_quedan_monedas(self):
        self.assertTrue(un_estado().quedan_monedas())
        self.assertFalse(dataclasses.replace(un_estado(), monedas=frozenset()).quedan_monedas())

    def test_rival(self):
        self.assertEqual(Estado.rival(constantes.VERDE), constantes.ROJO)
        self.assertEqual(Estado.rival(constantes.ROJO), constantes.VERDE)

    def test_jugador_desconocido(self):
        with self.assertRaises(ValueError):
            un_estado().posicion_de("azul")

    def test_es_inmutable_y_hasheable(self):
        estado = un_estado()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            estado.puntos_verde = 5
        self.assertEqual(hash(estado), hash(un_estado()))


if __name__ == "__main__":
    unittest.main()
