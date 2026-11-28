"""
Archivo:       src/yoshis_battle/gui/sonido.py
Objetivo:      Reproducir el audio del juego: la musica de fondo en bucle y el efecto de
               recoger una moneda.
Responsabilidad:
    SI hace:
        - Iniciar pygame.mixer cuando se necesita. Si el equipo no tiene salida de
          audio, o falta un archivo, todo queda en silencio y el juego sigue.
        - Poner la musica en bucle (loops=-1) y detenerla con un desvanecido.
        - Sonar la moneda (el efecto se carga una sola vez y se reutiliza).
        - Silenciar / reactivar todo el audio.
    NO hace:
        - No decide cuando suena cada cosa: eso lo hace gui/panel_tablero.py (musica
          al empezar la partida, moneda al aterrizar, silencio al terminar).
        - No conoce la carpeta assets/: las rutas las da gui/cargador_sprites.py.
Importa de:    pygame (pygame-ce), gui/cargador_sprites.py.
Lo importan:   gui/panel_tablero.py, demo_interfaz.py (tecla M).
Contrato:
    - VOLUMEN_MUSICA, VOLUMEN_EFECTOS (0.0 a 1.0)
    - disponible() -> bool                 hay mixer funcionando
    - reproducir_musica() -> bool          True si encontro la musica y empezo a sonar
    - detener_musica(desvanecer_ms=1200) -> None
    - sonar_moneda() -> None
    - silenciado() -> bool
    - alternar_silencio() -> bool          retorna el nuevo estado (True = en silencio)
"""
from __future__ import annotations

import pygame

from . import cargador_sprites

VOLUMEN_MUSICA = 0.45
VOLUMEN_EFECTOS = 0.8

_estado = {
    "mixer": None,        # None = sin intentar, True/False = resultado de iniciar
    "silencio": False,
    "moneda": None,       # pygame.mixer.Sound, False si no se pudo cargar
}


def disponible() -> bool:
    """Inicia el mixer la primera vez; False si no hay audio en este equipo."""
    if _estado["mixer"] is None:
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            _estado["mixer"] = True
        except pygame.error:
            _estado["mixer"] = False
    return bool(_estado["mixer"]) and bool(pygame.mixer.get_init())


def reproducir_musica() -> bool:
    """Musica de fondo en bucle hasta que se llame detener_musica()."""
    if not disponible():
        return False
    ruta = cargador_sprites.ruta_musica()
    if ruta is None:
        return False
    try:
        pygame.mixer.music.load(str(ruta))
        pygame.mixer.music.set_volume(0.0 if _estado["silencio"] else VOLUMEN_MUSICA)
        pygame.mixer.music.play(loops=-1, fade_ms=600)
    except pygame.error:
        return False
    return True


def detener_musica(desvanecer_ms: int = 1200) -> None:
    """Baja la musica hasta silenciarla en `desvanecer_ms` milisegundos."""
    if disponible():
        pygame.mixer.music.fadeout(desvanecer_ms)


def sonar_moneda() -> None:
    """Efecto de recoger una moneda."""
    if _estado["silencio"] or not disponible():
        return
    if _estado["moneda"] is None:
        ruta = cargador_sprites.ruta_sonido_moneda()
        try:
            _estado["moneda"] = pygame.mixer.Sound(str(ruta)) if ruta else False
            if _estado["moneda"]:
                _estado["moneda"].set_volume(VOLUMEN_EFECTOS)
        except pygame.error:
            _estado["moneda"] = False
    if _estado["moneda"]:
        _estado["moneda"].play()


def silenciado() -> bool:
    return _estado["silencio"]


def alternar_silencio() -> bool:
    """Silencia o reactiva todo el audio; retorna True si quedo en silencio."""
    _estado["silencio"] = not _estado["silencio"]
    if disponible():
        pygame.mixer.music.set_volume(0.0 if _estado["silencio"] else VOLUMEN_MUSICA)
    return _estado["silencio"]
