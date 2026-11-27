"""
Archivo:       src/yoshis_battle/juego/reglas.py
Objetivo:      Aplicar las reglas de Yoshi's Battle sobre un Estado: que jugadas son
               validas, que pasa al hacer una jugada y cuando termina la partida.
Responsabilidad:
    SI hace:
        - Listar las jugadas validas del jugador de turno: saltos de caballo dentro del
          tablero que no caen en la casilla del otro Yoshi.
        - Aplicar una jugada: mover al Yoshi, si hay moneda en el destino sumarla a sus
          puntos y quitarla del tablero, y pasar el turno al rival. Retorna un Estado
          nuevo (el original no cambia).
        - Decir si la partida termino (no quedan monedas) y quien gano.
    NO hace:
        - No decide que jugada conviene: eso es ia/.
        - No lleva el historial ni el flujo de turnos de la partida: eso es
          controlador/partida.py.
Importa de:    constantes, modelo/estado.py, modelo/movimiento.py.
Lo importan:   ia/minimax.py, ia/heuristica.py, controlador/partida.py, gui/ (para
               resaltar las casillas validas del humano).
Contrato previsto:
    - movimientos_validos(estado, jugador=None) -> list[Casilla]
          jugador por defecto = estado.turno. Orden = el de movimiento.SALTOS_CABALLO.
    - aplicar_movimiento(estado, destino) -> Estado
          Lanza ValueError si `destino` no es una jugada valida del jugador de turno.
    - es_terminal(estado) -> bool
    - ganador(estado) -> str | None
          constantes.VERDE, constantes.ROJO o constantes.EMPATE; None si no ha terminado.
Notas:
    - aplicar_movimiento tambien lanza ValueError si la partida ya termino.
    - En un tablero 8 x 8 un caballo siempre tiene al menos 2 saltos y el rival solo
      puede bloquear uno, asi que nunca hay un jugador sin movimientos.
"""
from __future__ import annotations

from dataclasses import replace

from .. import constantes
from ..modelo.estado import Casilla, Estado
from ..modelo.movimiento import saltos_desde


def movimientos_validos(estado: Estado, jugador: str | None = None) -> list[Casilla]:
    """Destinos validos para `jugador` (por defecto el de turno)."""
    if jugador is None:
        jugador = estado.turno
    casilla_rival = estado.posicion_de(Estado.rival(jugador))
    return [destino for destino in saltos_desde(estado.posicion_de(jugador))
            if destino != casilla_rival]


def aplicar_movimiento(estado: Estado, destino: Casilla) -> Estado:
    """Estado que resulta de que el jugador de turno salte a `destino`."""
    if es_terminal(estado):
        raise ValueError("La partida ya termino: no quedan monedas.")
    if destino not in movimientos_validos(estado):
        raise ValueError(f"Jugada invalida para {estado.turno}: {destino}")

    ganados = estado.valor_moneda_en(destino)
    monedas = frozenset(par for par in estado.monedas if par[0] != destino)
    rival = Estado.rival(estado.turno)

    if estado.turno == constantes.VERDE:
        return replace(estado, pos_verde=destino, monedas=monedas,
                       puntos_verde=estado.puntos_verde + ganados, turno=rival)
    return replace(estado, pos_rojo=destino, monedas=monedas,
                   puntos_rojo=estado.puntos_rojo + ganados, turno=rival)


def es_terminal(estado: Estado) -> bool:
    """Verdadero si ya no quedan monedas en el tablero."""
    return not estado.quedan_monedas()


def ganador(estado: Estado) -> str | None:
    """VERDE, ROJO o EMPATE si la partida termino; None si no."""
    if not es_terminal(estado):
        return None
    if estado.puntos_verde > estado.puntos_rojo:
        return constantes.VERDE
    if estado.puntos_rojo > estado.puntos_verde:
        return constantes.ROJO
    return constantes.EMPATE
