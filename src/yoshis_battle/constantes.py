"""
Archivo:       src/yoshis_battle/constantes.py
Objetivo:      Centralizar los valores fijos del juego para que ningun otro archivo repita
               numeros "magicos": tamano del tablero, monedas, jugadores y niveles.
Responsabilidad:
    SI hace:
        - Definir el tamano del tablero (8 x 8).
        - Definir las cuatro casillas especiales del centro y el valor de cada tipo de
          moneda (especial = 3 puntos, normal = 1 punto).
        - Definir cuantas monedas normales hay (9).
        - Definir los dos jugadores y quien empieza (siempre la maquina, Yoshi verde).
        - Definir los niveles de dificultad y la profundidad limite de cada uno
          (principiante = 2, intermedio = 4, experto = 6).
    NO hace:
        - No contiene logica ni estructuras de datos del juego.
        - No importa nada de otros modulos del proyecto.
Importa de:    (nada del proyecto; este es el modulo base de toda la jerarquia).
Lo importan:   modelo/, juego/, ia/, controlador/ y gui/.
Convenciones:
    - Las casillas son tuplas (fila, columna) con indices de 0 a TAMANO_TABLERO - 1;
      (0, 0) es la esquina superior izquierda.
Decisiones de equipo:
    - La profundidad cuenta jugadas individuales (plies): profundidad 2 = una jugada de
      la maquina y la respuesta del humano.  PENDIENTE confirmar con el profesor.
"""
TAMANO_TABLERO = 8

# ---------------------------------------------------------------- monedas
CASILLAS_ESPECIALES = ((3, 3), (3, 4), (4, 3), (4, 4))
VALOR_MONEDA_ESPECIAL = 3
VALOR_MONEDA_NORMAL = 1
CANTIDAD_MONEDAS_NORMALES = 9

# ---------------------------------------------------------------- jugadores
VERDE = "verde"   # la maquina (MAX en minimax)
ROJO = "rojo"     # el humano (MIN en minimax)
JUGADOR_MAQUINA = VERDE
JUGADOR_HUMANO = ROJO
JUGADOR_INICIAL = VERDE
EMPATE = "empate"

# ---------------------------------------------------------------- niveles
PRINCIPIANTE = "Principiante"
INTERMEDIO = "Intermedio"
EXPERTO = "Experto"
PROFUNDIDAD_POR_NIVEL = {
    PRINCIPIANTE: 2,
    INTERMEDIO: 4,
    EXPERTO: 6,
}
