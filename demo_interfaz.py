"""
Demo de la interfaz de Yoshi's Battle (tablero, Yoshis, monedas, marcador y generador)
mientras se terminan el minimax, el controlador y las pantallas.

    python demo_interfaz.py              (nivel Principiante)
    python demo_interfaz.py experto      (solo cambia la etiqueta del marcador)

Controles:
    Clic en una casilla resaltada -> mover el Yoshi rojo (tu)
    R                              -> nuevo tablero aleatorio
    M                              -> silenciar / activar el sonido
    Esc / cerrar ventana           -> salir

Audio: la musica se busca en assets/sonidos/ (musica.mp3, music.ogg, ...) y suena en
bucle hasta que termina la partida; el sonido de la moneda suena al recogerla.

OJO: la maquina NO usa minimax. Toma la moneda de mas valor que tenga a un salto y, si
no hay ninguna, salta al azar. Es solo para probar la parte visual; no hace parte del
juego final.
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import pygame  # noqa: E402

from yoshis_battle import constantes  # noqa: E402
from yoshis_battle.gui import estilo, sonido  # noqa: E402
from yoshis_battle.gui.panel_marcador import PanelMarcador  # noqa: E402
from yoshis_battle.gui.panel_tablero import PanelTablero  # noqa: E402
from yoshis_battle.juego.generador import generar_estado_inicial  # noqa: E402
from yoshis_battle.juego.reglas import (  # noqa: E402
    aplicar_movimiento, es_terminal, movimientos_validos)

PAUSA_MAQUINA_MS = 700  # cuanto "piensa" la maquina antes de mover


def jugada_de_prueba(estado, rng: random.Random):
    """Reemplazo temporal del minimax: la moneda mas valiosa a un salto, o al azar."""
    opciones = movimientos_validos(estado)
    mejor = max(estado.valor_moneda_en(c) for c in opciones)
    if mejor > 0:
        opciones = [c for c in opciones if estado.valor_moneda_en(c) == mejor]
    return rng.choice(opciones)


def elegir_nivel_por_argumento() -> str:
    if len(sys.argv) > 1:
        buscado = sys.argv[1].lower()
        for nivel in constantes.PROFUNDIDAD_POR_NIVEL:
            if nivel.lower().startswith(buscado):
                return nivel
    return constantes.PRINCIPIANTE


def main() -> int:
    pygame.init()
    pantalla = pygame.display.set_mode(estilo.TAMANO_VENTANA)
    pygame.display.set_caption("Yoshi's Battle - demo de la interfaz")
    reloj = pygame.time.Clock()

    tablero = PanelTablero(estilo.RECT_TABLERO)
    marcador = PanelMarcador(estilo.RECT_MARCADOR)
    nivel = elegir_nivel_por_argumento()
    rng = random.Random()

    estado = generar_estado_inicial(rng)
    ultima_jugada = None
    inicio_espera = pygame.time.get_ticks()  # la maquina empieza

    while True:
        ahora = pygame.time.get_ticks()
        hover = tablero.casilla_en(pygame.mouse.get_pos())
        # Mientras un Yoshi esta saltando no se acepta otra jugada.
        animando = tablero.animando()
        turno_humano = (not animando and not es_terminal(estado)
                        and estado.turno == constantes.JUGADOR_HUMANO)
        resaltadas = movimientos_validos(estado) if turno_humano else []

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return 0
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return 0
                if evento.key == pygame.K_m:
                    sonido.alternar_silencio()
                if evento.key == pygame.K_r:
                    estado = generar_estado_inicial(rng)
                    ultima_jugada = None
                    tablero.reiniciar()
                    inicio_espera = ahora
            if (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1
                    and turno_humano):
                destino = tablero.casilla_en(evento.pos)
                if destino in resaltadas:
                    estado = aplicar_movimiento(estado, destino)
                    inicio_espera = ahora

        # Turno de la maquina: espera un momento para que se note y luego mueve.
        pensando = (not es_terminal(estado)
                    and estado.turno == constantes.JUGADOR_MAQUINA)
        if animando:
            inicio_espera = ahora  # la maquina "piensa" despues de que aterrice el salto
        if pensando and not animando and ahora - inicio_espera >= PAUSA_MAQUINA_MS:
            origen = estado.pos_verde
            destino = jugada_de_prueba(estado, rng)
            estado = aplicar_movimiento(estado, destino)
            ultima_jugada = (origen, destino)
            pensando = False

        pantalla.fill(estilo.COLOR_FONDO)
        tablero.dibujar(pantalla, estado, resaltadas=resaltadas,
                        ultima_jugada=ultima_jugada, casilla_hover=hover)
        marcador.dibujar(pantalla, estado, nivel, pensando=pensando)
        fuente = estilo.fuente(estilo.FAMILIA_TEXTO, "bold", 14)
        centro_x = estilo.RECT_MARCADOR[0] + estilo.RECT_MARCADOR[2] // 2
        if es_terminal(estado):
            estilo.dibujar_texto(pantalla, "Presiona R para jugar otra vez", fuente,
                                 estilo.COLOR_DORADO,
                                 (centro_x, estilo.ALTO_VENTANA - 12), ancla="midbottom")
        else:
            aviso = "M: activar sonido" if sonido.silenciado() else "M: silenciar"
            estilo.dibujar_texto(pantalla, aviso, fuente, estilo.COLOR_TEXTO_SUAVE,
                                 (centro_x, estilo.ALTO_VENTANA - 12), ancla="midbottom")
        pygame.display.flip()
        reloj.tick(60)


if __name__ == "__main__":
    sys.exit(main())
