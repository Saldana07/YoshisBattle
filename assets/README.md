# Assets de Yoshi's Battle

Esta carpeta contiene solo imagenes. Igual que en AgroBot, solo
`src/yoshis_battle/gui/cargador_sprites.py` conoce la ruta de esta carpeta; ningun otro
archivo del proyecto debe leer `assets/` directamente.

## Estilo

Pixel art de 64 x 64 px, como los sprites de AgroBot. Si el juego los agranda, debe usar
`pygame.transform.scale` (nunca `smoothscale`) y un factor entero.

## Sprites esperados (`assets/sprites/`)

Formato: PNG de 64 x 64 px con fondo transparente, salvo las casillas, que cubren toda
la casilla.

| Carpeta / archivo                 | Representa                          | Estado     |
|-----------------------------------|-------------------------------------|------------|
| `tablero/casilla_clara.png`       | Casilla clara del tablero           | PENDIENTE  |
| `tablero/casilla_oscura.png`      | Casilla oscura del tablero          | PENDIENTE  |
| `yoshi/yoshi_verde.png`           | Yoshi de la maquina                 | PENDIENTE  |
| `yoshi/yoshi_rojo.png`            | Yoshi del humano                    | PENDIENTE  |
| `moneda/moneda_normal.png`        | Moneda normal (1 punto)             | PENDIENTE  |
| `moneda/moneda_especial.png`      | Moneda especial del centro (3 pts)  | PENDIENTE  |

Si falta un archivo, `cargador_sprites.py` debe dibujar un reemplazo (circulo de color)
para que el juego siga funcionando.

Nota: Yoshi es un personaje de Nintendo. Para el informe y el repositorio publico es mas
seguro usar sprites de elaboracion propia (como en AgroBot) en lugar de imagenes
descargadas del juego original.
