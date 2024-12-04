import pygame

def Calcular_envido(mano: list) -> int:
    """
    Calcula los puntos de Envido en la mano de un jugador según las reglas del Truco.
    """
    # Solo considerar las cartas con valores válidos para el Envido (máximo 7)
    valores_envido = []
    for carta in mano:
        valor = carta[0]
        if valor > 7:  # 10, 11, 12 valen 0
            valor = 0
        valores_envido.append(valor)
    
    # Agrupar las cartas por palo
    cartas_por_palo = {}
    for i, carta in enumerate(mano):
        palo = carta[1]
        if palo not in cartas_por_palo:
            cartas_por_palo[palo] = []
        cartas_por_palo[palo].append(valores_envido[i])

    maximo_puntaje = 0

    # Calcular el puntaje del Envido
    for palo, cartas in cartas_por_palo.items():
        if len(cartas) >= 2:
            # Ordenar las cartas de mayor a menor
            cartas.sort(reverse=True)
            # Sumar las dos mayores y añadir 20
            puntaje = cartas[0] + cartas[1] + 20
            maximo_puntaje = max(maximo_puntaje, puntaje)
    
    # Si no hay cartas del mismo palo, tomar el valor más alto
    if maximo_puntaje == 0:
        maximo_puntaje = max(valores_envido)

    return maximo_puntaje

def jugar_maquina(mano: list, carta_jugada: tuple = None) -> tuple:
    """
    Estrategia de la máquina para jugar una carta.
    Si se proporciona una carta_jugada, intenta superarla. Si no, juega su carta más alta.
    """
    mano_ordenada = sorted(mano, key=lambda carta: carta[0], reverse=True)

    if carta_jugada is None:
        # Si no hay una carta jugada, juega la carta más alta
        return mano_ordenada[0]

    # Si hay una carta jugada, intenta superarla
    for carta in mano_ordenada:
        if carta[0] > carta_jugada[0]:
            return carta

    # Si no puede superar la carta jugada, juega la más baja
    return mano_ordenada[-1]

def turno_maquina(mano_maquina: list, cartas_jugadas: list, valores_truco: dict, turno_actual: str, manos_ganadas: dict) -> str:
    """
    Maneja el turno de la máquina y actualiza los estados necesarios.
    """
    from funciones.juego import evaluar_mano
    if turno_actual == "maquina" and mano_maquina:
        carta_maquina = jugar_maquina(mano_maquina)
        mano_maquina.remove(carta_maquina)
        carta_jugador = cartas_jugadas[-1][0] if cartas_jugadas else None
        cartas_jugadas.append((carta_jugador, carta_maquina))
        print(f"La máquina jugó: {carta_maquina}")

        # Evaluar quién ganó la mano
        ganador_mano = evaluar_mano(cartas_jugadas[-1], valores_truco)
        if ganador_mano == "jugador":
            print("Ganaste esta mano.")
            manos_ganadas["jugador"] += 1
            return "jugador"  # El jugador inicia la próxima mano
        elif ganador_mano == "maquina":
            print("La máquina ganó esta mano.")
            manos_ganadas["maquina"] += 1
            return "maquina"  # La máquina inicia la próxima mano
        else:
            print("Empate en esta mano.")
            return "jugador"  # En caso de empate, el jugador sigue
    return turno_actual

def turno_maquina_canto(canto_actual: str, turno: str, puntos_canto: dict, puntos_jugador: int, puntos_maquina: int, mano_maquina: list) -> tuple:
    """
    Lógica estratégica para el canto de la máquina.

    Parámetros:
        canto_actual (str): El canto actual ("Truco", "Re Truco", "Vale Cuatro").
        turno (str): Turno actual ("jugador" o "maquina").
        puntos_canto (dict): Puntos asociados a cada canto.
        puntos_jugador (int): Puntos actuales del jugador.
        puntos_maquina (int): Puntos actuales de la máquina.
        mano_maquina (list): Cartas en mano de la máquina.

    Retorno:
        tuple: (turno, canto_actual, respuesta).
    """
    # Evaluar fuerza de la mano de la máquina
    fuerza_mano = sum(carta[0] for carta in mano_maquina if carta[0] <= 7)  # Considerar solo cartas válidas
    fuerza_promedio = fuerza_mano / len(mano_maquina) if mano_maquina else 0

    decision_maquina = "s"  # Por defecto, acepta
    print(f"La máquina está evaluando el {canto_actual}...")

    # Evaluar probabilidad de aceptación basada en puntos y fuerza de la mano
    if puntos_maquina >= 12 and puntos_jugador < 12:
        # La máquina será más conservadora si está ganando
        if fuerza_promedio < 5 or canto_actual == "Vale Cuatro":
            decision_maquina = "n"
    elif puntos_jugador >= 12 and puntos_maquina < 12:
        # La máquina será más agresiva si está perdiendo
        if fuerza_promedio > 5 and canto_actual != "Vale Cuatro":
            decision_maquina = "re"
    else:
        # Evaluación estándar
        if fuerza_promedio < 4 and canto_actual == "Re Truco":
            decision_maquina = "n"
        elif fuerza_promedio > 6 and canto_actual == "Truco":
            decision_maquina = "re"

    # Decisiones basadas en el canto actual
    if canto_actual == "Vale Cuatro":
        # Si es "Vale Cuatro", la máquina evalúa más conservadoramente
        decision_maquina = "n" if fuerza_promedio < 5 else "s"

    # Procesar la decisión
    if decision_maquina == "n":
        print(f"La máquina rechazó el {canto_actual}.")
        return turno, canto_actual, False
    elif decision_maquina == "re":
        # La máquina sube el canto
        print(f"La máquina cantó {canto_actual}.")
        if canto_actual == "Truco":
            canto_actual = "Re Truco"
        elif canto_actual == "Re Truco":
            canto_actual = "Vale Cuatro"
        return "jugador", canto_actual, True
    else:
        # La máquina acepta
        print(f"La máquina aceptó el {canto_actual}.")
        return "jugador", canto_actual, True
    
def mostrar_resultado_final(pantalla: pygame.Surface, fondo: pygame.Surface, imagen: str, mensaje: str, color: tuple) -> None:
    """
    Muestra la pantalla final con el resultado del juego (ganaste/perdiste).
    
    Parámetros:
        pantalla (pygame.Surface): La superficie donde se dibuja todo.
        fondo (pygame.Surface): Imagen de fondo.
        imagen (str): Ruta de la imagen a mostrar.
        mensaje (str): Mensaje a mostrar (Ganaste/Perdiste).
        color (tuple): Color del texto del mensaje.
    """
    # Cargar la imagen
    imagen_final = pygame.image.load(imagen)
    imagen_final = pygame.transform.scale(imagen_final, (300, 300))  # Escalar la imagen al tamaño deseado

    # Bucle para mostrar el resultado
    mostrando_resultado = True
    while mostrando_resultado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:  # Salir con Enter
                mostrando_resultado = False

        pantalla.blit(fondo, (0, 0))  # Mostrar el fondo
        pantalla.blit(imagen_final, (259, 194))  # Mostrar la imagen al centro

        # Mostrar el mensaje
        fuente = pygame.font.Font(None, 50)
        texto = fuente.render(mensaje, True, color)
        pantalla.blit(texto, (300 // 2 - texto.get_width() // 2, 450))

        pygame.display.flip()