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

from yoshis_battle import constantes  # noqa: E402
from yoshis_battle.juego import reglas  # noqa: E402
from yoshis_battle.modelo.estado import Estado  # noqa: E402


def estado_de_prueba(**cambios):
    """Estado pequeno y conocido: verde en (0, 0), rojo en (7, 7), tres monedas."""
    base = dict(
        pos_verde=(0, 0),
        pos_rojo=(7, 7),
        monedas=frozenset({((1, 2), 3), ((2, 1), 1), ((5, 5), 1)}),
    )
    base.update(cambios)
    return Estado(**base)


class TestReglas(unittest.TestCase):
    def test_no_se_puede_saltar_sobre_el_rival(self):
        # Verde en (0, 0) salta a (1, 2) o (2, 1); el rojo esta en (1, 2).
        estado = estado_de_prueba(pos_rojo=(1, 2))
        self.assertEqual(reglas.movimientos_validos(estado), [(2, 1)])

    def test_movimientos_validos_por_jugador(self):
        estado = estado_de_prueba()
        self.assertEqual(reglas.movimientos_validos(estado, constantes.ROJO),
                         [(6, 5), (5, 6)])   # orden de SALTOS_CABALLO

    def test_tomar_moneda_especial_suma_tres(self):
        nuevo = reglas.aplicar_movimiento(estado_de_prueba(), (1, 2))
        self.assertEqual(nuevo.puntos_verde, 3)
        self.assertEqual(nuevo.pos_verde, (1, 2))
        self.assertNotIn(((1, 2), 3), nuevo.monedas)

    def test_tomar_moneda_normal_suma_uno(self):
        nuevo = reglas.aplicar_movimiento(estado_de_prueba(), (2, 1))
        self.assertEqual(nuevo.puntos_verde, 1)
        self.assertNotIn(((2, 1), 1), nuevo.monedas)

    def test_casilla_sin_moneda_no_suma(self):
        estado = estado_de_prueba(monedas=frozenset({((5, 5), 1)}))
        nuevo = reglas.aplicar_movimiento(estado, (1, 2))
        self.assertEqual(nuevo.puntos_verde, 0)
        self.assertEqual(len(nuevo.monedas), 1)

    def test_cambia_el_turno_y_suma_al_jugador_correcto(self):
        estado = estado_de_prueba(pos_rojo=(7, 7), turno=constantes.ROJO,
                                  monedas=frozenset({((5, 6), 3)}))
        nuevo = reglas.aplicar_movimiento(estado, (5, 6))
        self.assertEqual(nuevo.puntos_rojo, 3)
        self.assertEqual(nuevo.puntos_verde, 0)
        self.assertEqual(nuevo.turno, constantes.VERDE)

    def test_aplicar_no_modifica_el_original(self):
        estado = estado_de_prueba()
        copia = estado_de_prueba()
        reglas.aplicar_movimiento(estado, (1, 2))
        self.assertEqual(estado, copia)

    def test_destino_invalido_lanza_error(self):
        with self.assertRaises(ValueError):
            reglas.aplicar_movimiento(estado_de_prueba(), (4, 4))   # no es salto de caballo
        with self.assertRaises(ValueError):
            reglas.aplicar_movimiento(estado_de_prueba(pos_rojo=(1, 2)), (1, 2))  # casilla del rival

    def test_no_se_puede_jugar_con_la_partida_terminada(self):
        with self.assertRaises(ValueError):
            reglas.aplicar_movimiento(estado_de_prueba(monedas=frozenset()), (1, 2))

    def test_fin_y_ganador(self):
        en_juego = estado_de_prueba()
        self.assertFalse(reglas.es_terminal(en_juego))
        self.assertIsNone(reglas.ganador(en_juego))

        sin_monedas = frozenset()
        self.assertTrue(reglas.es_terminal(estado_de_prueba(monedas=sin_monedas)))
        self.assertEqual(reglas.ganador(estado_de_prueba(
            monedas=sin_monedas, puntos_verde=11, puntos_rojo=10)), constantes.VERDE)
        self.assertEqual(reglas.ganador(estado_de_prueba(
            monedas=sin_monedas, puntos_verde=8, puntos_rojo=13)), constantes.ROJO)
        self.assertEqual(reglas.ganador(estado_de_prueba(
            monedas=sin_monedas, puntos_verde=5, puntos_rojo=5)), constantes.EMPATE)

    def test_partida_completa_al_azar_siempre_suma_lo_que_habia(self):
        # Jugadas al azar hasta que no queden monedas: los puntos deben sumar 21 si el
        # estado de partida tiene las 13 monedas del enunciado.
        import random
        rng = random.Random(7)
        especiales = [(c, 3) for c in constantes.CASILLAS_ESPECIALES]
        normales = [((0, 1), 1), ((0, 5), 1), ((1, 6), 1), ((2, 2), 1), ((2, 7), 1),
                    ((5, 0), 1), ((5, 4), 1), ((6, 3), 1), ((7, 6), 1)]
        estado = Estado(pos_verde=(0, 0), pos_rojo=(7, 7),
                        monedas=frozenset(especiales + normales))
        total = sum(v for _, v in estado.monedas)
        self.assertEqual(total, 21)
        for _ in range(5000):
            if reglas.es_terminal(estado):
                break
            estado = reglas.aplicar_movimiento(
                estado, rng.choice(reglas.movimientos_validos(estado)))
        self.assertTrue(reglas.es_terminal(estado))
        self.assertEqual(estado.puntos_verde + estado.puntos_rojo, 21)
        self.assertIn(reglas.ganador(estado), (constantes.VERDE, constantes.ROJO))


if __name__ == "__main__":
    unittest.main()
