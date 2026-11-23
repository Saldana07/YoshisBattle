"""
Archivo:       src/yoshis_battle/gui/panel_tablero.py
Objetivo:      Dibujar el tablero 8 x 8 con las monedas y los dos Yoshis, y traducir
               clics del mouse a casillas.
Responsabilidad:
    SI hace:
        - Dibujar las casillas, las monedas (normales y especiales) y los Yoshis a
          partir de un Estado.
        - Resaltar las casillas a las que puede saltar el humano en su turno.
        - Resaltar la ultima jugada de la maquina para que el usuario la vea.
        - Convertir una posicion en pixeles a una casilla (fila, columna) o None.
    NO hace:
        - No decide si una jugada es valida (recibe la lista ya calculada).
        - No lee eventos: eso es gui/ventana_juego.py.
Importa de:    pygame, constantes, modelo/estado.py, gui/estilo.py,
               gui/cargador_sprites.py.
Lo importan:   gui/ventana_juego.py.
Contrato previsto:
    - PanelTablero(rect)
    - PanelTablero.dibujar(superficie, estado, resaltadas=(), ultima_jugada=None) -> None
    - PanelTablero.casilla_en(posicion_pixel) -> Casilla | None
"""
from __future__ import annotations


class PanelTablero:
    def __init__(self, rect) -> None:
        self.rect = rect
        raise NotImplementedError("PENDIENTE: gui/panel_tablero.py PanelTablero.__init__")

    def dibujar(self, superficie, estado, resaltadas=(), ultima_jugada=None) -> None:
        raise NotImplementedError("PENDIENTE: gui/panel_tablero.py dibujar")

    def casilla_en(self, posicion_pixel):
        raise NotImplementedError("PENDIENTE: gui/panel_tablero.py casilla_en")
