"""
Archivo:       src/yoshis_battle/gui/pantalla_final.py
Objetivo:      Anunciar al final de la partida quien gano (o si hubo empate) con el
               marcador final.
Responsabilidad:
    SI hace:
        - Mostrar el ganador, los puntos finales y dos opciones: jugar de nuevo o salir.
    NO hace:
        - No decide el ganador: lo recibe de controlador/partida.py.
Importa de:    pygame, constantes, gui/estilo.py, gui/cargador_sprites.py.
Lo importan:   main.py.
Contrato previsto:
    - mostrar_resultado(pantalla, ganador, puntos_verde, puntos_rojo) -> bool
          True = jugar de nuevo, False = salir.
"""
from __future__ import annotations


def mostrar_resultado(pantalla, ganador: str, puntos_verde: int, puntos_rojo: int) -> bool:
    """Pantalla final; retorna True si el usuario quiere jugar otra vez."""
    raise NotImplementedError("PENDIENTE: gui/pantalla_final.py mostrar_resultado")
