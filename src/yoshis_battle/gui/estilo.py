"""
Archivo:       src/yoshis_battle/gui/estilo.py
Objetivo:      Reunir lo que comparten todas las pantallas: tamano de ventana, paleta de
               colores, tipografias y utilidades para dibujar texto.
Responsabilidad:
    SI hace:
        - Definir el tamano de la ventana y la paleta.
        - Cargar las tipografias Pixelify Sans y DM Sans desde gui/fuentes/ (ver el
          LEEME.md de esa carpeta), con una fuente del sistema si faltan.
        - Ofrecer utilidades de texto (dibujar con ancla, partir en lineas).
    NO hace:
        - No conoce ninguna pantalla ni la logica del juego.
        - No lee assets/: eso es solo gui/cargador_sprites.py.
Importa de:    pygame (pygame-ce).
Lo importan:   todos los demas archivos de gui/.
Contrato previsto:
    - ANCHO_VENTANA, ALTO_VENTANA, TAMANO_VENTANA
    - COLOR_* (paleta)
    - fuente(familia, peso, tamano) -> pygame.font.Font
    - dibujar_texto(superficie, texto, fuente, color, posicion, ancla="topleft") -> pygame.Rect
PENDIENTE:
    - Paleta definitiva (se puede reutilizar la de AgroBot o una con colores de Yoshi).
    - Se puede copiar la carga de fuentes de src/agrobot/gui/estilo.py del Proyecto 1.
"""
from __future__ import annotations

ANCHO_VENTANA = 1120
ALTO_VENTANA = 760
TAMANO_VENTANA = (ANCHO_VENTANA, ALTO_VENTANA)


def fuente(familia: str, peso: str, tamano: int):
    """Fuente de gui/fuentes/ (o del sistema si falta el archivo)."""
    raise NotImplementedError("PENDIENTE: gui/estilo.py fuente")


def dibujar_texto(superficie, texto: str, fuente_texto, color, posicion, ancla: str = "topleft"):
    """Dibuja `texto` anclado en `posicion` y retorna su rectangulo."""
    raise NotImplementedError("PENDIENTE: gui/estilo.py dibujar_texto")
