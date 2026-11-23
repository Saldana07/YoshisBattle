"""
Archivo:       src/yoshis_battle/gui/panel_marcador.py
Objetivo:      Mostrar en todo momento los puntos de cada jugador, de quien es el turno,
               el nivel elegido y cuantas monedas quedan.
Responsabilidad:
    SI hace:
        - Dibujar el marcador: puntos de la maquina (verde) y del humano (rojo).
        - Indicar el turno ("Tu turno" / "La maquina esta pensando...").
        - Mostrar el nivel y, opcionalmente, datos de la ultima decision de la IA
          (nodos expandidos y tiempo).
    NO hace:
        - No calcula puntos: los lee del Estado.
Importa de:    pygame, constantes, modelo/estado.py, ia/minimax.py (Decision),
               gui/estilo.py.
Lo importan:   gui/ventana_juego.py.
Contrato previsto:
    - PanelMarcador(rect)
    - PanelMarcador.dibujar(superficie, estado, nivel, pensando=False, decision=None) -> None
"""
from __future__ import annotations


class PanelMarcador:
    def __init__(self, rect) -> None:
        self.rect = rect
        raise NotImplementedError("PENDIENTE: gui/panel_marcador.py PanelMarcador.__init__")

    def dibujar(self, superficie, estado, nivel, pensando=False, decision=None) -> None:
        raise NotImplementedError("PENDIENTE: gui/panel_marcador.py dibujar")
