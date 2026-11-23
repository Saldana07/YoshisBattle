"""
Archivo:       src/yoshis_battle/gui/cargador_sprites.py
Objetivo:      Ser el unico archivo del proyecto que conoce la carpeta assets/sprites/ y
               entregar las imagenes por nombre al resto de la GUI.
Responsabilidad:
    SI hace:
        - Cargar una vez los sprites: Yoshi verde, Yoshi rojo, moneda normal, moneda
          especial y casillas del tablero (ver assets/README.md).
        - Escalarlos al tamano de casilla sin suavizar (pygame.transform.scale con
          factor entero), igual que en AgroBot.
        - Si falta un sprite, devolver un reemplazo dibujado (circulo de color) para
          que el juego no se caiga.
    NO hace:
        - No dibuja el tablero: eso es gui/panel_tablero.py.
Importa de:    pygame (pygame-ce).
Lo importan:   gui/panel_tablero.py, gui/pantalla_inicio.py, gui/pantalla_final.py.
Contrato previsto:
    - CARPETA_SPRITES: Path a assets/sprites/.
    - cargar_sprites(tamano_casilla) -> dict[str, pygame.Surface]
          Claves: "yoshi_verde", "yoshi_rojo", "moneda_normal", "moneda_especial",
          "casilla_clara", "casilla_oscura".
"""
from __future__ import annotations

from pathlib import Path

CARPETA_SPRITES = Path(__file__).resolve().parents[3] / "assets" / "sprites"


def cargar_sprites(tamano_casilla: int) -> dict:
    """Sprites del juego escalados a `tamano_casilla` pixeles."""
    raise NotImplementedError("PENDIENTE: gui/cargador_sprites.py cargar_sprites")
