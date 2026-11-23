"""
Archivo:       src/yoshis_battle/main.py
Objetivo:      Punto de entrada del juego: crear la ventana y conectar todas las piezas
               (controlador, ia, juego, modelo y gui).
Responsabilidad:
    SI hace:
        - Orquestar el flujo: elegir nivel -> partida -> pantalla final -> de nuevo al
          inicio, hasta que el usuario cierre la aplicacion.
        - Ser el unico archivo que importa de gui/ (composicion).
    NO hace:
        - No implementa reglas, IA ni dibujo: delega todo.
Importa de:    controlador/partida.py, gui/pantalla_inicio.py, gui/ventana_juego.py,
               gui/pantalla_final.py.
Lo importan:   ejecutar.py.
Ejecucion:
    Desde la raiz del repositorio:   python ejecutar.py
    Desde la carpeta src/:           python -m yoshis_battle.main
Contrato previsto:
    - punto_de_entrada() -> int: 0 si todo bien, 1 si falta pygame-ce o hay piezas
      sin implementar.
"""
from __future__ import annotations

import sys


def punto_de_entrada() -> int:
    """Corre el juego completo. Retorna el codigo de salida del proceso."""
    try:
        import pygame
    except ImportError:
        print(
            "No se encontro pygame-ce. Activa el entorno virtual e instala las "
            "dependencias con: pip install -r requirements.txt",
            file=sys.stderr,
        )
        return 1

    from .controlador.partida import Partida
    from .gui.pantalla_final import mostrar_resultado
    from .gui.pantalla_inicio import crear_ventana, elegir_nivel
    from .gui.ventana_juego import SALIR, TERMINADA, jugar_partida

    try:
        pantalla = crear_ventana()
        while True:
            nivel = elegir_nivel(pantalla)
            if nivel is None:
                return 0
            partida = Partida(nivel)
            resultado = jugar_partida(pantalla, partida)
            if resultado == SALIR:
                return 0
            if resultado == TERMINADA:
                estado = partida.estado
                if not mostrar_resultado(pantalla, partida.ganador(),
                                         estado.puntos_verde, estado.puntos_rojo):
                    return 0
    except NotImplementedError as pendiente:
        print(f"Esqueleto: todavia falta implementar -> {pendiente}", file=sys.stderr)
        return 1
    finally:
        pygame.quit()


if __name__ == "__main__":
    sys.exit(punto_de_entrada())
