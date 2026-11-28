"""
Archivo:       src/yoshis_battle/gui/panel_marcador.py
Objetivo:      Mostrar en todo momento los puntos de cada jugador, de quien es el turno,
               el nivel elegido y cuantas monedas quedan.
Responsabilidad:
    SI hace:
        - Dibujar el marcador: puntos de la maquina (verde) y del humano (rojo), cada
          uno en una tarjeta con su Yoshi; la tarjeta del jugador de turno se resalta.
        - Indicar el turno ("Tu turno" / "La maquina esta pensando...") o, si la
          partida termino, quien gano.
        - Mostrar el nivel (con su profundidad), las monedas que quedan y los puntos
          que siguen en juego.
        - Mostrar, si se pasa, la ultima decision de la IA (casilla, valor, nodos
          expandidos y tiempo).
    NO hace:
        - No calcula puntos: los lee del Estado.
Importa de:    pygame, constantes, modelo/estado.py, juego/reglas.py (ganador),
               ia/minimax.py (Decision), gui/estilo.py, gui/cargador_sprites.py.
Lo importan:   gui/ventana_juego.py.
Contrato:
    - PanelMarcador(rect)        rect: p. ej. estilo.RECT_MARCADOR (~320 x 680 px).
    - PanelMarcador.dibujar(superficie, estado, nivel, pensando=False, decision=None) -> None
          decision: Decision de la ultima jugada de la maquina (o None).
"""
from __future__ import annotations

import pygame

from .. import constantes
from ..juego import reglas
from ..modelo.estado import Estado
from . import estilo
from .cargador_sprites import ANIMACION_CELEBRAR, cargar_animaciones_yoshi, cargar_sprites

ALTO_TARJETA = 108
TAMANO_ICONO_YOSHI = 84   # con la hoja actual da un Yoshi de ~48 x 76 (factor 2)
ANCHO_ZONA_ICONO = 50
TAMANO_ICONO_MONEDA = 40
MS_POR_CUADRO_ICONO = 110  # el Yoshi de turno camina en su sitio


class PanelMarcador:
    def __init__(self, rect) -> None:
        self.rect = pygame.Rect(rect)
        caminar = cargar_animaciones_yoshi(TAMANO_ICONO_YOSHI)
        monedas = cargar_sprites(TAMANO_ICONO_MONEDA)
        # Verde mira a la derecha y rojo a la izquierda: quedan "frente a frente".
        self._icono_yoshi = {constantes.VERDE: caminar["yoshi_verde"]["abajo_derecha"],
                             constantes.ROJO: caminar["yoshi_rojo"]["abajo_izquierda"]}
        self._icono_celebrar = {constantes.VERDE: caminar["yoshi_verde"][ANIMACION_CELEBRAR],
                                constantes.ROJO: caminar["yoshi_rojo"][ANIMACION_CELEBRAR]}
        self._icono_moneda = {constantes.VALOR_MONEDA_ESPECIAL: monedas["moneda_especial"],
                              constantes.VALOR_MONEDA_NORMAL: monedas["moneda_normal"]}

        self._f_titulo = estilo.fuente(estilo.FAMILIA_TITULO, "regular", 30)
        self._f_puntos = estilo.fuente(estilo.FAMILIA_TITULO, "regular", 40)
        self._f_nombre = estilo.fuente(estilo.FAMILIA_PIXEL, "bold", 22)
        self._f_seccion = estilo.fuente(estilo.FAMILIA_PIXEL, "medium", 17)
        self._f_texto = estilo.fuente(estilo.FAMILIA_TEXTO, "regular", 15)
        self._f_texto_fuerte = estilo.fuente(estilo.FAMILIA_TEXTO, "bold", 15)
        self._f_chico = estilo.fuente(estilo.FAMILIA_TEXTO, "regular", 13)

        self._datos_jugador = {
            constantes.VERDE: ("Máquina", "Yoshi verde · MAX", estilo.COLOR_VERDE),
            constantes.ROJO: ("Tú", "Yoshi rojo · MIN", estilo.COLOR_ROJO),
        }

    # ------------------------------------------------------------ dibujo
    def dibujar(self, superficie, estado: Estado, nivel, pensando=False,
                decision=None) -> None:
        estilo.dibujar_caja(superficie, self.rect, estilo.COLOR_FONDO_PANEL,
                            borde=estilo.COLOR_BORDE, radio=16)
        x = self.rect.left + 18
        ancho = self.rect.width - 36
        y = self.rect.top + 18

        y = self._dibujar_encabezado(superficie, x, y, ancho, nivel)
        terminada = reglas.es_terminal(estado)
        ganador = reglas.ganador(estado) if terminada else None
        for jugador in (constantes.VERDE, constantes.ROJO):
            puntos = estado.puntos_verde if jugador == constantes.VERDE else estado.puntos_rojo
            activo = (not terminada) and estado.turno == jugador
            self._dibujar_tarjeta(superficie, pygame.Rect(x, y, ancho, ALTO_TARJETA),
                                  jugador, puntos, activo, celebra=jugador == ganador)
            y += ALTO_TARJETA + 12

        y = self._dibujar_monedas(superficie, x, y + 4, ancho, estado)
        y = self._dibujar_mensaje(superficie, x, y + 10, ancho, estado, pensando, terminada)
        if decision is not None:
            self._dibujar_decision(superficie, x, y + 10, ancho, decision)

        estilo.dibujar_texto(superficie, "Esc: volver al menú", self._f_chico,
                             estilo.COLOR_TEXTO_SUAVE,
                             (self.rect.centerx, self.rect.bottom - 14), ancla="midbottom")

    # ------------------------------------------------------------ secciones
    def _dibujar_encabezado(self, superficie, x, y, ancho, nivel) -> int:
        estilo.dibujar_texto(superficie, "Yoshi's Battle", self._f_titulo,
                             estilo.COLOR_DORADO, (x + ancho // 2, y), ancla="midtop",
                             sombra=estilo.COLOR_SOMBRA)
        y += self._f_titulo.get_height() + 8
        profundidad = constantes.PROFUNDIDAD_POR_NIVEL.get(nivel)
        texto = f"Nivel {nivel}" + (f"  ·  profundidad {profundidad}"
                                    if profundidad is not None else "")
        chip = pygame.Rect(0, 0, ancho, 28)
        chip.midtop = (x + ancho // 2, y)
        estilo.dibujar_caja(superficie, chip, estilo.COLOR_TARJETA, radio=14)
        estilo.dibujar_texto(superficie, texto, self._f_texto, estilo.COLOR_TEXTO,
                             chip.center, ancla="center")
        return chip.bottom + 14

    def _dibujar_tarjeta(self, superficie, rect, jugador, puntos, activo,
                         celebra=False) -> None:
        nombre, detalle, color = self._datos_jugador[jugador]
        if celebra:
            borde, grosor = estilo.COLOR_DORADO, 3
        else:
            borde, grosor = (color, 3) if activo else (estilo.COLOR_BORDE, 1)
        estilo.dibujar_caja(superficie, rect, estilo.COLOR_TARJETA, borde=borde,
                            grosor=grosor, radio=14)
        # Franja de color a la izquierda.
        pygame.draw.rect(superficie, color, (rect.left, rect.top + 14, 6, rect.height - 28),
                         border_radius=3)

        # El de turno camina en su sitio; el ganador levanta los brazos.
        if celebra:
            cuadros, animado = self._icono_celebrar[jugador], True
        else:
            cuadros, animado = self._icono_yoshi[jugador], activo
        indice = (pygame.time.get_ticks() // MS_POR_CUADRO_ICONO) % len(cuadros) if animado else 0
        icono = cuadros[indice]
        centro_icono = rect.left + 16 + ANCHO_ZONA_ICONO // 2
        superficie.blit(icono, icono.get_rect(
            midbottom=(centro_icono, rect.centery + icono.get_height() // 2)))

        texto_x = rect.left + 16 + ANCHO_ZONA_ICONO + 12
        estilo.dibujar_texto(superficie, nombre, self._f_nombre, estilo.COLOR_TEXTO,
                             (texto_x, rect.top + 22))
        estilo.dibujar_texto(superficie, detalle, self._f_chico, estilo.COLOR_TEXTO_SUAVE,
                             (texto_x, rect.top + 52))
        if activo or celebra:
            texto, fondo = ("GANADOR", estilo.COLOR_DORADO) if celebra else ("TURNO", color)
            etiqueta = self._f_chico.render(texto, True, estilo.COLOR_FONDO)
            caja = etiqueta.get_rect().inflate(14, 6)
            caja.topleft = (texto_x, rect.top + 74)
            estilo.dibujar_caja(superficie, caja, fondo, radio=caja.height // 2)
            superficie.blit(etiqueta, etiqueta.get_rect(center=caja.center))

        derecha = rect.right - 16
        rect_puntos = estilo.dibujar_texto(superficie, str(puntos), self._f_puntos, color,
                                           (derecha, rect.centery - 6), ancla="midright",
                                           sombra=estilo.COLOR_SOMBRA)
        estilo.dibujar_texto(superficie, "pts", self._f_chico, estilo.COLOR_TEXTO_SUAVE,
                             (rect_puntos.centerx, rect_puntos.bottom + 2), ancla="midtop")

    def _dibujar_monedas(self, superficie, x, y, ancho, estado: Estado) -> int:
        estilo.dibujar_texto(superficie, "Monedas en el tablero", self._f_seccion,
                             estilo.COLOR_TEXTO, (x, y))
        y += self._f_seccion.get_height() + 8
        especiales = sum(1 for _, v in estado.monedas if v == constantes.VALOR_MONEDA_ESPECIAL)
        normales = sum(1 for _, v in estado.monedas if v == constantes.VALOR_MONEDA_NORMAL)
        en_juego = sum(v for _, v in estado.monedas)

        mitad = ancho // 2
        for i, (valor, cantidad, texto) in enumerate((
                (constantes.VALOR_MONEDA_ESPECIAL, especiales, "3 pts c/u"),
                (constantes.VALOR_MONEDA_NORMAL, normales, "1 pt c/u"))):
            caja = pygame.Rect(x + i * mitad, y, mitad - (6 if i == 0 else 0), 48)
            estilo.dibujar_caja(superficie, caja, estilo.COLOR_TARJETA, radio=12)
            icono = self._icono_moneda[valor]
            superficie.blit(icono, icono.get_rect(midleft=(caja.left + 10, caja.centery)))
            tx = caja.left + 10 + TAMANO_ICONO_MONEDA
            estilo.dibujar_texto(superficie, f"x {cantidad}", self._f_texto_fuerte,
                                 estilo.COLOR_TEXTO, (tx, caja.top + 7))
            estilo.dibujar_texto(superficie, texto, self._f_chico, estilo.COLOR_TEXTO_SUAVE,
                                 (tx, caja.top + 26))
        y += 48 + 8
        estilo.dibujar_texto(superficie, f"Puntos en juego: {en_juego}", self._f_texto,
                             estilo.COLOR_TEXTO_SUAVE, (x, y))
        return y + self._f_texto.get_height()

    def _dibujar_mensaje(self, superficie, x, y, ancho, estado: Estado, pensando,
                         terminada) -> int:
        if terminada:
            resultado = reglas.ganador(estado)
            if resultado == constantes.VERDE:
                titulo, color = "¡Gana la máquina!", estilo.COLOR_VERDE
                detalle = "El Yoshi verde reunió más puntos."
            elif resultado == constantes.ROJO:
                titulo, color = "¡Ganaste!", estilo.COLOR_ROJO
                detalle = "Tu Yoshi rojo reunió más puntos."
            else:
                titulo, color = "¡Empate!", estilo.COLOR_DORADO
                detalle = "Ambos Yoshis tienen los mismos puntos."
        elif pensando or estado.turno == constantes.JUGADOR_MAQUINA:
            puntos = "." * (1 + (pygame.time.get_ticks() // 400) % 3)
            titulo = f"La máquina está pensando{puntos}"
            detalle = "Explorando el árbol minimax."
            color = estilo.COLOR_VERDE
        else:
            titulo = "Tu turno"
            detalle = "Haz clic en una casilla resaltada para saltar."
            color = estilo.COLOR_ROJO

        # Si el titulo no cabe con la fuente grande, se usa la mediana.
        f_titulo = self._f_nombre
        if f_titulo.size(titulo)[0] > ancho - 28:
            f_titulo = self._f_seccion
        lineas = estilo.partir_en_lineas(detalle, self._f_texto, ancho - 28)
        alto = (12 + f_titulo.get_height() + 6
                + len(lineas) * (self._f_texto.get_height() + 2) + 12)
        caja = pygame.Rect(x, y, ancho, alto)
        estilo.dibujar_caja(superficie, caja, estilo.COLOR_TARJETA, borde=color, radio=14)
        ty = caja.top + 12
        estilo.dibujar_texto(superficie, titulo, f_titulo, color, (caja.left + 14, ty))
        ty += f_titulo.get_height() + 6
        for linea in lineas:
            estilo.dibujar_texto(superficie, linea, self._f_texto, estilo.COLOR_TEXTO,
                                 (caja.left + 14, ty))
            ty += self._f_texto.get_height() + 2
        return caja.bottom

    def _dibujar_decision(self, superficie, x, y, ancho, decision) -> int:
        estilo.dibujar_texto(superficie, "Última jugada de la IA", self._f_seccion,
                             estilo.COLOR_TEXTO, (x, y))
        y += self._f_seccion.get_height() + 6
        fila, columna = decision.movimiento
        datos = (
            ("Casilla", f"fila {fila}, columna {columna}"),
            ("Valor heurístico", f"{decision.valor:.2f}"),
            ("Nodos expandidos", f"{decision.nodos_expandidos:,}".replace(",", ".")),
            ("Tiempo", f"{decision.segundos:.3f} s"),
        )
        for etiqueta, valor in datos:
            estilo.dibujar_texto(superficie, etiqueta, self._f_texto,
                                 estilo.COLOR_TEXTO_SUAVE, (x, y))
            estilo.dibujar_texto(superficie, valor, self._f_texto_fuerte, estilo.COLOR_TEXTO,
                                 (x + ancho, y), ancla="topright")
            y += self._f_texto.get_height() + 4
        return y
