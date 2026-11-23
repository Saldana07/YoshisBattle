"""
Archivo:       src/yoshis_battle/ia/heuristica.py
Objetivo:      Definir la funcion de utilidad heuristica con la que minimax evalua los
               estados donde corta la busqueda (decisiones imperfectas). Es la funcion
               que el informe debe definir y explicar.
Responsabilidad:
    SI hace:
        - Evaluar cualquier Estado desde el punto de vista de la maquina (Yoshi verde,
          MAX): valores altos = bueno para verde, bajos = bueno para rojo.
        - Dar un valor exacto y muy grande a los estados terminales:
          +UTILIDAD_VICTORIA si gana verde, -UTILIDAD_VICTORIA si gana rojo, 0 si empate.
        - Calcular la distancia en saltos de caballo entre dos casillas (BFS sobre el
          tablero 8 x 8, idealmente precalculada una sola vez).
    NO hace:
        - No recorre el arbol de juego: eso es ia/minimax.py.
        - No modifica el Estado.
Importa de:    constantes, modelo/estado.py, modelo/movimiento.py, juego/reglas.py.
Lo importan:   ia/minimax.py, tests/test_heuristica.py.
Contrato previsto:
    - UTILIDAD_VICTORIA: numero mayor que cualquier valor heuristico no terminal.
    - distancia_caballo(origen, destino) -> int
    - evaluar(estado) -> float
PENDIENTE (decision de equipo, va al informe):
    - Terminos y pesos de la heuristica. Propuesta inicial para discutir:
        h(s) = w1 * (puntos_verde - puntos_rojo)
             + w2 * sum(valor / (1 + d_verde)) - w2 * sum(valor / (1 + d_rojo))
             + w3 * (movilidad_verde - movilidad_rojo)
      donde d_x es la distancia en saltos de caballo del Yoshi x a cada moneda.
    - Ajustar los pesos con partidas de prueba y dejar los resultados en docs/informe/.
"""
from __future__ import annotations

from .. import constantes  # noqa: F401  (se usa al implementar)
from ..modelo.estado import Casilla, Estado

UTILIDAD_VICTORIA = 1_000.0


def distancia_caballo(origen: Casilla, destino: Casilla) -> int:
    """Minimo numero de saltos de caballo para ir de `origen` a `destino`."""
    raise NotImplementedError("PENDIENTE: ia/heuristica.py distancia_caballo")


def evaluar(estado: Estado) -> float:
    """Valor heuristico de `estado` para la maquina (verde)."""
    raise NotImplementedError("PENDIENTE: ia/heuristica.py evaluar")
