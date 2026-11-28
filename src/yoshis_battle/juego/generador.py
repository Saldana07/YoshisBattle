"""
Archivo:       src/yoshis_battle/juego/generador.py
Objetivo:      Construir el estado inicial aleatorio de una partida.
Responsabilidad:
    SI hace:
        - Poner las 4 monedas especiales en constantes.CASILLAS_ESPECIALES (siempre en
          el centro).
        - Poner constantes.CANTIDAD_MONEDAS_NORMALES monedas normales en casillas
          aleatorias, distintas entre si y distintas de las especiales.
        - Poner a los dos Yoshis en casillas aleatorias libres (sin moneda) y distintas.
        - Dejar puntos en 0 y el turno en constantes.JUGADOR_INICIAL (la maquina).
        - Recibir un generador aleatorio opcional para que las pruebas sean repetibles
          (misma semilla = mismo tablero).
    NO hace:
        - No valida movimientos ni juega: solo arma el primer Estado.
Importa de:    constantes, modelo/estado.py.
Lo importan:   controlador/partida.py, tests/test_generador.py.
Contrato:
    - generar_estado_inicial(rng: random.Random | None = None) -> Estado
Como funciona:
    1. Se listan las 64 casillas en orden fijo (fila por fila).
    2. Las monedas normales se sortean con rng.sample entre las casillas que NO son
       especiales; sample nunca repite, asi que quedan 9 casillas distintas.
    3. Los Yoshis se sortean con rng.sample entre las casillas que quedaron sin
       moneda; sample(..., 2) garantiza que no coinciden entre si.
    Como las listas de candidatas siempre se arman en el mismo orden, la misma
    semilla produce exactamente el mismo tablero.
"""
from __future__ import annotations

import random

from .. import constantes
from ..modelo.estado import Casilla, Estado


def _todas_las_casillas() -> list[Casilla]:
    """Las 64 casillas del tablero, fila por fila (orden fijo y repetible)."""
    n = constantes.TAMANO_TABLERO
    return [(fila, columna) for fila in range(n) for columna in range(n)]


def generar_estado_inicial(rng: random.Random | None = None) -> Estado:
    """Estado inicial aleatorio que cumple todas las restricciones del enunciado."""
    if rng is None:
        rng = random.Random()

    todas = _todas_las_casillas()
    especiales = set(constantes.CASILLAS_ESPECIALES)

    # Monedas normales: en cualquier casilla que no sea del centro.
    candidatas_normales = [casilla for casilla in todas if casilla not in especiales]
    normales = rng.sample(candidatas_normales, constantes.CANTIDAD_MONEDAS_NORMALES)

    # Yoshis: en casillas sin ninguna moneda, y distintas entre si.
    con_moneda = especiales | set(normales)
    libres = [casilla for casilla in todas if casilla not in con_moneda]
    pos_verde, pos_rojo = rng.sample(libres, 2)

    monedas = frozenset(
        [(casilla, constantes.VALOR_MONEDA_ESPECIAL)
         for casilla in constantes.CASILLAS_ESPECIALES]
        + [(casilla, constantes.VALOR_MONEDA_NORMAL) for casilla in normales]
    )
    return Estado(
        pos_verde=pos_verde,
        pos_rojo=pos_rojo,
        monedas=monedas,
        puntos_verde=0,
        puntos_rojo=0,
        turno=constantes.JUGADOR_INICIAL,
    )
