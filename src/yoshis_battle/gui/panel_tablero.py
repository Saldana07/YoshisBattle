"""
Archivo:       src/yoshis_battle/gui/panel_tablero.py
Objetivo:      Dibujar el tablero 8 x 8 con las monedas y los dos Yoshis (animados), y
               traducir clics del mouse a casillas.
Responsabilidad:
    SI hace:
        - Dibujar las casillas (pasto; las 4 especiales del centro en arena dorada),
          las monedas (girando) y los Yoshis a partir de un Estado.
        - Animar cada jugada sin que nadie se lo pida: cuando el Estado que recibe
          cambia, detecta que Yoshi se movio y lo hace saltar en arco de la casilla
          de origen a la de destino, caminando en la direccion del salto. Si cae en
          una moneda, la moneda hace su animacion de recogida y aparece "+3" / "+1".
        - Hacer que cada Yoshi quieto mire hacia el rival, en 8 direcciones.
        - Cuando la partida termina, el ganador levanta los brazos y da brinquitos
          (animacion "celebrar"; en empate nadie celebra).
        - Si es el turno del humano y pasan ESPERA_ANTES_DE_ANIMAR_MS sin que juegue,
          su Yoshi hace la animacion "esperar" hasta que haga clic.
        - Audio (con gui/sonido.py, si con_sonido=True): la musica arranca en bucle
          con cada partida nueva y se apaga cuando aterriza la ultima jugada; el
          sonido de la moneda suena justo cuando el Yoshi cae sobre ella.
        - Resaltar las casillas a las que puede saltar el humano en su turno (y con
          mas fuerza la que esta bajo el mouse, si se pasa casilla_hover). Mientras
          hay un salto en curso no resalta nada.
        - Resaltar la ultima jugada de la maquina.
        - Convertir una posicion en pixeles a una casilla (fila, columna) o None.
    NO hace:
        - No decide si una jugada es valida (recibe la lista ya calculada).
        - No lee eventos: eso es gui/ventana_juego.py.
Importa de:    pygame, constantes, modelo/estado.py, juego/reglas.py, gui/estilo.py,
               gui/cargador_sprites.py, gui/sonido.py.
Lo importan:   gui/ventana_juego.py.
Contrato:
    - PanelTablero(rect, con_sonido=True)
          rect: zona de la ventana para el tablero (p. ej. estilo.RECT_TABLERO). El
          tablero se centra en ella y el tamano de casilla sale de su lado menor.
          con_sonido: False para un tablero mudo (pruebas, vistas previas).
    - PanelTablero.dibujar(superficie, estado, resaltadas=(), ultima_jugada=None,
                           casilla_hover=None) -> None
          Llamarlo en CADA cuadro del bucle (30-60 fps) con el estado actual: asi
          avanzan las animaciones.
          resaltadas:    casillas a resaltar (Partida.movimientos_humano()).
          ultima_jugada: la casilla destino de la maquina, o el par (origen, destino).
          casilla_hover: casilla bajo el mouse (opcional, de casilla_en).
    - PanelTablero.animando() -> bool
          True mientras un Yoshi esta saltando (o hay saltos en cola). ventana_juego
          deberia esperar a que sea False antes de pedirle la jugada a la maquina y
          antes de aceptar clics del humano.
    - PanelTablero.reiniciar() -> None
          Olvida el estado anterior: el siguiente dibujar() pone todo en su sitio sin
          animar (usarlo al empezar una partida nueva; igual se detecta solo).
    - PanelTablero.casilla_en(posicion_pixel) -> Casilla | None
    - PanelTablero.rect_casilla(casilla) -> pygame.Rect
    - PanelTablero.tamano_casilla, PanelTablero.rect_tablero
Como detecta las jugadas:
    Guarda la ultima posicion "final" de cada Yoshi. Si en el nuevo Estado un Yoshi
    esta a un salto de caballo de donde estaba, y las monedas que faltan son
    justamente las de las casillas de destino, encola el salto. Si llegan dos jugadas
    juntas (humano y maquina en el mismo cuadro) las encola en orden de turno. Si el
    cambio no se explica con saltos (partida nueva), pone todo en su sitio sin animar.
"""
from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass

import pygame

from .. import constantes
from ..juego import reglas
from ..modelo.estado import Casilla, Estado
from . import estilo, sonido
from .cargador_sprites import (ANIMACION_CELEBRAR, ANIMACION_ESPERAR, DIRECCIONES,
                               cargar_animaciones, cargar_animaciones_yoshi, cargar_sprites)

GROSOR_MARCO = 12
MS_POR_CUADRO_MONEDA = 55       # 30 cuadros -> una vuelta cada ~1.6 s
MS_POR_CUADRO_TOMA = 60         # animacion "get" de la moneda
MS_POR_CUADRO_CAMINAR = 65      # ciclo de caminar del Yoshi durante el salto
DURACION_SALTO_MS = 560
ALTURA_SALTO = 0.7              # en casillas, en la mitad del salto
DURACION_PUNTOS_MS = 900        # cuanto dura el "+3" flotando
MS_POR_CUADRO_CELEBRAR = 150    # brazos arriba del ganador
PERIODO_BRINCO_MS = 600         # el ganador da brinquitos mientras celebra
ALTURA_BRINCO = 0.18            # en casillas
ESPERA_ANTES_DE_ANIMAR_MS = 4000  # si el humano no juega en este tiempo, su Yoshi "espera"
MS_POR_CUADRO_ESPERAR = 170


@dataclass
class _Salto:
    jugador: str
    origen: Casilla
    destino: Casilla
    moneda: tuple[Casilla, int] | None
    inicio: int = 0


def direccion_hacia(desde: Casilla, hacia: Casilla) -> str:
    """Cual de las 8 DIRECCIONES apunta mejor de `desde` a `hacia`."""
    df = hacia[0] - desde[0]
    dc = hacia[1] - desde[1]
    if df == 0 and dc == 0:
        return "abajo"
    angulo = math.degrees(math.atan2(-df, dc))  # las filas crecen hacia abajo
    return DIRECCIONES[round(angulo / 45) % 8]


def _es_salto_de_caballo(origen: Casilla, destino: Casilla) -> bool:
    return sorted((abs(destino[0] - origen[0]), abs(destino[1] - origen[1]))) == [1, 2]


class PanelTablero:
    def __init__(self, rect, con_sonido: bool = True) -> None:
        self.rect = pygame.Rect(rect)
        self._con_sonido = con_sonido
        self._musica_sonando = False
        n = constantes.TAMANO_TABLERO
        lado_disponible = min(self.rect.width, self.rect.height) - 2 * GROSOR_MARCO
        self.tamano_casilla = max(8, lado_disponible // n)
        lado = self.tamano_casilla * n
        self.rect_tablero = pygame.Rect(0, 0, lado, lado)
        self.rect_tablero.center = self.rect.center

        self.sprites = cargar_sprites(self.tamano_casilla)
        self.animaciones = cargar_animaciones(self.tamano_casilla)
        caminar = cargar_animaciones_yoshi(self.tamano_casilla)
        self._caminar = {constantes.VERDE: caminar["yoshi_verde"],
                         constantes.ROJO: caminar["yoshi_rojo"]}
        self._esperar = {
            jugador: {"derecha": ciclos[ANIMACION_ESPERAR],
                      "izquierda": [pygame.transform.flip(c, True, False)
                                    for c in ciclos[ANIMACION_ESPERAR]]}
            for jugador, ciclos in self._caminar.items()
        }
        self._color_jugador = {constantes.VERDE: estilo.COLOR_VERDE,
                               constantes.ROJO: estilo.COLOR_ROJO}
        self._especiales = set(constantes.CASILLAS_ESPECIALES)
        self._capa = pygame.Surface((self.tamano_casilla, self.tamano_casilla),
                                    pygame.SRCALPHA)
        self._fuente_puntos = estilo.fuente(estilo.FAMILIA_TITULO, "regular",
                                            max(14, self.tamano_casilla * 2 // 5))
        self.reiniciar()

    # ------------------------------------------------------------ geometria
    def rect_casilla(self, casilla: Casilla) -> pygame.Rect:
        """Rectangulo en pixeles de la casilla (fila, columna)."""
        fila, columna = casilla
        t = self.tamano_casilla
        return pygame.Rect(self.rect_tablero.left + columna * t,
                           self.rect_tablero.top + fila * t, t, t)

    def casilla_en(self, posicion_pixel) -> Casilla | None:
        """Casilla bajo `posicion_pixel` (x, y), o None si cae fuera del tablero."""
        x, y = posicion_pixel
        if not self.rect_tablero.collidepoint(x, y):
            return None
        t = self.tamano_casilla
        return ((y - self.rect_tablero.top) // t, (x - self.rect_tablero.left) // t)

    def _pie(self, casilla: Casilla) -> tuple[float, float]:
        """Punto (x, y) donde van los pies de un Yoshi parado en `casilla`."""
        rect = self.rect_casilla(casilla)
        return rect.centerx, rect.bottom - max(4, self.tamano_casilla // 9)

    # ------------------------------------------------------------ animaciones
    def reiniciar(self) -> None:
        """El proximo dibujar() coloca todo sin animar."""
        self._ultimo_estado: Estado | None = None
        self._vista_pos: dict[str, Casilla] = {}      # donde se dibuja cada Yoshi
        self._vista_monedas: dict[Casilla, int] = {}  # monedas que se dibujan
        self._pos_final: dict[str, Casilla] = {}      # donde queda tras la cola
        self._monedas_final: dict[Casilla, int] = {}
        self._cola: deque[_Salto] = deque()
        self._salto: _Salto | None = None
        self._tomas: list[tuple[Casilla, int, int]] = []  # (casilla, valor, inicio)
        self._celebra: str | None = None          # jugador que gano (si ya termino)
        self._celebra_desde = 0
        self._quieto_desde = 0                    # ultimo cambio de estado o aterrizaje
        self._esperando = False                   # el Yoshi del humano hace "esperar"

    def animando(self) -> bool:
        """True mientras un Yoshi esta saltando o hay saltos en cola."""
        return self._salto is not None or bool(self._cola)

    def _sincronizar(self, estado: Estado) -> bool:
        """Compara el estado nuevo con el anterior y encola los saltos que haya.

        Retorna True si el estado cambio.
        """
        if self._ultimo_estado is not None and estado == self._ultimo_estado:
            return False
        posiciones = {constantes.VERDE: estado.pos_verde, constantes.ROJO: estado.pos_rojo}
        monedas = dict(estado.monedas)
        saltos = None
        if self._ultimo_estado is not None:
            saltos = self._saltos_entre(posiciones, monedas)
        if saltos is None:
            # Partida nueva (o cambio que no se explica con saltos): todo en su sitio.
            self._cola.clear()
            self._salto = None
            self._tomas.clear()
            self._vista_pos = dict(posiciones)
            self._vista_monedas = dict(monedas)
            if self._con_sonido and not reglas.es_terminal(estado):
                self._musica_sonando = sonido.reproducir_musica()
        else:
            self._cola.extend(saltos)
        self._pos_final = posiciones
        self._monedas_final = monedas
        self._ultimo_estado = estado
        return True

    def _saltos_entre(self, posiciones, monedas) -> list[_Salto] | None:
        """Saltos que llevan de la posicion final anterior a la nueva, o None."""
        if not set(monedas) <= set(self._monedas_final):
            return None  # aparecieron monedas: es otra partida
        primero = self._ultimo_estado.turno
        orden = (primero, Estado.rival(primero))
        quitadas = set(self._monedas_final) - set(monedas)
        saltos = []
        for jugador in orden:
            origen, destino = self._pos_final[jugador], posiciones[jugador]
            if origen == destino:
                continue
            if not _es_salto_de_caballo(origen, destino):
                return None
            moneda = None
            if destino in quitadas:
                moneda = (destino, self._monedas_final[destino])
                quitadas.discard(destino)
            saltos.append(_Salto(jugador, origen, destino, moneda))
        return None if quitadas else saltos

    def _avanzar(self, ahora: int) -> None:
        """Termina los saltos que ya acabaron y empieza el siguiente de la cola."""
        while True:
            if self._salto is None:
                if not self._cola:
                    break
                self._salto = self._cola.popleft()
                self._salto.inicio = ahora
            fin = self._salto.inicio + DURACION_SALTO_MS
            if ahora < fin:
                break
            salto = self._salto
            self._vista_pos[salto.jugador] = salto.destino
            if salto.moneda is not None:
                casilla, valor = salto.moneda
                self._vista_monedas.pop(casilla, None)
                self._tomas.append((casilla, valor, fin))
                if self._con_sonido:
                    sonido.sonar_moneda()
            self._salto = None
            if self._cola:
                self._salto = self._cola.popleft()
                self._salto.inicio = fin
        self._tomas = [t for t in self._tomas if ahora - t[2] < DURACION_PUNTOS_MS]

    def _actualizar_celebracion(self, estado: Estado, ahora: int) -> None:
        """Cuando la partida termina (y ya aterrizo el ultimo salto) celebra el ganador.

        En empate nadie celebra.
        """
        ganador = None
        if not self.animando() and reglas.es_terminal(estado):
            ganador = reglas.ganador(estado)
            if ganador not in (constantes.VERDE, constantes.ROJO):
                ganador = None
        if ganador != self._celebra:
            self._celebra = ganador
            self._celebra_desde = ahora
        # La musica suena hasta el final: se apaga cuando aterriza la ultima jugada.
        if self._musica_sonando and not self.animando() and reglas.es_terminal(estado):
            sonido.detener_musica()
            self._musica_sonando = False

    # ------------------------------------------------------------ dibujo
    def dibujar(self, superficie, estado: Estado, resaltadas=(), ultima_jugada=None,
                casilla_hover=None) -> None:
        ahora = pygame.time.get_ticks()
        cambio = self._sincronizar(estado)
        self._avanzar(ahora)
        self._actualizar_celebracion(estado, ahora)
        # Espera del humano: cuenta desde el ultimo cambio o el ultimo aterrizaje.
        if cambio or self.animando():
            self._quieto_desde = ahora
        self._esperando = (not self.animando() and not reglas.es_terminal(estado)
                           and estado.turno == constantes.JUGADOR_HUMANO
                           and ahora - self._quieto_desde >= ESPERA_ANTES_DE_ANIMAR_MS)

        self._dibujar_marco(superficie)
        self._dibujar_casillas(superficie)

        origen, destino = self._separar_ultima_jugada(ultima_jugada)
        if origen is not None:
            self._marcar(superficie, origen, estilo.COLOR_ULTIMA_JUGADA, relleno=45, borde=2)
        if destino is not None:
            self._marcar(superficie, destino, estilo.COLOR_ULTIMA_JUGADA, relleno=90, borde=3)

        resaltadas = [] if self.animando() else list(resaltadas)
        for casilla in resaltadas:
            intenso = casilla == casilla_hover
            self._marcar(superficie, casilla, estilo.COLOR_RESALTE,
                         relleno=130 if intenso else 70, borde=3 if intenso else 2)

        self._dibujar_monedas(superficie, ahora)

        # Punto guia en las casillas vacias resaltadas (como en apps de ajedrez).
        for casilla in resaltadas:
            if casilla not in self._vista_monedas:
                centro = self.rect_casilla(casilla).center
                radio = max(3, self.tamano_casilla // 9)
                pygame.draw.circle(superficie, estilo.COLOR_SOMBRA,
                                   (centro[0] + 1, centro[1] + 2), radio)
                pygame.draw.circle(superficie, estilo.COLOR_RESALTE, centro, radio)

        self._dibujar_yoshis(superficie, ahora)
        self._dibujar_tomas(superficie, ahora)

    # ------------------------------------------------------------ partes
    def _dibujar_marco(self, superficie) -> None:
        marco = self.rect_tablero.inflate(2 * GROSOR_MARCO, 2 * GROSOR_MARCO)
        pygame.draw.rect(superficie, estilo.COLOR_SOMBRA, marco.move(5, 6), border_radius=10)
        pygame.draw.rect(superficie, estilo.COLOR_MARCO, marco, border_radius=10)
        pygame.draw.rect(superficie, estilo.COLOR_MARCO_CLARO, marco, width=3,
                         border_radius=10)
        pygame.draw.rect(superficie, estilo.COLOR_MARCO_OSCURO,
                         self.rect_tablero.inflate(6, 6), width=3)

    def _dibujar_casillas(self, superficie) -> None:
        n = constantes.TAMANO_TABLERO
        for fila in range(n):
            for columna in range(n):
                clara = (fila + columna) % 2 == 0
                if (fila, columna) in self._especiales:
                    clave = "casilla_especial_clara" if clara else "casilla_especial_oscura"
                else:
                    clave = "casilla_clara" if clara else "casilla_oscura"
                superficie.blit(self.sprites[clave], self.rect_casilla((fila, columna)))

    def _marcar(self, superficie, casilla: Casilla, color, relleno: int, borde: int) -> None:
        """Velo semitransparente + borde sobre una casilla."""
        self._capa.fill((*color, relleno))
        rect = self.rect_casilla(casilla)
        superficie.blit(self._capa, rect)
        pygame.draw.rect(superficie, color, rect.inflate(-borde, -borde), width=borde)

    def _dibujar_monedas(self, superficie, ahora: int) -> None:
        for casilla, valor in self._vista_monedas.items():
            clave = ("moneda_especial" if valor == constantes.VALOR_MONEDA_ESPECIAL
                     else "moneda_normal")
            cuadros = self.animaciones[clave]
            cuadro = cuadros[(ahora // MS_POR_CUADRO_MONEDA) % len(cuadros)]
            rect = self.rect_casilla(casilla)
            # Sombra eliptica para que la moneda "flote" sobre el pasto.
            ancho_sombra = int(cuadro.get_height() * 0.7)
            sombra = pygame.Rect(0, 0, ancho_sombra, max(3, ancho_sombra // 4))
            sombra.center = (rect.centerx, rect.centery + cuadro.get_height() // 2 + 2)
            self._elipse_translucida(superficie, sombra, (*estilo.COLOR_SOMBRA, 70))
            superficie.blit(cuadro, cuadro.get_rect(center=rect.center))

    def _dibujar_yoshis(self, superficie, ahora: int) -> None:
        dibujos = []  # (y de los pies, jugador, x, y, altura, cuadro)
        for jugador in (constantes.VERDE, constantes.ROJO):
            rival = Estado.rival(jugador)
            if self._salto is not None and self._salto.jugador == jugador:
                salto = self._salto
                transcurrido = max(0, ahora - salto.inicio)
                p = min(1.0, transcurrido / DURACION_SALTO_MS)
                (x0, y0), (x1, y1) = self._pie(salto.origen), self._pie(salto.destino)
                x, y = x0 + (x1 - x0) * p, y0 + (y1 - y0) * p
                altura = ALTURA_SALTO * self.tamano_casilla * 4 * p * (1 - p)
                cuadros = self._caminar[jugador][direccion_hacia(salto.origen, salto.destino)]
                cuadro = cuadros[(transcurrido // MS_POR_CUADRO_CAMINAR) % len(cuadros)]
            elif jugador == self._celebra:
                # Ganador: levanta los brazos y da brinquitos.
                x, y = self._pie(self._vista_pos[jugador])
                transcurrido = ahora - self._celebra_desde
                fase = (transcurrido % PERIODO_BRINCO_MS) / PERIODO_BRINCO_MS
                altura = ALTURA_BRINCO * self.tamano_casilla * math.sin(math.pi * fase)
                cuadros = self._caminar[jugador][ANIMACION_CELEBRAR]
                cuadro = cuadros[(transcurrido // MS_POR_CUADRO_CELEBRAR) % len(cuadros)]
            elif self._esperando and jugador == constantes.JUGADOR_HUMANO:
                # El humano tarda: su Yoshi se pone a esperar (mirando hacia el rival).
                casilla = self._vista_pos[jugador]
                x, y = self._pie(casilla)
                altura = 0.0
                lado = ("izquierda" if self._vista_pos[rival][1] < casilla[1]
                        else "derecha")
                cuadros = self._esperar[jugador][lado]
                transcurrido = ahora - self._quieto_desde - ESPERA_ANTES_DE_ANIMAR_MS
                cuadro = cuadros[(transcurrido // MS_POR_CUADRO_ESPERAR) % len(cuadros)]
            else:
                casilla = self._vista_pos[jugador]
                x, y = self._pie(casilla)
                altura = 0.0
                mira = direccion_hacia(casilla, self._vista_pos[rival])
                cuadro = self._caminar[jugador][mira][0]
            dibujos.append((y, jugador, x, y, altura, cuadro))

        # El que esta mas abajo en pantalla se dibuja encima.
        for _, jugador, x, y, altura, cuadro in sorted(dibujos, key=lambda d: d[0]):
            self._dibujar_sombra_yoshi(superficie, jugador, x, y, altura)
            superficie.blit(cuadro, cuadro.get_rect(midbottom=(round(x), round(y - altura))))

    def _dibujar_sombra_yoshi(self, superficie, jugador, x, y, altura) -> None:
        """Elipse del color del jugador bajo los pies; se achica cuando salta."""
        escala = 1 - 0.45 * min(1.0, altura / max(1, ALTURA_SALTO * self.tamano_casilla))
        ancho = int(self.tamano_casilla * 0.62 * escala)
        base = pygame.Rect(0, 0, ancho, max(4, ancho // 3))
        base.center = (round(x), round(y))
        color = self._color_jugador[jugador]
        self._elipse_translucida(superficie, base, (*color, int(150 * escala)))
        pygame.draw.ellipse(superficie, color, base, width=2)

    def _dibujar_tomas(self, superficie, ahora: int) -> None:
        """Moneda recogida: animacion "get" y el puntaje subiendo y desvaneciendose."""
        # La moneda y el puntaje salen por encima de la cabeza del Yoshi, sin taparlo.
        alto_yoshi = self._caminar[constantes.VERDE]["abajo"][0].get_height()
        for casilla, valor, inicio in self._tomas:
            transcurrido = ahora - inicio
            if transcurrido < 0:
                continue
            x, pie_y = self._pie(casilla)
            cabeza_y = round(pie_y) - alto_yoshi
            clave = ("moneda_especial_toma" if valor == constantes.VALOR_MONEDA_ESPECIAL
                     else "moneda_normal_toma")
            cuadros = self.animaciones.get(clave) or []
            indice = transcurrido // MS_POR_CUADRO_TOMA
            if indice < len(cuadros):
                cuadro = cuadros[indice]
                superficie.blit(cuadro, cuadro.get_rect(midbottom=(round(x), cabeza_y - 2)))
            # El "+3" arranca encima de la moneda (fijo, para que no salte al terminar).
            tope = cabeza_y - 2 - max((c.get_height() for c in cuadros), default=0)

            p = min(1.0, transcurrido / DURACION_PUNTOS_MS)
            texto = self._fuente_puntos.render(f"+{valor}", True, estilo.COLOR_DORADO)
            sombra = self._fuente_puntos.render(f"+{valor}", True, estilo.COLOR_SOMBRA)
            alfa = int(255 * (1 - p * p))
            texto.set_alpha(alfa)
            sombra.set_alpha(alfa)
            centro = (round(x), tope - texto.get_height() // 2
                      - int(p * self.tamano_casilla * 0.6))
            superficie.blit(sombra, sombra.get_rect(center=(centro[0] + 2, centro[1] + 2)))
            superficie.blit(texto, texto.get_rect(center=centro))

    @staticmethod
    def _elipse_translucida(superficie, rect: pygame.Rect, color_rgba) -> None:
        if rect.width <= 0 or rect.height <= 0:
            return
        capa = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(capa, color_rgba, capa.get_rect())
        superficie.blit(capa, rect)

    @staticmethod
    def _separar_ultima_jugada(ultima_jugada):
        """Acepta una casilla destino o el par (origen, destino)."""
        if ultima_jugada is None:
            return None, None
        if (len(ultima_jugada) == 2 and isinstance(ultima_jugada[0], tuple)
                and isinstance(ultima_jugada[1], tuple)):
            return ultima_jugada[0], ultima_jugada[1]
        return None, tuple(ultima_jugada)
