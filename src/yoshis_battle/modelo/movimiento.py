"""
Archivo:       src/yoshis_battle/modelo/movimiento.py
Objetivo:      Definir el movimiento de caballo de ajedrez que usan los dos Yoshis.
Responsabilidad:
    SI hace:
        - Definir los ocho desplazamientos posibles del caballo, en un orden fijo.
        - Decir si una casilla esta dentro del tablero.
        - Listar las casillas a las que se llega con un salto desde una casilla dada,
          sin salirse del tablero.
    NO hace:
        - No sabe donde esta el otro Yoshi ni que casillas estan ocupadas: descartar la
          casilla del rival es responsabilidad de juego/reglas.py.
Importa de:    constantes (TAMANO_TABLERO), modelo/estado.py (Casilla).
Lo importan:   juego/reglas.py, juego/generador.py (opcional), ia/heuristica.py
               (distancias en saltos de caballo).
Contrato previsto:
    - SALTOS_CABALLO: tupla de 8 desplazamientos (df, dc).
    - dentro_del_tablero(casilla) -> bool
    - saltos_desde(casilla) -> list[Casilla]   (en el orden de SALTOS_CABALLO)
Decisiones de equipo:
    - Orden de los saltos: el de SALTOS_CABALLO (sentido horario empezando arriba a la
      derecha). Ese orden es el que usa minimax para desempatar.
"""
from __future__ import annotations

from .. import constantes
from .estado import Casilla

SALTOS_CABALLO = (
    (-2, 1), (-1, 2), (1, 2), (2, 1),
    (2, -1), (1, -2), (-1, -2), (-2, -1),
)


def dentro_del_tablero(casilla: Casilla) -> bool:
    """Verdadero si `casilla` esta entre (0, 0) y (TAMANO_TABLERO-1, TAMANO_TABLERO-1)."""
    fila, columna = casilla
    return (0 <= fila < constantes.TAMANO_TABLERO
            and 0 <= columna < constantes.TAMANO_TABLERO)


def saltos_desde(casilla: Casilla) -> list[Casilla]:
    """Casillas alcanzables con un salto de caballo desde `casilla`, dentro del tablero."""
    fila, columna = casilla
    destinos = []
    for df, dc in SALTOS_CABALLO:
        destino = (fila + df, columna + dc)
        if dentro_del_tablero(destino):
            destinos.append(destino)
    return destinos
