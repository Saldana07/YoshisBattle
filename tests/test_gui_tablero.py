"""
Archivo:       tests/test_gui_tablero.py
Objetivo:      Verificar la parte de la GUI que se puede probar sin abrir ventana:
               carga de sprites (con sus reemplazos), conversion clic -> casilla y que
               el tablero y el marcador se dibujan sin errores.
QUE VERIFICA:
    - cargar_sprites entrega todas las claves del contrato y las monedas animadas.
    - casilla_en y rect_casilla son inversas; fuera del tablero da None.
    - PanelTablero.dibujar y PanelMarcador.dibujar corren sobre un estado inicial.
Nota:          Si pygame-ce no esta instalado, estas pruebas se saltan.
"""
import os
import random
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

try:
    import pygame
except ImportError:  # pragma: no cover
    pygame = None

from yoshis_battle import constantes  # noqa: E402
from yoshis_battle.juego.generador import generar_estado_inicial  # noqa: E402

CLAVES = {"yoshi_verde", "yoshi_rojo", "moneda_normal", "moneda_especial",
          "casilla_clara", "casilla_oscura"}


@unittest.skipIf(pygame is None, "pygame-ce no esta instalado")
class TestGuiTablero(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.pantalla = pygame.display.set_mode((1120, 760))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_sprites_con_todas_las_claves(self):
        from yoshis_battle.gui.cargador_sprites import cargar_animaciones, cargar_sprites
        sprites = cargar_sprites(64)
        self.assertTrue(CLAVES.issubset(sprites))
        for clave in CLAVES:
            ancho, alto = sprites[clave].get_size()
            self.assertLessEqual(ancho, 64, clave)
            self.assertLessEqual(alto, 64, clave)
        animaciones = cargar_animaciones(64)
        self.assertGreaterEqual(len(animaciones["moneda_normal"]), 1)
        self.assertGreaterEqual(len(animaciones["moneda_especial"]), 1)

    def test_yoshis_animados_en_8_direcciones(self):
        from yoshis_battle.gui.cargador_sprites import (ANIMACION_CELEBRAR,
                                                        ANIMACION_ESPERAR, DIRECCIONES,
                                                        cargar_animaciones_yoshi)
        caminar = cargar_animaciones_yoshi(56)
        for clave in ("yoshi_verde", "yoshi_rojo"):
            self.assertEqual(set(caminar[clave]),
                             set(DIRECCIONES) | {ANIMACION_CELEBRAR, ANIMACION_ESPERAR})
            for nombre in caminar[clave]:
                self.assertGreaterEqual(len(caminar[clave][nombre]), 1)
        # El rojo es un recoloreado: mismo tamano, distintos pixeles.
        verde = caminar["yoshi_verde"]["abajo"][0]
        rojo = caminar["yoshi_rojo"]["abajo"][0]
        self.assertEqual(verde.get_size(), rojo.get_size())
        self.assertNotEqual(pygame.image.tobytes(verde, "RGBA"),
                            pygame.image.tobytes(rojo, "RGBA"))

    def test_direccion_hacia(self):
        from yoshis_battle.gui.panel_tablero import direccion_hacia
        self.assertEqual(direccion_hacia((4, 4), (4, 7)), "derecha")
        self.assertEqual(direccion_hacia((4, 4), (0, 4)), "arriba")
        self.assertEqual(direccion_hacia((4, 4), (7, 1)), "abajo_izquierda")
        self.assertEqual(direccion_hacia((4, 4), (2, 5)), "arriba_derecha")

    def test_detecta_el_salto_y_lo_anima(self):
        from yoshis_battle.gui import panel_tablero
        from yoshis_battle.juego.reglas import aplicar_movimiento, movimientos_validos
        reloj = [1000]
        original = panel_tablero.pygame.time.get_ticks
        panel_tablero.pygame.time.get_ticks = lambda: reloj[0]
        try:
            tablero = panel_tablero.PanelTablero((40, 40, 476, 476))
            estado = generar_estado_inicial(random.Random(3))
            tablero.dibujar(self.pantalla, estado)
            self.assertFalse(tablero.animando())
            siguiente = aplicar_movimiento(estado, movimientos_validos(estado)[0])
            tablero.dibujar(self.pantalla, siguiente)
            self.assertTrue(tablero.animando())
            reloj[0] += panel_tablero.DURACION_SALTO_MS // 2
            tablero.dibujar(self.pantalla, siguiente)
            self.assertTrue(tablero.animando())
            reloj[0] += panel_tablero.DURACION_SALTO_MS
            tablero.dibujar(self.pantalla, siguiente)
            self.assertFalse(tablero.animando())
            # Una partida nueva no se anima: se coloca de una vez.
            tablero.dibujar(self.pantalla, generar_estado_inicial(random.Random(99)))
            self.assertFalse(tablero.animando())
        finally:
            panel_tablero.pygame.time.get_ticks = original

    def test_celebra_solo_el_ganador(self):
        from yoshis_battle.gui.panel_tablero import PanelTablero
        from yoshis_battle.modelo.estado import Estado
        tablero = PanelTablero((40, 40, 476, 476))
        casos = ((9, 4, constantes.VERDE), (4, 9, constantes.ROJO), (6, 6, None))
        for verde, rojo, esperado in casos:
            with self.subTest(verde=verde, rojo=rojo):
                tablero.reiniciar()
                final = Estado((0, 0), (7, 7), frozenset(), verde, rojo, constantes.ROJO)
                tablero.dibujar(self.pantalla, final)
                self.assertEqual(tablero._celebra, esperado)

    def test_humano_que_tarda_pone_a_esperar_a_su_yoshi(self):
        from yoshis_battle.gui import panel_tablero
        from yoshis_battle.juego.reglas import aplicar_movimiento, movimientos_validos
        reloj = [1000]
        original = panel_tablero.pygame.time.get_ticks
        panel_tablero.pygame.time.get_ticks = lambda: reloj[0]
        try:
            tablero = panel_tablero.PanelTablero((40, 40, 476, 476))
            estado = generar_estado_inicial(random.Random(5))
            tablero.dibujar(self.pantalla, estado)       # turno de la maquina
            reloj[0] += 10_000
            tablero.dibujar(self.pantalla, estado)
            self.assertFalse(tablero._esperando)         # la maquina no "espera"
            estado = aplicar_movimiento(estado, movimientos_validos(estado)[0])
            tablero.dibujar(self.pantalla, estado)       # salta la maquina
            reloj[0] += panel_tablero.DURACION_SALTO_MS + 10
            tablero.dibujar(self.pantalla, estado)       # aterrizo: turno del humano
            self.assertFalse(tablero._esperando)
            reloj[0] += panel_tablero.ESPERA_ANTES_DE_ANIMAR_MS
            tablero.dibujar(self.pantalla, estado)
            self.assertTrue(tablero._esperando)
            estado = aplicar_movimiento(estado, movimientos_validos(estado)[0])
            tablero.dibujar(self.pantalla, estado)       # el humano jugo
            self.assertFalse(tablero._esperando)
        finally:
            panel_tablero.pygame.time.get_ticks = original

    def test_musica_hasta_el_final_y_moneda(self):
        from yoshis_battle.gui import cargador_sprites, panel_tablero, sonido
        from yoshis_battle.modelo.estado import Estado
        from yoshis_battle.juego.reglas import aplicar_movimiento
        self.assertIsNotNone(cargador_sprites.ruta_sonido_moneda())
        sonido.sonar_moneda()  # no debe fallar (con o sin audio)
        # Musica de prueba: se usa el mismo archivo de la moneda como "cancion".
        original_ruta = cargador_sprites.ruta_musica
        cargador_sprites.ruta_musica = cargador_sprites.ruta_sonido_moneda
        reloj = [1000]
        original_ticks = panel_tablero.pygame.time.get_ticks
        panel_tablero.pygame.time.get_ticks = lambda: reloj[0]
        try:
            tablero = panel_tablero.PanelTablero((40, 40, 476, 476))
            antes = Estado((5, 5), (1, 2), frozenset({((3, 4), 3)}), 9, 8,
                           constantes.VERDE)
            tablero.dibujar(self.pantalla, antes)
            self.assertEqual(tablero._musica_sonando, sonido.disponible())
            tablero.dibujar(self.pantalla, aplicar_movimiento(antes, (3, 4)))
            self.assertEqual(tablero._musica_sonando, sonido.disponible())  # aun salta
            reloj[0] += panel_tablero.DURACION_SALTO_MS + 10
            tablero.dibujar(self.pantalla, aplicar_movimiento(antes, (3, 4)))
            self.assertFalse(tablero._musica_sonando)                      # termino
        finally:
            cargador_sprites.ruta_musica = original_ruta
            panel_tablero.pygame.time.get_ticks = original_ticks
            sonido.detener_musica(0)

    def test_casilla_en_es_inversa_de_rect_casilla(self):
        from yoshis_battle.gui.panel_tablero import PanelTablero
        panel = PanelTablero((40, 40, 680, 680))
        n = constantes.TAMANO_TABLERO
        for fila in range(n):
            for columna in range(n):
                rect = panel.rect_casilla((fila, columna))
                self.assertEqual(panel.casilla_en(rect.center), (fila, columna))
                self.assertEqual(panel.casilla_en(rect.topleft), (fila, columna))
                self.assertEqual(panel.casilla_en((rect.right - 1, rect.bottom - 1)),
                                 (fila, columna))
        self.assertIsNone(panel.casilla_en((0, 0)))
        self.assertIsNone(panel.casilla_en(panel.rect_tablero.bottomright))

    def test_dibujar_tablero_y_marcador(self):
        from yoshis_battle.gui.panel_marcador import PanelMarcador
        from yoshis_battle.gui.panel_tablero import PanelTablero
        from yoshis_battle.juego.reglas import movimientos_validos
        estado = generar_estado_inicial(random.Random(1))
        tablero = PanelTablero((40, 40, 680, 680))
        marcador = PanelMarcador((760, 40, 320, 680))
        tablero.dibujar(self.pantalla, estado,
                        resaltadas=movimientos_validos(estado, constantes.ROJO),
                        ultima_jugada=(estado.pos_verde, estado.pos_rojo))
        tablero.dibujar(self.pantalla, estado, ultima_jugada=estado.pos_verde)
        for nivel in constantes.PROFUNDIDAD_POR_NIVEL:
            marcador.dibujar(self.pantalla, estado, nivel, pensando=True)


if __name__ == "__main__":
    unittest.main()
