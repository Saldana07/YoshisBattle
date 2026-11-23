"""
Archivo:       src/yoshis_battle/gui/pantalla_inicio.py
Objetivo:      Crear la ventana y mostrar la pantalla de bienvenida donde el usuario
               elige el nivel de dificultad.
Responsabilidad:
    SI hace:
        - Crear la ventana de pygame con el tamano de gui/estilo.py.
        - Mostrar el titulo, una explicacion corta de las reglas y tres botones:
          Principiante (profundidad 2), Intermedio (4) y Experto (6).
        - Retornar el nivel elegido, o None si el usuario cierra la ventana o pulsa Esc.
    NO hace:
        - No crea la Partida ni juega: eso lo hace main.py con controlador/partida.py.
Importa de:    pygame, constantes (niveles), gui/estilo.py, gui/cargador_sprites.py.
Lo importan:   main.py.
Contrato previsto:
    - crear_ventana() -> pygame.Surface
    - elegir_nivel(pantalla) -> str | None
          Retorna constantes.PRINCIPIANTE, INTERMEDIO o EXPERTO.
"""
from __future__ import annotations


def crear_ventana():
    """Inicializa pygame y crea la ventana del juego."""
    raise NotImplementedError("PENDIENTE: gui/pantalla_inicio.py crear_ventana")


def elegir_nivel(pantalla) -> str | None:
    """Pantalla de bienvenida; retorna el nivel elegido o None si el usuario sale."""
    raise NotImplementedError("PENDIENTE: gui/pantalla_inicio.py elegir_nivel")
