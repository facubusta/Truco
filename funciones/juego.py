import pygame
from funciones.mazo import *
from funciones.jugador import *
from funciones.puntuacion import *
from funciones.botones import Boton



def jugar_mano(mano_jugador: list, mano_maquina: list, valores_truco: dict) -> str:
    '''
    Juega una mano completa de truco con 3 rondas y determina el ganador según las reglas del juego.
    '''
    resultados_rondas = []  # Guarda el resultado de cada ronda ("jugador", "maquina", "empate")
    
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

def manejar_envido(puntos_jugador: int, puntos_maquina: int, mano_jugador: list, mano_maquina: list) -> tuple:
    '''
    Maneja el flujo del canto de envido y determina al ganador.
    '''
    envido_jugador = Calcular_envido(mano_jugador)
    envido_maquina = Calcular_envido(mano_maquina)
    print(f"Tus puntos: {envido_jugador}")

    # Máquina decide si acepta, sube o rechaza
    if envido_maquina > 20:
        respuesta_maquina = "s" if envido_maquina >= envido_jugador else "real"  # Máquina sube si tiene más puntos
    else:
        respuesta_maquina = "n"

    if respuesta_maquina == "n":
        puntos_jugador += calcular_puntos_envido("envido no querido")
        print("La máquina rechazó el Envido. Sumás 1 punto.")
        return puntos_jugador, puntos_maquina
    elif respuesta_maquina in ["real", "falta"]:
        print(f"La máquina cantó {respuesta_maquina.capitalize()} Envido.")
        print(f"¿Aceptás, subís o rechazás? (s/{respuesta_maquina}/n)")
        decision = input().strip().lower()

        if decision == "n":
            puntos_maquina += calcular_puntos_envido("envido no querido")
            print("Rechazaste el Envido. La máquina suma 1 punto.")
            return puntos_jugador, puntos_maquina
        elif decision == "real":
            print("¡Aceptaste el Real Envido!")
            puntos_jugador += calcular_puntos_envido("real envido")
        elif decision == "falta":
            print("¡Aceptaste la Falta Envido!")
            puntos_ganados = calcular_puntos_envido("falta envido", puntos_jugador, puntos_maquina)
            if envido_jugador > envido_maquina:
                puntos_jugador += puntos_ganados
            else:
                puntos_maquina += puntos_ganados
            return puntos_jugador, puntos_maquina

    # Comparar puntos del Envido
    if envido_jugador > envido_maquina:
        print(f"Tus puntos: {envido_jugador}, Máquina: {envido_maquina}")
        print("Ganaste el Envido.")
        puntos_jugador += calcular_puntos_envido("envido ganado")
    elif envido_jugador < envido_maquina:
        print(f"Tus puntos: {envido_jugador}, Máquina: {envido_maquina}")
        print("La máquina ganó el Envido.")
        puntos_maquina += calcular_puntos_envido("envido ganado")
    else:
        print(f"Tus puntos: {envido_jugador}, Máquina: {envido_maquina}")
        print("Empate en el Envido. No suman puntos.")
    return puntos_jugador, puntos_maquina

def evaluar_mano(cartas: tuple, valores_truco: dict) -> str:
    """
    Evalúa quién gana una mano según las cartas jugadas y sus valores.

    Parámetros:
        cartas (tuple): Una tupla con las cartas jugadas por el jugador y la máquina.
                        Ejemplo: ((10, "oros"), (2, "oros")).
        valores_truco (dict): Diccionario con los valores de las cartas en el Truco.

    Retorno:
        str: "jugador" si gana el jugador, "maquina" si gana la máquina o "empate".
    """
    carta_jugador, carta_maquina = cartas
    valor_jugador = valores_truco[f"{carta_jugador[0]} de {carta_jugador[1]}"]
    valor_maquina = valores_truco[f"{carta_maquina[0]} de {carta_maquina[1]}"]

    if valor_jugador > valor_maquina:
        return "jugador"
    elif valor_jugador < valor_maquina:
        return "maquina"
    else:
        return "empate"

def determinar_ganador_ronda(ganadores_manos: dict) -> str:
    """
    Determina quién ganó la ronda según las manos ganadas por cada jugador.

    Parámetros:
        ganadores_manos (dict): Diccionario con el conteo de manos ganadas.
                                Ejemplo: {"jugador": 2, "maquina": 1}

    Retorno:
        str: "jugador" si gana el jugador, "maquina" si gana la máquina o "empate" si no se decide.
    """
    if ganadores_manos["jugador"] >= 2:
        return "jugador"
    elif ganadores_manos["maquina"] >= 2:
        return "maquina"
    else:
        return "empate"  # Si no se llegó a 2 manos ganadas por nadie

def gestionar_truco_interfaz(pantalla, turno, puntos_jugador, puntos_maquina) -> tuple:
    """
    Maneja la lógica del Truco, Re Truco y Vale Cuatro en la interfaz gráfica.

    Parámetros:
        pantalla (pygame.Surface): Superficie de pygame.
        turno (str): Quién inicia el canto ("jugador" o "maquina").
        puntos_jugador (int): Puntaje actual del jugador.
        puntos_maquina (int): Puntaje actual de la máquina.

    Retorno:
        tuple: (puntos_jugador, puntos_maquina, canto_terminado).
    """
    # Crear los botones para aceptar, subir y rechazar
    boton_aceptar = Boton(200, 500, 150, 50, "Aceptar")
    boton_subir = Boton(400, 500, 150, 50, "Subir")
    boton_rechazar = Boton(600, 500, 150, 50, "Rechazar")

    puntos_canto = {"Truco": 2, "Re Truco": 3, "Vale Cuatro": 4}
    canto_actual = "Truco"
    canto_terminado = False

    while not canto_terminado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return puntos_jugador, puntos_maquina, True

        boton_aceptar.dibujar(pantalla)
        boton_subir.dibujar(pantalla)
        boton_rechazar.dibujar(pantalla)

        pygame.display.flip()

        if turno == "jugador":
            if boton_aceptar.detectar_clic():
                pygame.time.delay(500) 
                print(f"¡cantaste {canto_actual}!")
                turno = "maquina"
                
            elif boton_subir.detectar_clic() and canto_actual != "Vale Cuatro":
                pygame.time.delay(500)
                canto_actual = {"Truco": "Re Truco", "Re Truco": "Vale Cuatro"}[canto_actual]
                print(f"Subiste el canto a {canto_actual}.")
                turno = "maquina"
            elif boton_rechazar.detectar_clic():
                pygame.time.delay(500)
                puntos_maquina += puntos_canto[canto_actual] - 1
                print(f"Rechazaste el {canto_actual}. La máquina gana {puntos_canto[canto_actual] - 1} puntos.")
                canto_terminado = True
                return puntos_jugador, puntos_maquina

        elif turno == "maquina":
            decision_maquina = "s" 
            print(f"¡La maquina acepto el {canto_actual}!")
            turno = "jugador"
            if canto_actual == "Re Truco" and puntos_canto[canto_actual] > 0:
                decision_maquina = "s"
                turno = "jugador"
            elif canto_actual == "Vale Cuatro":
                decision_maquina = "s"
                turno = "jugador"
            else:
                decision_maquina = "re" if canto_actual != "Vale Cuatro" else "n"
                turno = "jugador"

            if decision_maquina == "n":
                puntos_jugador += puntos_canto[canto_actual] - 1
                print(f"La máquina rechazó el {canto_actual}. Ganás {puntos_canto[canto_actual] - 1} puntos.")
                canto_terminado = True
                return puntos_jugador, puntos_maquina
            
            elif decision_maquina == "re":
                canto_actual = {"Truco": "Re Truco", "Re Truco": "Vale Cuatro"}[canto_actual]
                print(f"La máquina cantó {canto_actual}.")
                turno = "jugador"
            elif decision_maquina == "s":
                print(f"La máquina aceptó el {canto_actual}.")
                turno = "jugador"

    return puntos_jugador, puntos_maquina, False

def turno_maquina(mano_maquina: list, cartas_jugadas: list, valores_truco: dict, turno_actual: str, manos_ganadas: dict) -> str:
    if turno_actual == "maquina" and mano_maquina:
        pygame.time.delay(500)  # Retraso para simular el turno
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
            return "jugador"
        elif ganador_mano == "maquina":
            print("La máquina ganó esta mano.")
            manos_ganadas["maquina"] += 1
            return "maquina"
        else:
            print("Empate en esta mano.")
            return "jugador"

        # Verificar si alguien ganó dos manos
        if manos_ganadas["jugador"] == 2 or manos_ganadas["maquina"] == 2:
            print("Se ganaron dos manos. Fin de la ronda.")
            return "fin_ronda"

    return turno_actual

def determinar_ganador_final(puntos_jugador: int, puntos_maquina: int, ganador_primera: str, manos_ganadas: dict,
                             puntos_truco: int) -> tuple:
    """
    Determina el ganador de la ronda y actualiza los puntos.
    """
    print("¡Fin de la ronda!")
    ganador_ronda = determinar_ganador_ronda(manos_ganadas)
    if ganador_ronda == "jugador":
        puntos_jugador += puntos_truco if puntos_truco > 0 else 1
        print("Ganaste la ronda.")
    elif ganador_ronda == "maquina":
        puntos_maquina += puntos_truco if puntos_truco > 0 else 1
        print("La máquina ganó la ronda.")
    else:
        print("La ronda terminó en empate.")
        if ganador_primera == "jugador":
            puntos_jugador += 1
        else:
            puntos_maquina += 1

    # Reiniciar la ronda
    return puntos_jugador, puntos_maquina

def reiniciar_ronda(mazo: list, mano_jugador: list, mano_maquina: list, cartas_jugadas: list,
                    manos_ganadas: dict, inicia_ronda: str) -> None:
    """
    Reinicia las variables necesarias para iniciar una nueva ronda.

    Parámetros:
        mazo (list): El mazo de cartas para repartir.
        mano_jugador (list): Las cartas en mano del jugador.
        mano_maquina (list): Las cartas en mano de la máquina.
        cartas_jugadas (list): Las cartas jugadas en la ronda.
        manos_ganadas (dict): Diccionario con las manos ganadas por cada jugador.
        
         inicia_ronda (str): Alterna entre "jugador" y "maquina" para iniciar la ronda.
    """
    print("Comienza una nueva ronda.")
    # Crear un nuevo mazo y repartir cartas
    mazo.clear()
    nuevo_mazo, rutas_imagenes, valores_truco = crear_mazo()
    mazo.extend(nuevo_mazo)
    mano_jugador.clear()
    mano_jugador.extend(mazo[:3])
    del mazo[:3]
    mano_maquina.clear()
    mano_maquina.extend(mazo[:3])
    del mazo[:3]

    # Reiniciar variables
    cartas_jugadas.clear()
    manos_ganadas["jugador"] = 0
    manos_ganadas["maquina"] = 0
    puntos_truco = 0
    envido_jugado = False
    ronda_activa = True

    # Alternar quién inicia la ronda
    turno_actual = inicia_ronda
    inicia_ronda = "maquina" if inicia_ronda == "jugador" else "jugador"

    pygame.time.delay(500)  # Dar un pequeño tiempo de espera para iniciar la nueva ronda

def manejar_turno_maquina(
    mano_maquina: list, 
    cartas_jugadas: list, 
    valores_truco: dict, 
    turno_actual: str, 
    manos_ganadas: dict,
    cartas_maquina: list
) -> str:
    """
    Maneja el turno de la máquina, ya sea iniciando la jugada o respondiendo.
    """
    if not cartas_jugadas or cartas_jugadas[-1][1] is not None:  # La máquina inicia la jugada
        carta_maquina = jugar_maquina(mano_maquina)  # Juega la carta más alta o estratégica
        mano_maquina.remove(carta_maquina)
        #cartas_jugadas.append((None, carta_maquina))  # La máquina inicia la jugada
        cartas_maquina.append(carta_maquina)
        print(f"La máquina jugó: {carta_maquina}")
        return "jugador"  # Turno pasa al jugador

    elif cartas_jugadas[-1][1] is None:  # La máquina responde a la jugada del jugador
        carta_jugador = cartas_jugadas[-1][0]
        carta_maquina = jugar_maquina(mano_maquina, carta_jugador)  # Responde estratégicamente
        mano_maquina.remove(carta_maquina)
        cartas_jugadas[-1] = (carta_jugador, carta_maquina)  # Completa la jugada actual
        print(f"La máquina jugó: {carta_maquina}")

        # Evaluar quién gana la mano
        ganador_mano = evaluar_mano(cartas_jugadas[-1], valores_truco)
        if ganador_mano == "jugador":
            print("Ganaste esta mano.")
            manos_ganadas["jugador"] += 1
            return "jugador"  # El jugador sigue si gana
        elif ganador_mano == "maquina":
            print("La máquina ganó esta mano.")
            manos_ganadas["maquina"] += 1
            return "maquina"  # La máquina sigue si gana
        else:
            print("Empate en esta mano.")
            return "jugador"  # Por defecto, turno pasa al jugador en caso de empate

    return turno_actual  # Mantener turno si no se cumplió ninguna condición