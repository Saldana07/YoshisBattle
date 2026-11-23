# Yoshi's Battle

Proyecto universitario de Inteligencia Artificial (Universidad del Valle), Proyecto 2.

Dos Yoshis que se mueven como el caballo del ajedrez compiten en un tablero de 8x8 por
recoger monedas: 4 especiales en el centro (3 puntos cada una) y 9 normales en casillas
aleatorias (1 punto cada una). El juego termina cuando no quedan monedas y gana quien
tenga mas puntos. La maquina (Yoshi verde) siempre empieza y decide con un arbol
**minimax de decisiones imperfectas** cuya profundidad depende del nivel:
principiante = 2, intermedio = 4, experto = 6. El enunciado esta en `docs/Proyecto2.pdf`.

Estado actual: **esqueleto**. Cada archivo tiene su cabecera (objetivo, responsabilidad,
dependencias y contrato) y las funciones lanzan `NotImplementedError` hasta que se
implementen. Las pruebas pendientes estan marcadas con `@unittest.skip("PENDIENTE")`.

## Instalacion del entorno

Mismas tecnologias que AgroBot: Python 3.10+ y `pygame-ce`, dentro de un entorno virtual
local en `.venv/` (ya esta en `.gitignore`; cada integrante crea el suyo).

Windows (PowerShell), desde la raiz del repositorio:

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Linux / macOS:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Si PowerShell no deja activar el entorno, ejecutar una vez
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`. No instalar `pygame` y
`pygame-ce` en el mismo entorno: chocan entre si.

## Ejecucion

Con el entorno activo, desde la raiz del repositorio:

```
python ejecutar.py
```

(tambien se puede, desde la carpeta `src/`: `python -m yoshis_battle.main`). Flujo:
elegir nivel -> partida -> pantalla con el ganador -> de vuelta a elegir nivel.

Pruebas (desde la raiz, con el entorno activo):

```
python -m unittest discover -s tests -v
```

Las tipografias Pixelify Sans y DM Sans van en `src/yoshis_battle/gui/fuentes/`, siguiendo
el `LEEME.md` de esa carpeta (son las mismas de AgroBot).

## Arbol de carpetas

```
YoshisBattle/
├── README.md
├── LICENSE
├── requirements.txt
├── ejecutar.py                 (lanzador desde la raiz)
├── docs/
│   ├── Proyecto2.pdf           (enunciado)
│   └── informe/                (informe: definicion y explicacion de la heuristica)
├── assets/
│   ├── README.md               (sprites esperados, formato y tamano)
│   └── sprites/{tablero,yoshi,moneda}/
├── src/yoshis_battle/
│   ├── __init__.py
│   ├── main.py                 (punto de entrada; une todo)
│   ├── constantes.py           (tablero 8x8, monedas, jugadores, niveles y profundidades)
│   ├── modelo/
│   │   ├── estado.py           (Estado inmutable: Yoshis, monedas, puntos, turno)
│   │   └── movimiento.py       (saltos de caballo)
│   ├── juego/
│   │   ├── generador.py        (estado inicial aleatorio)
│   │   └── reglas.py           (jugadas validas, aplicar jugada, fin y ganador)
│   ├── ia/
│   │   ├── heuristica.py       (funcion de utilidad heuristica)
│   │   └── minimax.py          (minimax con profundidad limite y alfa-beta)
│   ├── controlador/
│   │   └── partida.py          (turnos maquina/humano, fin de partida)
│   └── gui/
│       ├── estilo.py           (ventana, paleta, fuentes)
│       ├── cargador_sprites.py (unico archivo que lee assets/sprites/)
│       ├── pantalla_inicio.py  (bienvenida y eleccion de nivel)
│       ├── panel_tablero.py    (tablero, monedas, Yoshis, casillas resaltadas)
│       ├── panel_marcador.py   (puntos de cada jugador y turno)
│       ├── ventana_juego.py    (bucle de eventos de una partida)
│       ├── pantalla_final.py   (ganador y jugar de nuevo)
│       └── fuentes/LEEME.md
└── tests/
    ├── test_estructura.py      (ya corre: imports y constantes del enunciado)
    ├── test_movimiento.py
    ├── test_generador.py
    ├── test_reglas.py
    ├── test_heuristica.py
    ├── test_minimax.py
    └── test_partida.py
```

## Regla de dependencias

Cada capa solo importa de las que estan antes en esta cadena:

```
constantes <- modelo <- juego <- ia <- controlador <- gui <- main
```

- `constantes.py` no importa nada del proyecto.
- `modelo/` solo importa de `constantes`.
- `juego/` importa de `modelo/` y `constantes`.
- `ia/` importa de `juego/`, `modelo/` y `constantes`; nunca de `controlador/` ni `gui/`.
- `controlador/` importa de `ia/`, `juego/`, `modelo/` y `constantes`; no conoce pygame.
- `gui/` puede importar de todo lo anterior; dentro de `gui/` solo `cargador_sprites.py`
  lee `assets/sprites/`.
- `main.py` es el unico que une todo (composicion). Nada importa de `gui/` excepto
  `main.py` y los propios archivos de `gui/`.

## Contrato principal (para trabajar en paralelo)

| Funcion | Archivo | Recibe | Devuelve |
|---|---|---|---|
| `generar_estado_inicial(rng=None)` | `juego/generador.py` | generador aleatorio opcional | `Estado` |
| `movimientos_validos(estado, jugador=None)` | `juego/reglas.py` | `Estado`, jugador | `list[Casilla]` |
| `aplicar_movimiento(estado, destino)` | `juego/reglas.py` | `Estado`, `Casilla` | `Estado` nuevo |
| `es_terminal(estado)` / `ganador(estado)` | `juego/reglas.py` | `Estado` | `bool` / `"verde"`, `"rojo"`, `"empate"` o `None` |
| `evaluar(estado)` | `ia/heuristica.py` | `Estado` | `float` (alto = bueno para verde) |
| `decidir_por_nivel(estado, nivel)` | `ia/minimax.py` | `Estado`, nivel | `Decision` (jugada, valor, nodos, tiempo) |
| `Partida(nivel)` | `controlador/partida.py` | nivel | partida lista, con la maquina por jugar |
| `jugar_partida(pantalla, partida)` | `gui/ventana_juego.py` | ventana, `Partida` | `"terminada"`, `"volver"` o `"salir"` |

`Casilla` = `(fila, columna)` con indices 0..7; `(0, 0)` es la esquina superior izquierda.

## Decisiones del equipo

Tomadas en el esqueleto (se pueden discutir):

- Mismas tecnologias y convenciones que AgroBot: Python, pygame-ce, `unittest`, carpeta
  `src/`, cabecera de documentacion en cada archivo.
- La maquina es MAX (verde) y el humano es MIN (rojo). La heuristica siempre evalua
  desde el punto de vista de verde.
- El `Estado` es inmutable: aplicar una jugada crea uno nuevo.
- Orden de los saltos del caballo: el de `modelo/movimiento.SALTOS_CABALLO`; minimax
  desempata con ese orden.

Pendientes:

- [ ] Confirmar si la profundidad cuenta jugadas individuales (2 = maquina + humano).
- [ ] Terminos y pesos de la heuristica (`ia/heuristica.py`), con su justificacion para
      el informe.
- [ ] Si minimax en experto se corre en un hilo para no congelar la ventana.
- [ ] Sprites propios (`assets/README.md`) y paleta (`gui/estilo.py`).

## Flujo de trabajo con Git

- Una rama por tarea (`feature/<modulo>`), y Pull Request a `main` con al menos una
  revision de otro integrante.
- Antes de abrir el PR: `python -m unittest discover -s tests` sin errores.
- Al implementar una funcion, quitar el `@unittest.skip("PENDIENTE")` de sus pruebas.
