"""
Archivo:       src/yoshis_battle/modelo/estado.py
Objetivo:      Representar un estado del juego: donde esta cada Yoshi, que monedas quedan
               en el tablero, cuantos puntos lleva cada jugador y a quien le toca mover.
Responsabilidad:
    SI hace:
        - Definir los componentes del estado:
            pos_verde, pos_rojo: casilla (fila, columna) de cada Yoshi.
            monedas: conjunto inmutable de pares (casilla, valor) de las monedas que
                     siguen en el tablero (valor 3 = especial, 1 = normal).
            puntos_verde, puntos_rojo: puntos acumulados de cada jugador.
            turno: constantes.VERDE o constantes.ROJO.
        - Ser inmutable y hasheable: aplicar un movimiento produce un Estado nuevo, asi
          minimax puede explorar ramas sin deshacer cambios.
        - Ofrecer consultas simples sobre el propio estado (posicion de un jugador, valor
          de la moneda en una casilla, si quedan monedas).
    NO hace:
        - No decide que movimientos son validos ni los aplica: eso es juego/reglas.py.
        - No genera el estado inicial aleatorio: eso es juego/generador.py.
Importa de:    constantes (VERDE, ROJO).
Lo importan:   juego/, ia/, controlador/ y gui/ (para dibujar el tablero).
Contrato previsto:
    - Casilla: alias de tuple[int, int] = (fila, columna).
    - Estado: dataclass congelada con los seis campos de arriba.
    - Estado.posicion_de(jugador) -> Casilla
    - Estado.valor_moneda_en(casilla) -> int   (0 si no hay moneda)
    - Estado.quedan_monedas() -> bool
    - Estado.rival(jugador) -> str             (el otro jugador)
PENDIENTE:
    - Confirmar si frozenset de pares (casilla, valor) es suficiente o conviene otra
      estructura (por ejemplo dos frozenset separados: especiales y normales).
"""
from __future__ import annotations

from dataclasses import dataclass

from .. import constantes

Casilla = tuple[int, int]


@dataclass(frozen=True)
class Estado:
    pos_verde: Casilla
    pos_rojo: Casilla
    monedas: frozenset[tuple[Casilla, int]]
    puntos_verde: int = 0
    puntos_rojo: int = 0
    turno: str = constantes.JUGADOR_INICIAL

    def posicion_de(self, jugador: str) -> Casilla:
        """Casilla donde esta el Yoshi de `jugador`."""
        if jugador == constantes.VERDE:
            return self.pos_verde
        if jugador == constantes.ROJO:
            return self.pos_rojo
        raise ValueError(f"Jugador desconocido: {jugador!r}")

    def valor_moneda_en(self, casilla: Casilla) -> int:
        """Valor de la moneda en `casilla`, o 0 si no hay moneda."""
        for posicion, valor in self.monedas:
            if posicion == casilla:
                return valor
        return 0

    def quedan_monedas(self) -> bool:
        """Verdadero si todavia hay al menos una moneda en el tablero."""
        return len(self.monedas) > 0

    @staticmethod
    def rival(jugador: str) -> str:
        """El otro jugador: VERDE <-> ROJO."""
        if jugador == constantes.VERDE:
            return constantes.ROJO
        if jugador == constantes.ROJO:
            return constantes.VERDE
        raise ValueError(f"Jugador desconocido: {jugador!r}")
