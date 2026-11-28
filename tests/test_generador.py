"""
Archivo:       tests/test_generador.py
Objetivo:      Verificar juego/generador.py con muchas semillas distintas.
QUE VERIFICA:
    - Las 4 monedas especiales estan siempre en CASILLAS_ESPECIALES con valor 3.
    - Hay exactamente 9 monedas normales, de valor 1, en casillas distintas entre si y
      distintas de las especiales.
    - Los Yoshis estan en casillas distintas y sin moneda.
    - Puntos en 0 y turno de VERDE.
    - Con la misma semilla se obtiene el mismo estado.
"""
import random
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from yoshis_battle import constantes  # noqa: E402
from yoshis_battle.juego import generador  # noqa: E402
from yoshis_battle.modelo.movimiento import dentro_del_tablero  # noqa: E402

SEMILLAS = range(300)


def _estados():
    """Un estado inicial por cada semilla de prueba."""
    for semilla in SEMILLAS:
        yield semilla, generador.generar_estado_inicial(random.Random(semilla))


class TestGenerador(unittest.TestCase):
    def test_monedas_especiales_en_el_centro(self):
        for semilla, estado in _estados():
            with self.subTest(semilla=semilla):
                especiales = {casilla for casilla, valor in estado.monedas
                              if valor == constantes.VALOR_MONEDA_ESPECIAL}
                self.assertEqual(especiales, set(constantes.CASILLAS_ESPECIALES))

    def test_nueve_monedas_normales_sin_repetir(self):
        for semilla, estado in _estados():
            with self.subTest(semilla=semilla):
                normales = [casilla for casilla, valor in estado.monedas
                            if valor == constantes.VALOR_MONEDA_NORMAL]
                self.assertEqual(len(normales), constantes.CANTIDAD_MONEDAS_NORMALES)
                self.assertEqual(len(set(normales)), len(normales))
                self.assertTrue(set(normales).isdisjoint(constantes.CASILLAS_ESPECIALES))
                self.assertTrue(all(dentro_del_tablero(c) for c in normales))
                # Ninguna casilla tiene dos monedas y solo hay valores 1 y 3.
                casillas = [casilla for casilla, _ in estado.monedas]
                self.assertEqual(len(casillas), len(set(casillas)))
                self.assertEqual(
                    len(estado.monedas),
                    len(constantes.CASILLAS_ESPECIALES)
                    + constantes.CANTIDAD_MONEDAS_NORMALES,
                )

    def test_yoshis_en_casillas_libres_y_distintas(self):
        for semilla, estado in _estados():
            with self.subTest(semilla=semilla):
                self.assertNotEqual(estado.pos_verde, estado.pos_rojo)
                self.assertTrue(dentro_del_tablero(estado.pos_verde))
                self.assertTrue(dentro_del_tablero(estado.pos_rojo))
                self.assertEqual(estado.valor_moneda_en(estado.pos_verde), 0)
                self.assertEqual(estado.valor_moneda_en(estado.pos_rojo), 0)

    def test_empieza_la_maquina_con_cero_puntos(self):
        for semilla, estado in _estados():
            with self.subTest(semilla=semilla):
                self.assertEqual(estado.puntos_verde, 0)
                self.assertEqual(estado.puntos_rojo, 0)
                self.assertEqual(estado.turno, constantes.VERDE)

    def test_misma_semilla_mismo_estado(self):
        for semilla in (0, 7, 2026):
            with self.subTest(semilla=semilla):
                a = generador.generar_estado_inicial(random.Random(semilla))
                b = generador.generar_estado_inicial(random.Random(semilla))
                self.assertEqual(a, b)

    def test_es_aleatorio(self):
        tableros = {generador.generar_estado_inicial(random.Random(s)) for s in SEMILLAS}
        self.assertGreater(len(tableros), 1)

    def test_sin_rng_tambien_funciona(self):
        estado = generador.generar_estado_inicial()
        self.assertEqual(
            len(estado.monedas),
            len(constantes.CASILLAS_ESPECIALES) + constantes.CANTIDAD_MONEDAS_NORMALES,
        )


if __name__ == "__main__":
    unittest.main()
