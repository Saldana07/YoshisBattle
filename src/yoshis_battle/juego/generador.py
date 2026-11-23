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
Contrato previsto:
    - generar_estado_inicial(rng: random.Random | None = None) -> Estado
"""
from __future__ import annotations

import random

from .. import constantes  # noqa: F401  (se usa al implementar)
from ..modelo.estado import Estado


def generar_estado_inicial(rng: random.Random | None = None) -> Estado:
    """Estado inicial aleatorio que cumple todas las restricciones del enunciado."""
    raise NotImplementedError("PENDIENTE: juego/generador.py generar_estado_inicial")
