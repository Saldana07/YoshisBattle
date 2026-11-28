# Assets de Yoshi's Battle

Esta carpeta contiene solo imagenes y la fuente de titulos. Igual que en AgroBot, solo
`src/yoshis_battle/gui/cargador_sprites.py` conoce la ruta de esta carpeta; ningun otro
archivo del proyecto debe leer `assets/` directamente.

## Estilo

Pixel art. Si el juego los agranda, usa `pygame.transform.scale` (nunca `smoothscale`)
y un factor entero.

## Lo que usa el juego hoy (`assets/sprites/`)

| Archivo / carpeta | Que se saca de ahi | Clave en `cargar_sprites` |
|---|---|---|
| `yoshi/DS _ DSi - Mario & Luigi_ Partners in Time - Non-Playable Characters - Yoshi.png` | Fila "Palettes" de la hoja: el 1.er Yoshi (verde) y el 5.o (rojo), 24 x 39 px; el fondo azul (165, 235, 255) se vuelve transparente | `yoshi_verde`, `yoshi_rojo` |
| (misma hoja) | Ciclos de caminar del Yoshi verde: abajo (fila 1), abajo-derecha (fila 2), arriba (fila 3) y derecha (fila 5, 8 primeros). La hoja no trae arriba-derecha: se usa el perfil. Las 3 direcciones hacia la izquierda se sacan reflejando. El rojo se obtiene recoloreando con el mapa verde -> rojo de la fila "Palettes" | `cargar_animaciones_yoshi()` |
| (misma hoja) | Celebracion, brazos arriba y boca abierta (los 4 primeros de la fila donde Yoshi aparece acostado, y = 228): la hace el ganador al final de la partida | `cargar_animaciones_yoshi()[...]["celebrar"]` |
| (misma hoja) | Esperando, de espaldas moviendo las manos (fila 5, 4 ultimos): la hace el Yoshi del humano si tarda mas de 4 s en jugar | `cargar_animaciones_yoshi()[...]["esperar"]` |
| `moneda/Coin (Large)/[idle]` y `[get] coin_large_*.png` | 30 cuadros girando + 8 al recogerla, de 64 x 64 (moneda con estrella), recortados a 34 x 34 | `moneda_especial` (3 pts), `moneda_especial_toma` |
| `moneda/Coin (Small)/[idle]` y `[get] coin_small_*.png` | 30 + 8 cuadros de 32 x 32, recortados a 26 x 26 | `moneda_normal` (1 pt), `moneda_normal_toma` |
| `font/SuperMario256.ttf` | Fuente de titulos y puntajes (`estilo.FAMILIA_TITULO`) | `ruta_fuente_titulo()` |
| `tablero/` (vacia) | Las casillas de pasto y las de arena del centro se dibujan por codigo | `casilla_clara`, `casilla_oscura`, `casilla_especial_clara`, `casilla_especial_oscura` |

## Sonidos (`assets/sonidos/`)

| Archivo | Uso | Lo busca |
|---|---|---|
| `mario-coin-sfx.mp3` | Al recoger una moneda (suena cuando el Yoshi aterriza en ella) | `ruta_sonido_moneda()`: `moneda*` o `*coin*` |
| `flower-garden-yoshis-island-1.mp3` | Musica de fondo (Flower Garden, *Yoshi's Island*), en bucle desde que empieza la partida hasta que aterriza la ultima jugada | `ruta_musica()`: `musica*`, `music*`, `*theme*`, `*bgm*`, `*soundtrack*`; si ninguno coincide, cualquier otro audio de esta carpeta que no sea el de la moneda |

Formatos aceptados: `.ogg`, `.mp3`, `.wav`, `.flac`, `.opus`. Si falta un archivo (o el
equipo no tiene audio) el juego sigue en silencio.

## Archivos "limpios" opcionales

Si alguien quiere reemplazar un sprite sin tocar codigo, basta con poner un PNG con fondo
transparente con estos nombres; el cargador los prefiere sobre la hoja y las carpetas de
arriba:

| Archivo | Representa |
|---|---|
| `yoshi/yoshi_verde.png`, `yoshi/yoshi_rojo.png` | Yoshis (mirando a la derecha) |
| `moneda/moneda_normal.png`, `moneda/moneda_especial.png` | Monedas (sin animacion) |
| `tablero/casilla_clara.png`, `tablero/casilla_oscura.png`, `tablero/casilla_especial_clara.png`, `tablero/casilla_especial_oscura.png` | Casillas (cubren toda la casilla) |

Si falta todo, `cargador_sprites.py` dibuja un reemplazo (circulo de color) para que el
juego siga funcionando.

## Creditos

- Hoja de Yoshi: *Mario & Luigi: Partners in Time* (Nintendo DS), ripeada por A.J. Nitro
  (The Spriters Resource). La hoja pide dar credito si se usa.
- Yoshi y las monedas son propiedad de Nintendo; se usan solo con fines academicos.
