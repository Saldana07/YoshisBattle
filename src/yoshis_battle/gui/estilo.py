"""
Archivo:       src/yoshis_battle/gui/estilo.py
Objetivo:      Reunir lo que comparten todas las pantallas: tamano de ventana, paleta de
               colores, tipografias y utilidades para dibujar texto y cajas.
Responsabilidad:
    SI hace:
        - Definir el tamano de la ventana y la paleta.
        - Cargar las tipografias Pixelify Sans y DM Sans desde gui/fuentes/ (ver el
          LEEME.md de esa carpeta) y la de titulos (Super Mario 256, que vive en
          assets/ y se pide a cargador_sprites). Si falta un archivo usa la fuente por
          defecto de pygame y el juego sigue.
        - Ofrecer utilidades de dibujo: texto con ancla (y sombra opcional), partir un
          texto en lineas y cajas redondeadas.
    NO hace:
        - No conoce ninguna pantalla ni la logica del juego.
        - No lee assets/ directamente: la ruta de la fuente de titulos la da
          gui/cargador_sprites.py.
Importa de:    pygame (pygame-ce), gui/cargador_sprites.py (ruta de la fuente de titulos).
Lo importan:   todos los demas archivos de gui/.
Contrato:
    - ANCHO_VENTANA, ALTO_VENTANA, TAMANO_VENTANA
    - COLOR_* (paleta)
    - FAMILIA_TITULO, FAMILIA_PIXEL, FAMILIA_TEXTO (nombres de familia)
    - fuente(familia, peso, tamano) -> pygame.font.Font
          familia: FAMILIA_TITULO | FAMILIA_PIXEL | FAMILIA_TEXTO
          peso:    "regular" | "medium" | "bold"  (tambien "400", "500", "700")
    - dibujar_texto(superficie, texto, fuente, color, posicion, ancla="topleft",
                    sombra=None) -> pygame.Rect
    - partir_en_lineas(texto, fuente, ancho_maximo) -> list[str]
    - dibujar_caja(superficie, rect, color, borde=None, grosor=2, radio=12) -> None
Uso tipico (para pantalla_inicio, ventana_juego y pantalla_final):
    titulo = estilo.fuente(estilo.FAMILIA_TITULO, "regular", 48)
    estilo.dibujar_texto(pantalla, "Yoshi's Battle", titulo, estilo.COLOR_DORADO,
                         (estilo.ANCHO_VENTANA // 2, 80), ancla="center",
                         sombra=estilo.COLOR_SOMBRA)
"""
from __future__ import annotations

from pathlib import Path

import pygame

from . import cargador_sprites

# ---------------------------------------------------------------- ventana
ANCHO_VENTANA = 1120
ALTO_VENTANA = 760
TAMANO_VENTANA = (ANCHO_VENTANA, ALTO_VENTANA)
TITULO_VENTANA = "Yoshi's Battle"

# Zonas sugeridas para la pantalla de juego (las usa ventana_juego.py).
# El tablero ocupa el 70 % de la zona izquierda (680 px -> 476 px) y va centrado en ella.
MARGEN = 40
ESCALA_TABLERO = 0.70
_ZONA_TABLERO = ALTO_VENTANA - 2 * MARGEN
LADO_TABLERO = round(_ZONA_TABLERO * ESCALA_TABLERO)
_INICIO_TABLERO = MARGEN + (_ZONA_TABLERO - LADO_TABLERO) // 2
RECT_TABLERO = (_INICIO_TABLERO, _INICIO_TABLERO, LADO_TABLERO, LADO_TABLERO)
RECT_MARCADOR = (ALTO_VENTANA, MARGEN, ANCHO_VENTANA - ALTO_VENTANA - MARGEN,
                 ALTO_VENTANA - 2 * MARGEN)

# ---------------------------------------------------------------- paleta
# Fondo nocturno azul (hace resaltar el pasto y las monedas) con acentos de Yoshi.
COLOR_FONDO = (28, 34, 58)
COLOR_FONDO_PANEL = (38, 47, 80)
COLOR_TARJETA = (48, 59, 98)
COLOR_BORDE = (78, 94, 142)
COLOR_SOMBRA = (12, 14, 26)

COLOR_TEXTO = (247, 242, 228)
COLOR_TEXTO_SUAVE = (172, 182, 214)

COLOR_VERDE = (92, 200, 78)        # Yoshi de la maquina
COLOR_VERDE_OSCURO = (46, 120, 50)
COLOR_ROJO = (236, 76, 66)         # Yoshi del humano
COLOR_ROJO_OSCURO = (150, 36, 36)
COLOR_DORADO = (255, 208, 64)      # monedas, titulos
COLOR_DORADO_OSCURO = (196, 136, 28)

# Tablero
COLOR_PASTO_CLARO = (148, 208, 96)
COLOR_PASTO_OSCURO = (100, 172, 74)
COLOR_ARENA_CLARA = (246, 214, 124)  # casillas especiales del centro
COLOR_ARENA_OSCURA = (226, 186, 92)
COLOR_MARCO = (122, 78, 44)
COLOR_MARCO_OSCURO = (78, 48, 26)
COLOR_MARCO_CLARO = (168, 116, 66)

# Resaltes sobre el tablero
COLOR_RESALTE = (255, 246, 160)    # casillas a las que puede saltar el humano
COLOR_ULTIMA_JUGADA = (255, 146, 54)  # ultima jugada de la maquina

# ---------------------------------------------------------------- tipografias
FAMILIA_TITULO = "Super Mario 256"
FAMILIA_PIXEL = "Pixelify Sans"
FAMILIA_TEXTO = "DM Sans"

CARPETA_FUENTES = Path(__file__).resolve().parent / "fuentes"

_ARCHIVOS_FUENTE = {
    (FAMILIA_PIXEL, "regular"): "PixelifySans-Medium.ttf",
    (FAMILIA_PIXEL, "medium"): "PixelifySans-Medium.ttf",
    (FAMILIA_PIXEL, "bold"): "PixelifySans-Bold.ttf",
    (FAMILIA_TEXTO, "regular"): "DMSans-Regular.ttf",
    (FAMILIA_TEXTO, "medium"): "DMSans-Medium.ttf",
    (FAMILIA_TEXTO, "bold"): "DMSans-Bold.ttf",
}

_PESOS = {
    "regular": "regular", "normal": "regular", "400": "regular",
    "medium": "medium", "500": "medium",
    "bold": "bold", "negrita": "bold", "700": "bold",
}

_cache_fuentes: dict[tuple[str, str, int], pygame.font.Font] = {}


def _ruta_fuente(familia: str, peso: str) -> Path | None:
    """Archivo .ttf para (familia, peso), o None si no esta disponible."""
    if familia == FAMILIA_TITULO:
        return cargador_sprites.ruta_fuente_titulo()
    candidatos = [peso, "medium", "regular", "bold"]
    for opcion in candidatos:
        nombre = _ARCHIVOS_FUENTE.get((familia, opcion))
        if nombre and (CARPETA_FUENTES / nombre).is_file():
            return CARPETA_FUENTES / nombre
    return None


def fuente(familia: str, peso: str, tamano: int) -> pygame.font.Font:
    """Fuente de gui/fuentes/ (o la de pygame si falta el archivo)."""
    peso = _PESOS.get(str(peso).lower(), "regular")
    clave = (familia, peso, tamano)
    if clave in _cache_fuentes:
        return _cache_fuentes[clave]
    if not pygame.font.get_init():
        pygame.font.init()

    ruta = _ruta_fuente(familia, peso)
    fuente_cargada = None
    if ruta is not None:
        try:
            fuente_cargada = pygame.font.Font(str(ruta), tamano)
        except (OSError, pygame.error):
            fuente_cargada = None
    if fuente_cargada is None:
        # Fuente por defecto de pygame: es algo mas pequena, por eso se agranda.
        fuente_cargada = pygame.font.Font(None, round(tamano * 1.3))
        fuente_cargada.set_bold(peso == "bold")
    _cache_fuentes[clave] = fuente_cargada
    return fuente_cargada


def dibujar_texto(superficie, texto: str, fuente_texto, color, posicion,
                  ancla: str = "topleft", sombra=None) -> pygame.Rect:
    """Dibuja `texto` anclado en `posicion` y retorna su rectangulo.

    `ancla` es cualquier atributo de pygame.Rect ("topleft", "center", "midright"...).
    Si `sombra` es un color, primero dibuja una copia desplazada 2 px (estilo arcade).
    """
    imagen = fuente_texto.render(str(texto), True, color)
    rect = imagen.get_rect(**{ancla: posicion})
    if sombra is not None:
        desplazamiento = max(2, fuente_texto.get_height() // 16)
        imagen_sombra = fuente_texto.render(str(texto), True, sombra)
        superficie.blit(imagen_sombra, rect.move(desplazamiento, desplazamiento))
    superficie.blit(imagen, rect)
    return rect


def partir_en_lineas(texto: str, fuente_texto, ancho_maximo: int) -> list[str]:
    """Parte `texto` en lineas que no pasen de `ancho_maximo` pixeles."""
    lineas: list[str] = []
    for parrafo in str(texto).split("\n"):
        actual = ""
        for palabra in parrafo.split(" "):
            prueba = palabra if not actual else f"{actual} {palabra}"
            if fuente_texto.size(prueba)[0] <= ancho_maximo or not actual:
                actual = prueba
            else:
                lineas.append(actual)
                actual = palabra
        lineas.append(actual)
    return lineas


def dibujar_caja(superficie, rect, color, borde=None, grosor: int = 2,
                 radio: int = 12) -> None:
    """Rectangulo redondeado relleno, con borde opcional."""
    pygame.draw.rect(superficie, color, rect, border_radius=radio)
    if borde is not None:
        pygame.draw.rect(superficie, borde, rect, width=grosor, border_radius=radio)
