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

def decidir_canto_maquina(mano: list, tipo: str) -> str:
    '''
    Decide si la máquina canta o acepta un canto (envido o truco).
    '''
    if tipo == "envido":
        puntos_envido = Calcular_envido(mano)
        if puntos_envido > 25:  
            return "s"
        return "n"
    elif tipo == "truco":
        return "s"
    
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