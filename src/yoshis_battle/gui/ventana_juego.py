"""
Archivo:       src/yoshis_battle/gui/ventana_juego.py
Objetivo:      Correr el bucle de eventos de una partida: turno de la maquina, clics del
               humano y redibujado del tablero y el marcador.
Responsabilidad:
    SI hace:
        - Dibujar PanelTablero y PanelMarcador en cada cuadro.
        - En el turno de la maquina: mostrar "pensando", pedir Partida.jugar_maquina()
          y hacer una pausa corta para que se vea la jugada.
        - En el turno del humano: resaltar Partida.movimientos_humano() y aplicar el
          clic con Partida.jugar_humano(destino).
        - Terminar cuando la partida termina (o con Esc / cerrar ventana).
    NO hace:
        - No implementa reglas ni IA; no muestra la pantalla final.
Importa de:    pygame, controlador/partida.py, gui/estilo.py, gui/panel_tablero.py,
               gui/panel_marcador.py.
Lo importan:   main.py.
Contrato previsto:
    - TERMINADA, VOLVER, SALIR: constantes de resultado.
    - jugar_partida(pantalla, partida) -> str
          TERMINADA si se acabaron las monedas, VOLVER con Esc, SALIR al cerrar.
PENDIENTE:
    - Si minimax en experto tarda, decidir si se corre en un hilo para que la ventana
      no se congele.
"""
from __future__ import annotations

TERMINADA = "terminada"
VOLVER = "volver"
SALIR = "salir"


def jugar_partida(pantalla, partida) -> str:
    """Bucle de una partida; retorna TERMINADA, VOLVER o SALIR."""
    raise NotImplementedError("PENDIENTE: gui/ventana_juego.py jugar_partida")
