"""
Archivo:       src/yoshis_battle/ia/minimax.py
Objetivo:      Elegir la jugada de la maquina con un arbol minimax de decisiones
               imperfectas: se expande hasta la profundidad limite del nivel y alli se
               evalua con la heuristica.
Responsabilidad:
    SI hace:
        - Recorrer el arbol de juego alternando MAX (verde, maquina) y MIN (rojo, humano)
          hasta la profundidad limite o hasta un estado terminal.
        - Usar ia/heuristica.evaluar en las hojas.
        - Aplicar poda alfa-beta para que el nivel experto (profundidad 6) responda
          en un tiempo razonable.
        - Retornar, ademas de la jugada, datos para el informe: valor, nodos
          expandidos y tiempo.
    NO hace:
        - No conoce la interfaz ni el flujo de la partida.
        - No define la heuristica.
Importa de:    constantes, modelo/estado.py, juego/reglas.py, ia/heuristica.py.
Lo importan:   controlador/partida.py, tests/test_minimax.py.
Contrato previsto:
    - Decision: dataclass con movimiento (Casilla), valor (float),
      nodos_expandidos (int) y segundos (float).
    - decidir(estado, profundidad) -> Decision
          `estado.turno` debe ser constantes.VERDE.
    - decidir_por_nivel(estado, nivel) -> Decision
          Traduce el nivel con constantes.PROFUNDIDAD_POR_NIVEL y llama a decidir.
Decisiones de equipo:
    - Desempate entre jugadas con el mismo valor: la primera en el orden de
      juego/reglas.movimientos_validos.
PENDIENTE:
    - Ordenar las jugadas antes de expandir (por ejemplo, primero las que toman
      moneda) para podar mas.
"""
from __future__ import annotations

from dataclasses import dataclass

from .. import constantes  # noqa: F401  (se usa al implementar)
from ..modelo.estado import Casilla, Estado


@dataclass(frozen=True)
class Decision:
    movimiento: Casilla
    valor: float
    nodos_expandidos: int
    segundos: float


def decidir(estado: Estado, profundidad: int) -> Decision:
    """Mejor jugada para la maquina con minimax + alfa-beta hasta `profundidad`."""
    raise NotImplementedError("PENDIENTE: ia/minimax.py decidir")


def decidir_por_nivel(estado: Estado, nivel: str) -> Decision:
    """Como `decidir`, usando la profundidad del nivel elegido por el usuario."""
    raise NotImplementedError("PENDIENTE: ia/minimax.py decidir_por_nivel")
