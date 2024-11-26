carta = ()

def Calcular_envido(mano: list) -> int:
    '''
    Calcula los puntos de envido en la mano de un jugador, siguiendo las reglas del Truco.

    Parámetro:
        mano (list): Lista de cartas en la mano del jugador.

    Retorno:
        int: Puntos de envido calculados.
    '''
    puntos = 0

    # Validar formato de las cartas
    #if not all(isinstance(carta, tuple) and isinstance(carta[0], int) for carta in mano):
     #   raise ValueError("Las cartas deben estar en el formato (valor, palo)")

    # Crear una lista de los valores "reducidos" para el envido (10, 11, 12 no suman puntos)
    valores_envido = [min(carta[0], 7) for carta in mano]  # Reducimos valores mayores a 7
    
    # Comparar pares de cartas para encontrar el mejor envido
    for i in range(len(mano)):
        for j in range(i + 1, len(mano)):
            # Comparar si las cartas tienen el mismo palo
            if mano[i][1] == mano[j][1]:  # Comparar los palos
                valor_envido = 20 + valores_envido[i] + valores_envido[j]  # Sumar valores reducidos + 20
                puntos = max(puntos, valor_envido)  # Guardar el máximo puntaje encontrado

    return puntos

def jugar_maquina(mano: list, carta_jugada: tuple) -> tuple:
    '''
    Es una estrategia de juego para la máquina,
    siguiendo la lógica del truco.
    '''
    mano_ordenada = sorted(mano, key=lambda carta: carta[0], reverse=True)

    
    for carta in mano_ordenada:
        if carta[0] >= carta_jugada[0]:  
            return carta

    return mano_ordenada[-1]

def decidir_canto_maquina(mano: list, tipo: str) -> str:
    '''
    Decide si la máquina canta o acepta un canto (envido o truco).
    '''
    if tipo == "envido":
        puntos_envido = Calcular_envido(mano)
        if puntos_envido > 21:  
            return "s"
        return "n"
    elif tipo == "truco":
        return "s"