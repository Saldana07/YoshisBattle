"""
Archivo:       src/yoshis_battle/controlador/partida.py
Objetivo:      Llevar una partida completa: crear el tablero inicial, alternar turnos
               entre la maquina y el humano, y avisar cuando termina y quien gano.
Responsabilidad:
    SI hace:
        - Crear el estado inicial con juego/generador.py para el nivel elegido.
        - Garantizar que la maquina (verde) hace la primera jugada.
        - Pedirle la jugada a ia/minimax.py en el turno de la maquina.
        - Validar y aplicar la jugada del humano en su turno.
        - Exponer el estado actual, los puntos, de quien es el turno, si termino y el
          ganador, para que la GUI los muestre.
        - Guardar la ultima Decision de la IA (nodos, tiempo) para mostrarla o para
          las pruebas del informe.
    NO hace:
        - No dibuja nada ni lee eventos de pygame: eso es gui/.
        - No implementa reglas ni busqueda: las delega.
Importa de:    constantes, modelo/estado.py, juego/generador.py, juego/reglas.py,
               ia/minimax.py.
Lo importan:   gui/ventana_juego.py, main.py, tests/test_partida.py.
Contrato previsto:
    - Partida(nivel, rng=None)
    - Partida.estado -> Estado
    - Partida.turno_de_maquina() -> bool
    - Partida.jugar_maquina() -> Decision
          Solo valido si es turno de la maquina y la partida no ha terminado.
    - Partida.movimientos_humano() -> list[Casilla]
    - Partida.jugar_humano(destino) -> None
          Lanza ValueError si `destino` no es valido.
    - Partida.terminada() -> bool
    - Partida.ganador() -> str | None
    - Partida.ultima_decision -> Decision | None
"""
from __future__ import annotations

import random

from .. import constantes  # noqa: F401  (se usa al implementar)
from ..ia.minimax import Decision
from ..modelo.estado import Casilla, Estado


class Partida:
    def __init__(self, nivel: str, rng: random.Random | None = None) -> None:
        self.nivel = nivel
        self.estado: Estado
        self.ultima_decision: Decision | None = None
        raise NotImplementedError("PENDIENTE: controlador/partida.py Partida.__init__")

    def turno_de_maquina(self) -> bool:
        raise NotImplementedError("PENDIENTE: controlador/partida.py turno_de_maquina")

    def jugar_maquina(self) -> Decision:
        raise NotImplementedError("PENDIENTE: controlador/partida.py jugar_maquina")

    def movimientos_humano(self) -> list[Casilla]:
        raise NotImplementedError("PENDIENTE: controlador/partida.py movimientos_humano")

    def jugar_humano(self, destino: Casilla) -> None:
        raise NotImplementedError("PENDIENTE: controlador/partida.py jugar_humano")

    def terminada(self) -> bool:
        raise NotImplementedError("PENDIENTE: controlador/partida.py terminada")

    def ganador(self) -> str | None:
        raise NotImplementedError("PENDIENTE: controlador/partida.py ganador")
