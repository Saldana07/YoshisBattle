"""
Archivo:       src/yoshis_battle/gui/cargador_sprites.py
Objetivo:      Ser el unico archivo del proyecto que conoce la carpeta assets/sprites/ y
               entregar las imagenes por nombre al resto de la GUI.
Responsabilidad:
    SI hace:
        - Cargar una vez los sprites: Yoshi verde, Yoshi rojo, moneda normal, moneda
          especial y casillas del tablero (ver assets/README.md).
        - Recortar de la hoja de Yoshi los ciclos de caminar en 4 direcciones (abajo,
          abajo-derecha, derecha, arriba) y completar las 8: arriba-derecha usa el
          perfil (la hoja no la trae) y las de la izquierda se sacan reflejando.
        - Recortar la animacion de celebracion (brazos arriba) para el ganador y la de
          espera (de espaldas moviendo las manos) para cuando el humano tarda en jugar.
        - Sacar el Yoshi rojo recoloreando el verde: el mapa de colores se arma
          comparando pixel a pixel los dos Yoshis de la fila "Palettes" de la hoja
          (misma pose, distinto color).
        - Cargar las animaciones de las monedas: "idle" (girando, 30 cuadros) y "get"
          (al recogerla, 8 cuadros), recortadas al area donde de verdad hay moneda.
        - Escalarlos sin suavizar (pygame.transform.scale con factor entero), igual que
          en AgroBot.
        - Si falta un sprite, devolver un reemplazo dibujado (circulo o casilla de
          color) para que el juego no se caiga.
        - Dar la ruta de la fuente de titulos (assets/sprites/font/SuperMario256.ttf)
          a gui/estilo.py.
        - Dar las rutas de la musica y del sonido de la moneda (assets/sonidos/) a
          gui/sonido.py.
    NO hace:
        - No dibuja el tablero ni decide que cuadro mostrar: eso es gui/panel_tablero.py.
Importa de:    pygame (pygame-ce).
Lo importan:   gui/estilo.py, gui/panel_tablero.py, gui/panel_marcador.py,
               gui/pantalla_inicio.py, gui/pantalla_final.py.
Contrato:
    - CARPETA_SPRITES: Path a assets/sprites/.
    - DIRECCIONES: las 8 direcciones, cada 45 grados empezando en "derecha" (0 grados)
      y girando en sentido antihorario: derecha, arriba_derecha, arriba, ...
    - cargar_sprites(tamano_casilla) -> dict[str, pygame.Surface]
          Claves: "yoshi_verde", "yoshi_rojo", "moneda_normal", "moneda_especial",
          "casilla_clara", "casilla_oscura", "casilla_especial_clara",
          "casilla_especial_oscura".
          Los Yoshis quietos miran hacia abajo-derecha.
    - cargar_animaciones(tamano_casilla) -> dict[str, list[pygame.Surface]]
          Claves: "moneda_normal", "moneda_especial" (girando) y
          "moneda_normal_toma", "moneda_especial_toma" (al recogerla).
    - cargar_animaciones_yoshi(tamano_casilla) -> dict[str, dict[str, list[Surface]]]
          {"yoshi_verde": {nombre: [cuadros]}, "yoshi_rojo": {...}}, con las 8
          DIRECCIONES, ANIMACION_CELEBRAR ("celebrar") y ANIMACION_ESPERAR ("esperar").
          Todos los cuadros comparten la linea de los pies: se dibujan con ancla
          midbottom.
    - ruta_fuente_titulo() -> Path | None
    - ruta_musica() -> Path | None          (musica*, music*, *theme*, *bgm*... o, si
                                              no, cualquier otro audio de sonidos/)
    - ruta_sonido_moneda() -> Path | None   (moneda*, *coin*)
          Se buscan primero en assets/sonidos/ y luego en assets/, con extension
          .ogg, .mp3, .wav, .flac u .opus.
Orden de busqueda de cada sprite:
    1. El archivo "limpio" que pide assets/README.md (p. ej. yoshi/yoshi_verde.png).
    2. Los assets que tiene hoy el repo (hoja de Yoshis y carpetas Coin (Large/Small)).
    3. Un reemplazo dibujado.
Notas:
    - Los resultados se guardan en memoria por tamano: llamar varias veces a
      cargar_sprites(56) no vuelve a leer el disco.
    - Si ya hay ventana (pygame.display.set_mode) se usa convert_alpha() para que
      dibujar sea mas rapido; sin ventana (pruebas) se dejan como estan.
"""
from __future__ import annotations

import random
import re
from pathlib import Path

import pygame

CARPETA_ASSETS = Path(__file__).resolve().parents[3] / "assets"
CARPETA_SPRITES = CARPETA_ASSETS / "sprites"
CARPETA_YOSHI = CARPETA_SPRITES / "yoshi"
CARPETA_MONEDA = CARPETA_SPRITES / "moneda"
CARPETA_TABLERO = CARPETA_SPRITES / "tablero"
CARPETA_FUENTE = CARPETA_SPRITES / "font"
CARPETA_SONIDOS = CARPETA_ASSETS / "sonidos"

# ---------------------------------------------------------------- sonidos
EXTENSIONES_AUDIO = (".ogg", ".mp3", ".wav", ".flac", ".opus")
# Nombres que se buscan (en assets/sonidos/ y luego en assets/), en este orden.
PATRONES_MUSICA = ("musica*", "music*", "*theme*", "*bgm*", "*soundtrack*")
PATRONES_MONEDA = ("moneda*", "*coin*")

DIRECCIONES = ("derecha", "arriba_derecha", "arriba", "arriba_izquierda",
               "izquierda", "abajo_izquierda", "abajo", "abajo_derecha")

# ---------------------------------------------------------------- Yoshis
# Hoja de sprites de Mario & Luigi: Partners in Time (ripeada por A.J. Nitro).
HOJA_YOSHI = ("DS _ DSi - Mario & Luigi_ Partners in Time - "
              "Non-Playable Characters - Yoshi.png")
COLOR_FONDO_HOJA = (165, 235, 255)
# (x, y, ancho, alto) dentro de la hoja: fila "Palettes", misma pose en todos los colores.
RECORTES_YOSHI = {
    "yoshi_verde": (4, 422, 24, 39),
    "yoshi_rojo": (120, 422, 24, 39),
}
# Ciclos de caminar del Yoshi verde: direccion -> (y, alto, [(x, ancho), ...]).
# Las direcciones hacia la izquierda se sacan reflejando las de la derecha.
ALTO_FILA_CAMINAR = 38
FILAS_CAMINAR = {
    "abajo": (4, ALTO_FILA_CAMINAR,
              [(4, 18), (27, 17), (49, 18), (72, 17), (94, 18), (117, 17), (139, 18),
               (162, 17)]),
    "abajo_derecha": (48, ALTO_FILA_CAMINAR,
                      [(4, 24), (33, 23), (61, 24), (90, 23), (118, 24), (147, 23),
                       (175, 24), (204, 23)]),
    "arriba": (92, ALTO_FILA_CAMINAR,
               [(4, 18), (27, 17), (49, 16), (70, 17), (92, 18), (115, 17), (137, 16),
                (158, 17)]),
    "derecha": (183, ALTO_FILA_CAMINAR,
                [(4, 24), (33, 23), (61, 23), (89, 23), (117, 24), (146, 23), (174, 22),
                 (201, 23)]),
}
# La hoja no trae caminar hacia arriba-derecha: se usa el perfil (derecha).
SUSTITUTOS = {"arriba_derecha": "derecha"}
ESPEJOS = {"izquierda": "derecha", "arriba_izquierda": "arriba_derecha",
           "abajo_izquierda": "abajo_derecha"}
# Celebracion (brazos arriba, boca abierta): los 4 primeros de la fila donde Yoshi
# tambien aparece acostado (y = 228). La usa el ganador.
FILA_CELEBRAR = (228, 41, [(4, 28), (37, 28), (70, 28), (103, 28)])
ANIMACION_CELEBRAR = "celebrar"
# Esperando (de espaldas, moviendo las manos): los 4 ultimos sprites de la fila de
# caminar a la derecha (y = 183). La usa el Yoshi del humano cuando tarda en jugar.
FILA_ESPERAR = (183, ALTO_FILA_CAMINAR, [(244, 22), (271, 22), (298, 22), (325, 22)])
ANIMACION_ESPERAR = "esperar"
# Que fraccion del alto de la casilla puede ocupar un Yoshi.
FRACCION_YOSHI = 0.96

# ---------------------------------------------------------------- monedas
# clave -> (carpeta, nombre base de los cuadros, fraccion de la casilla que ocupa)
MONEDAS = {
    "moneda_especial": (CARPETA_MONEDA / "Coin (Large)", "coin_large_", 0.84),
    "moneda_normal": (CARPETA_MONEDA / "Coin (Small)", "coin_small_", 0.64),
}

# ---------------------------------------------------------------- reemplazos
_COLOR_REEMPLAZO = {
    "yoshi_verde": ((92, 200, 78), (30, 80, 30)),
    "yoshi_rojo": ((236, 76, 66), (110, 24, 24)),
    "moneda_normal": ((255, 208, 64), (150, 100, 20)),
    "moneda_especial": ((255, 236, 120), (190, 120, 20)),
}
_COLORES_CASILLA = {
    # clave -> (base, mas oscuro, mas claro)
    "casilla_clara": ((148, 208, 96), (128, 192, 84), (170, 222, 116)),
    "casilla_oscura": ((100, 172, 74), (86, 154, 64), (118, 188, 88)),
    "casilla_especial_clara": ((246, 214, 124), (228, 192, 104), (252, 228, 152)),
    "casilla_especial_oscura": ((226, 186, 92), (206, 164, 76), (240, 204, 118)),
}

_cache: dict[tuple[str, int], object] = {}


# ================================================================ utilidades
def _preparar(imagen: pygame.Surface) -> pygame.Surface:
    """convert_alpha() si ya existe la ventana (mas rapido al dibujar)."""
    if pygame.display.get_init() and pygame.display.get_surface() is not None:
        return imagen.convert_alpha()
    return imagen


def _cargar_png(ruta: Path) -> pygame.Surface | None:
    """Imagen en `ruta`, o None si no existe o no se puede leer."""
    if not ruta.is_file():
        return None
    try:
        return pygame.image.load(str(ruta))
    except (pygame.error, OSError):
        return None


def _factor_entero(ancho: int, alto: int, ancho_max: int, alto_max: int) -> float:
    """Mayor factor entero que cabe; si ni el 1 cabe, la fraccion necesaria."""
    factor = min(ancho_max // ancho, alto_max // alto)
    if factor >= 1:
        return factor
    return min(ancho_max / ancho, alto_max / alto)


def _escalar(imagen: pygame.Surface, factor: float) -> pygame.Surface:
    if factor == 1:
        return imagen.copy()
    ancho, alto = imagen.get_size()
    return pygame.transform.scale(
        imagen, (max(1, round(ancho * factor)), max(1, round(alto * factor))))


def _escalar_entero(imagen: pygame.Surface, ancho_max: int, alto_max: int) -> pygame.Surface:
    """Agranda `imagen` por el mayor factor entero que quepa en ancho_max x alto_max."""
    return _escalar(imagen, _factor_entero(*imagen.get_size(), ancho_max, alto_max))


def _limpiar_pixeles(imagen: pygame.Surface, fondo, mapa: dict | None = None) -> pygame.Surface:
    """Copia con el `fondo` transparente y, si hay `mapa`, los colores reemplazados."""
    resultado = pygame.Surface(imagen.get_size(), pygame.SRCALPHA)
    resultado.blit(imagen, (0, 0))
    fondo = tuple(fondo)
    ancho, alto = resultado.get_size()
    for x in range(ancho):
        for y in range(alto):
            color = tuple(resultado.get_at((x, y)))[:3]
            if color == fondo:
                resultado.set_at((x, y), (0, 0, 0, 0))
            elif mapa and color in mapa:
                resultado.set_at((x, y), mapa[color])
    return resultado


def _recorte(hoja: pygame.Surface, x: int, y: int, ancho: int, alto: int):
    """Pedazo de la hoja, o None si se sale de ella."""
    if x + ancho > hoja.get_width() or y + alto > hoja.get_height():
        return None
    return hoja.subsurface(pygame.Rect(x, y, ancho, alto)).copy()


def _glob_seguro(texto: str) -> str:
    """Escapa los corchetes para usar el nombre en Path.glob ('[idle]' es literal)."""
    return re.sub(r"([\[\]])", r"[\1]", texto)


def _numero_final(ruta: Path) -> int:
    """'[idle] coin_large_12.png' -> 12 (para ordenar los cuadros)."""
    encontrado = re.search(r"(\d+)$", ruta.stem)
    return int(encontrado.group(1)) if encontrado else 0


def _hoja_yoshi() -> pygame.Surface | None:
    clave = ("hoja_yoshi", 0)
    if clave not in _cache:
        _cache[clave] = _cargar_png(CARPETA_YOSHI / HOJA_YOSHI)
    return _cache[clave]


def _mapa_verde_a_rojo(hoja: pygame.Surface) -> dict:
    """color del Yoshi verde -> color del Yoshi rojo, leido de la fila "Palettes"."""
    verde = _recorte(hoja, *RECORTES_YOSHI["yoshi_verde"])
    rojo = _recorte(hoja, *RECORTES_YOSHI["yoshi_rojo"])
    if verde is None or rojo is None:
        return {}
    mapa = {}
    ancho, alto = verde.get_size()
    for x in range(ancho):
        for y in range(alto):
            a = tuple(verde.get_at((x, y)))[:3]
            b = tuple(rojo.get_at((x, y)))[:3]
            if a != COLOR_FONDO_HOJA and a != b:
                mapa.setdefault(a, b)
    return mapa


# ================================================================ reemplazos dibujados
def _circulo(lado: int, relleno, borde, fraccion: float) -> pygame.Surface:
    superficie = pygame.Surface((lado, lado), pygame.SRCALPHA)
    radio = max(3, int(lado * fraccion / 2))
    centro = (lado // 2, lado // 2)
    pygame.draw.circle(superficie, borde, centro, radio)
    pygame.draw.circle(superficie, relleno, centro, max(1, radio - max(2, lado // 24)))
    return superficie


def _casilla_dibujada(clave: str, lado: int) -> pygame.Surface:
    """Casilla de pasto (o arena, si es especial) con textura pixelada repetible."""
    base, oscuro, claro = _COLORES_CASILLA[clave]
    superficie = pygame.Surface((lado, lado))
    superficie.fill(base)
    pixel = max(2, lado // 16)
    rng = random.Random(clave)  # misma textura siempre
    for _ in range(14):
        x = rng.randrange(0, lado - pixel + 1, pixel)
        y = rng.randrange(0, lado - pixel + 1, pixel)
        color = oscuro if rng.random() < 0.6 else claro
        ancho = pixel * rng.choice((1, 2))
        superficie.fill(color, (x, y, ancho, pixel))
    # Biselado de medio "pixel" para que se note la cuadricula.
    borde = max(1, pixel // 2)
    superficie.fill(claro, (0, 0, lado, borde))
    superficie.fill(claro, (0, 0, borde, lado))
    superficie.fill(oscuro, (0, lado - borde, lado, borde))
    superficie.fill(oscuro, (lado - borde, 0, borde, lado))
    return superficie


# ================================================================ carga por tipo
def _sprite_yoshi(clave: str, lado: int) -> pygame.Surface:
    alto_max = int(lado * FRACCION_YOSHI)
    limpio = _cargar_png(CARPETA_YOSHI / f"{clave}.png")
    if limpio is not None:
        return _escalar_entero(limpio, lado, alto_max)

    hoja = _hoja_yoshi()
    if hoja is not None:
        recorte = _recorte(hoja, *RECORTES_YOSHI[clave])
        if recorte is not None:
            return _escalar_entero(_limpiar_pixeles(recorte, COLOR_FONDO_HOJA),
                                   lado, alto_max)

    relleno, borde = _COLOR_REEMPLAZO[clave]
    return _circulo(lado, relleno, borde, 0.7)


def _caminar_yoshi(clave: str, lado: int) -> dict[str, list[pygame.Surface]] | None:
    """Ciclos de caminar en las 8 direcciones, o None si no se pueden sacar de la hoja."""
    hoja = _hoja_yoshi()
    if hoja is None:
        return None
    mapa = _mapa_verde_a_rojo(hoja) if clave == "yoshi_rojo" else None
    if clave == "yoshi_rojo" and not mapa:
        return None
    factor = _factor_entero(24, ALTO_FILA_CAMINAR, lado, int(lado * FRACCION_YOSHI))

    filas = dict(FILAS_CAMINAR)
    filas[ANIMACION_CELEBRAR] = FILA_CELEBRAR
    filas[ANIMACION_ESPERAR] = FILA_ESPERAR
    ciclos: dict[str, list[pygame.Surface]] = {}
    for nombre, (y, alto, cuadros) in filas.items():
        lista = []
        for x, ancho in cuadros:
            recorte = _recorte(hoja, x, y, ancho, alto)
            if recorte is None:
                return None
            lista.append(_escalar(_limpiar_pixeles(recorte, COLOR_FONDO_HOJA, mapa), factor))
        ciclos[nombre] = lista
    for faltante, sustituto in SUSTITUTOS.items():
        ciclos[faltante] = ciclos[sustituto]
    for izquierda, derecha in ESPEJOS.items():
        ciclos[izquierda] = [pygame.transform.flip(c, True, False) for c in ciclos[derecha]]
    return ciclos


def _cuadros_moneda(clave: str, lado: int) -> tuple[list, list]:
    """(cuadros girando, cuadros al recogerla) de una moneda."""
    carpeta, base, fraccion = MONEDAS[clave]
    maximo = max(4, int(lado * fraccion))

    limpio = _cargar_png(CARPETA_MONEDA / f"{clave}.png")
    if limpio is not None:
        imagen = _escalar_entero(limpio, maximo, maximo)
        return [imagen], []

    def leer(prefijo: str) -> list[pygame.Surface]:
        rutas = sorted(carpeta.glob(f"{_glob_seguro(prefijo + base)}*.png"),
                       key=_numero_final)
        return [img for img in (_cargar_png(r) for r in rutas) if img is not None]

    girando, toma = leer("[idle] "), leer("[get] ")
    if girando:
        # Recorte comun a todos los cuadros (mismo tamano para que no "salten").
        area = girando[0].get_bounding_rect()
        for cuadro in girando[1:] + toma:
            if cuadro.get_size() == girando[0].get_size():
                area = area.union(cuadro.get_bounding_rect())
        if area.width > 0 and area.height > 0:
            factor = _factor_entero(area.width, area.height, maximo, maximo)
            recortar = lambda c: _escalar(c.subsurface(area).copy(), factor)  # noqa: E731
            return ([recortar(c) for c in girando],
                    [recortar(c) for c in toma if c.get_size() == girando[0].get_size()])

    relleno, borde = _COLOR_REEMPLAZO[clave]
    return [_circulo(lado, relleno, borde, fraccion)], []


def _casilla(clave: str, lado: int) -> pygame.Surface:
    imagen = _cargar_png(CARPETA_TABLERO / f"{clave}.png")
    if imagen is not None:
        return pygame.transform.scale(imagen, (lado, lado))
    return _casilla_dibujada(clave, lado)


# ================================================================ contrato
def cargar_animaciones(tamano_casilla: int) -> dict[str, list[pygame.Surface]]:
    """Cuadros de las monedas (girando y al recogerlas) para `tamano_casilla`."""
    clave_cache = ("animaciones", tamano_casilla)
    if clave_cache not in _cache:
        animaciones = {}
        for clave in MONEDAS:
            girando, toma = _cuadros_moneda(clave, tamano_casilla)
            animaciones[clave] = [_preparar(c) for c in girando]
            animaciones[f"{clave}_toma"] = [_preparar(c) for c in toma]
        _cache[clave_cache] = animaciones
    return _cache[clave_cache]


def cargar_animaciones_yoshi(tamano_casilla: int) -> dict[str, dict[str, list[pygame.Surface]]]:
    """Ciclos de caminar de cada Yoshi en las 8 DIRECCIONES, mas "celebrar" y "esperar"."""
    clave_cache = ("caminar", tamano_casilla)
    if clave_cache not in _cache:
        resultado = {}
        nombres = DIRECCIONES + (ANIMACION_CELEBRAR, ANIMACION_ESPERAR)
        for clave in RECORTES_YOSHI:
            ciclos = None
            if not (CARPETA_YOSHI / f"{clave}.png").is_file():
                ciclos = _caminar_yoshi(clave, tamano_casilla)
            if ciclos is None:
                # Sin hoja (o con sprite limpio): el mismo sprite en todas direcciones.
                quieto = cargar_sprites(tamano_casilla)[clave]
                reflejado = pygame.transform.flip(quieto, True, False)
                ciclos = {n: [reflejado if "izquierda" in n else quieto] for n in nombres}
            resultado[clave] = {n: [_preparar(c) for c in ciclos[n]] for n in nombres}
        _cache[clave_cache] = resultado
    return _cache[clave_cache]


def cargar_sprites(tamano_casilla: int) -> dict[str, pygame.Surface]:
    """Sprites del juego escalados a `tamano_casilla` pixeles."""
    clave_cache = ("sprites", tamano_casilla)
    if clave_cache not in _cache:
        animaciones = cargar_animaciones(tamano_casilla)
        sprites = {clave: _preparar(_sprite_yoshi(clave, tamano_casilla))
                   for clave in RECORTES_YOSHI}
        sprites["moneda_normal"] = animaciones["moneda_normal"][0]
        sprites["moneda_especial"] = animaciones["moneda_especial"][0]
        for clave in _COLORES_CASILLA:
            sprites[clave] = _preparar(_casilla(clave, tamano_casilla))
        _cache[clave_cache] = sprites
    return _cache[clave_cache]


def _buscar_audio(patrones) -> Path | None:
    for carpeta in (CARPETA_SONIDOS, CARPETA_ASSETS):
        if not carpeta.is_dir():
            continue
        for patron in patrones:
            for ruta in sorted(carpeta.glob(patron)):
                if ruta.is_file() and ruta.suffix.lower() in EXTENSIONES_AUDIO:
                    return ruta
    return None


def ruta_musica() -> Path | None:
    """Archivo de la musica de fondo, o None.

    Primero busca por nombre (musica*, music*, *theme*...). Si ninguno coincide, toma
    cualquier audio de assets/sonidos/ que no sea el de la moneda (asi sirve, por
    ejemplo, flower-garden-yoshis-island-1.mp3 sin renombrarlo).
    """
    ruta = _buscar_audio(PATRONES_MUSICA)
    if ruta is not None or not CARPETA_SONIDOS.is_dir():
        return ruta
    moneda = ruta_sonido_moneda()
    for candidata in sorted(CARPETA_SONIDOS.iterdir()):
        if (candidata.is_file() and candidata.suffix.lower() in EXTENSIONES_AUDIO
                and candidata != moneda):
            return candidata
    return None


def ruta_sonido_moneda() -> Path | None:
    """Archivo del sonido de recoger moneda (assets/sonidos/*coin*), o None."""
    return _buscar_audio(PATRONES_MONEDA)


def ruta_fuente_titulo() -> Path | None:
    """Archivo .ttf de la fuente de titulos, o None si no esta."""
    preferido = CARPETA_FUENTE / "SuperMario256.ttf"
    if preferido.is_file():
        return preferido
    candidatos = sorted(CARPETA_FUENTE.glob("*.ttf")) if CARPETA_FUENTE.is_dir() else []
    return candidatos[0] if candidatos else None
