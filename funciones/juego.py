from funciones.mazo import *
from funciones.jugador import *
from funciones.puntuacion import *

def inicializar_juego(puntos_victoria: int) -> None:
    '''
    Inicia el juego y controla las rondas hasta que alguien gane.
    '''
    puntos_jugador = 0
    puntos_maquina = 0

    while puntos_jugador < puntos_victoria and puntos_maquina < puntos_victoria:
        mazo = crear_mazo()
        mano_jugador, mano_maquina = repartir_cartas(mazo)

        print("Mano del Jugador:", mano_jugador)
        print("Mano de la Máquina:", mano_maquina)

        puntos_ronda = jugar_ronda(mano_jugador, mano_maquina)
        puntos_jugador += puntos_ronda['jugador']
        puntos_maquina += puntos_ronda['maquina']

        print(f"Puntaje - Jugador: {puntos_jugador}, Máquina: {puntos_maquina}")

    
    if puntos_jugador >= puntos_victoria:
        print("¡El Jugador gana la partida!")
    else:
        print("¡La Máquina gana la partida!")

def jugar_ronda(mano_jugador: list, mano_maquina: list) -> dict:
    '''
    Ejecuta una ronda entre el jugador y la máquina.
    '''
    
    puntos = {"jugador": 0, "maquina": 0}

    # Calcular puntos del envido
    puntos_envido_jugador = Calcular_envido(mano_jugador)
    puntos_envido_maquina = Calcular_envido(mano_maquina)

    print(f"Puntos envido Jugador: {puntos_envido_jugador}, Máquina: {puntos_envido_maquina}")

    # Cantar envido
    print("La Máquina canta envido. ¿Aceptás? (s/n)")
    decision_envido = input().strip().lower()

    if decision_envido == "s":
        if puntos_envido_jugador > puntos_envido_maquina:
            puntos["jugador"] += calcular_puntos_envido("envido ganado")
        elif puntos_envido_jugador < puntos_envido_maquina:
            puntos["maquina"] += calcular_puntos_envido("envido ganado")
        else:
            puntos["jugador"] += calcular_puntos_envido("envido no querido")
            puntos["maquina"] += calcular_puntos_envido("envido no querido")
    else:
        puntos["maquina"] += calcular_puntos_envido("envido no querido")

    # Jugar tres manos de truco
    ganador_manos = {"jugador": 0, "maquina": 0}
    for _ in range(3):
        ganador, _, _ = jugar_mano(mano_jugador, mano_maquina)
        if ganador in ganador_manos:
            ganador_manos[ganador] += 1

        # Si un jugador gana dos manos, la ronda termina
        if ganador_manos["jugador"] == 2 or ganador_manos["maquina"] == 2:
            break

    # Asignar puntos del truco
    if ganador_manos["jugador"] > ganador_manos["maquina"]:
        puntos["jugador"] += calcular_puntos_truco("truco")
    elif ganador_manos["maquina"] > ganador_manos["jugador"]:
        puntos["maquina"] += calcular_puntos_truco("truco")
    return puntos

def jugar_mano(mano_jugador: list, mano_maquina: list, valores_truco: dict) -> str:
    '''
    Juega una mano completa de truco con 3 rondas y determina el ganador según las reglas del juego.
    '''
    resultados_rondas = []  # Guardará el resultado de cada ronda ("jugador", "maquina", "empate")
    
    for ronda in range(3):
        print(f"\nRonda {ronda + 1}:\n")
        
        # Mostrar las cartas disponibles del jugador
        print("Tus cartas:")
        for i, carta in enumerate(mano_jugador):
            print(f"{i + 1}: {carta}")
        
        # Jugador selecciona su carta
        carta_jugador = None
        while carta_jugador is None:
            try:
                seleccion = int(input("Seleccioná una carta para jugar (1, 2, o 3): "))
                if 1 <= seleccion <= len(mano_jugador):
                    carta_jugador = mano_jugador.pop(seleccion - 1)
                else:
                    print("Selección inválida. Elegí un número válido.")
            except ValueError:
                print("Entrada inválida. Ingresá un número.")
        
        # Máquina selecciona su carta
        carta_maquina = jugar_maquina(mano_maquina, carta_jugador)
        mano_maquina.remove(carta_maquina)
        
        # Comparar valores según el diccionario del truco
        valor_jugador = valores_truco[carta_jugador]
        valor_maquina = valores_truco[carta_maquina]
        
        if valor_jugador > valor_maquina:
            resultados_rondas.append("jugador")
        elif valor_maquina > valor_jugador:
            resultados_rondas.append("maquina")
        else:
            resultados_rondas.append("empate")
        
        print(f"El jugador jugó: {carta_jugador} (valor: {valor_jugador})")
        print(f"La máquina jugó: {carta_maquina} (valor: {valor_maquina})")
        print(f"Ganador de la ronda: {resultados_rondas[-1]}")
    
    # Determinar el ganador de la mano según las reglas
    if resultados_rondas[0] == "jugador":
        if resultados_rondas[1] == "maquina" and resultados_rondas[2] == "empate":
            return "jugador"
    elif resultados_rondas[0] == "maquina":
        if resultados_rondas[1] == "jugador" and resultados_rondas[2] == "empate":
            return "maquina"
    
    # Contar rondas ganadas
    jugador_gana = resultados_rondas.count("jugador")
    maquina_gana = resultados_rondas.count("maquina")
    
    if jugador_gana > maquina_gana:
        return "jugador"
    elif maquina_gana > jugador_gana:
        return "maquina"
    else:
        return "empate"  # En caso de empate en rondas

def manejar_truco(puntos_jugador: int, puntos_maquina: int) -> tuple:
    '''
    Maneja el flujo del canto del truco y determina al ganador.

    Parámetros:
        puntos_jugador (int): Puntaje actual del jugador.
        puntos_maquina (int): Puntaje actual de la máquina.

    Retorno:
        tuple: (puntos_jugador, puntos_maquina), puntajes actualizados después del truco.
    '''
    print("La máquina canta Truco. ¿Aceptás? (s/n)")
    respuesta = input().strip().lower()

    if respuesta == "n":
        print("No aceptaste el Truco. La máquina gana 1 punto.")
        puntos_maquina += 1
        return puntos_jugador, puntos_maquina

    # Simulación de la lógica del truco: el jugador siempre gana
    print("¡Aceptaste el Truco!")
    print("La máquina juega su estrategia y el jugador gana.")
    puntos_jugador += 2

    return puntos_jugador, puntos_maquina

def manejar_envido(puntos_jugador: int, puntos_maquina: int, mano_jugador: list, mano_maquina: list) -> tuple:
    '''
    Maneja el flujo del canto de envido y determina al ganador.

    Retorno:
        tuple: (puntos_jugador, puntos_maquina), puntajes actualizados después del envido.
    '''
    print("¿Querés cantar envido? (s/n)")
    respuesta = input().strip().lower()

    if respuesta != "s":
        return puntos_jugador, puntos_maquina

    envido_jugador = Calcular_envido(mano_jugador)
    envido_maquina = Calcular_envido(mano_maquina)

    print("La máquina canta envido. ¿Querés aceptar? (s/n)")
    respuesta_maquina = "s" if envido_maquina > 20 else "n"

    if respuesta_maquina == "n":
        puntos_jugador += calcular_puntos_envido("envido no querido")
        return puntos_jugador, puntos_maquina

    print(f"Tus puntos: {envido_jugador}, Máquina: {envido_maquina}")
    if envido_jugador > envido_maquina:
        puntos_jugador += calcular_puntos_envido("envido ganado")
    elif envido_jugador < envido_maquina:
        puntos_maquina += calcular_puntos_envido("envido ganado")
    else:
        print("Empate en envido.")
    return puntos_jugador, puntos_maquina
















