import pygame
from funciones.mazo import *
from funciones.jugador import *
from funciones.puntuacion import *
from funciones.botones import *

def manejar_envido_completo(puntos_jugador: int, puntos_maquina: int, mano_jugador: list, mano_maquina: list, turno_actual: str, seleccion : int) -> tuple:
    """
    Maneja el flujo completo del Envido, incluyendo variantes como "Real Envido" y "Falta Envido".

    Parámetros:
        puntos_jugador (int): Puntos actuales del jugador.
        puntos_maquina (int): Puntos actuales de la máquina.
        mano_jugador (list): Mano del jugador.
        mano_maquina (list): Mano de la máquina.
        turno_actual (str): Quién inicia el canto ("jugador" o "maquina").

    Retorno:
        tuple: (puntos_jugador_actualizados, puntos_maquina_actualizados, envido_terminado)
    """
    puntos_envido_jugador = Calcular_envido(mano_jugador)
    puntos_envido_maquina = Calcular_envido(mano_maquina)

    print(f"Tus puntos de Envido: {puntos_envido_jugador}")
    print(f"Puntos de Envido de la máquina: {puntos_envido_maquina}")

    opciones_envido = ["envido", "envido envido", "real envido", "falta envido"]
    valores_envido = {"envido": 2, "envido envido": 4, "real envido": 5, "falta envido": 0}
    valores_rechazados = {"envido": 1, "envido envido": 2, "real envido": 5, "falta envido": 1}

    # Determina los puntos faltantes para "Falta Envido"
    puntos_faltantes_jugador = seleccion - puntos_jugador
    puntos_faltantes_maquina = seleccion - puntos_maquina
    valores_envido["falta envido"] = max(puntos_faltantes_jugador, puntos_faltantes_maquina)

    envido_terminado = False
    canto_actual = ""
    respuesta = True

    # Ciclo para manejar el canto y respuesta del Envido
    while not envido_terminado:
        if turno_actual == "jugador":
            print("Opciones disponibles: Envido, Real Envido, Falta Envido")
            canto_jugador = input("¿Qué querés cantar? (envido/real envido/falta envido/n): ").strip().lower()

            if canto_jugador == "n":
                print("Decidiste no cantar más. La máquina puede responder.")
                turno_actual = "maquina"
            elif canto_jugador in opciones_envido:
                print(f"Cantaste {canto_jugador}.")
                canto_actual = canto_jugador
                turno_actual = "maquina"
            else:
                print("Canto inválido. Intentá nuevamente.")
        elif turno_actual == "maquina":
            # Estrategia básica de la máquina
            if puntos_envido_maquina > 27:
                respuesta_maquina = "s"  # Acepta
            else:
                respuesta_maquina = "n"  # Rechaza

            if respuesta_maquina == "s":
                print(f"La máquina aceptó el {canto_actual}.")
                if canto_actual == "falta envido":
                    ganador = "jugador" if puntos_envido_jugador > puntos_envido_maquina else "maquina"
                    puntos_ganados = valores_envido[canto_actual]
                    if ganador == "jugador":
                        puntos_jugador += puntos_ganados
                        print(f"Ganaste la falta envido y sumás {puntos_ganados} puntos.")
                    else:
                        puntos_maquina += puntos_ganados
                        print(f"La máquina ganó la falta envido y suma {puntos_ganados} puntos.")
                else:
                    ganador = "jugador" if puntos_envido_jugador > puntos_envido_maquina else "maquina"
                    puntos_ganados = valores_envido[canto_actual]
                    if ganador == "jugador":
                        puntos_jugador += puntos_ganados
                        print(f"Ganaste el {canto_actual} y sumás {puntos_ganados} puntos.")
                    else:
                        puntos_maquina += puntos_ganados
                        print(f"La máquina ganó el {canto_actual} y suma {puntos_ganados} puntos.")

                envido_terminado = True
            elif respuesta_maquina == "n":
                print(f"La máquina rechazó el {canto_actual}.")
                puntos_jugador += valores_rechazados[canto_actual]
                print(f"Sumás {valores_rechazados[canto_actual]} puntos.")
                envido_terminado = True

    return puntos_jugador, puntos_maquina, envido_terminado
    
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

def gestionar_truco_interfaz(pantalla: pygame.surface, turno: str, canto_actual: str, respuesta: bool) -> tuple:
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
    terminar_canto = False
    responde = ""
    if turno == "jugador":
        responde = "maquina"
    puntos_canto = {"Truco": 2, "Re Truco": 3, "Vale Cuatro": 4}
    if responde != "":
        if canto_actual == "":
            canto_actual = "Truco"
        elif canto_actual == "Truco":
            canto_actual = "Re Truco"
        elif canto_actual == "Re Truco":
            canto_actual = "Vale Cuatro"    
    
    while terminar_canto == False:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return canto_actual, respuesta, turno

        pygame.display.flip()

        if responde == "jugador":
            boton_aceptar.dibujar(pantalla)
            if canto_actual != "Vale Cuatro":
                boton_subir.dibujar(pantalla)
            boton_rechazar.dibujar(pantalla)

            if boton_aceptar.detectar_clic():
                pygame.time.delay(500)
                respuesta = True
                print(f"¡cantaste {canto_actual}!")             
            elif boton_subir.detectar_clic() and canto_actual != "Vale Cuatro":
                pygame.time.delay(500)
                respuesta = True
                if canto_actual == "Truco":
                    canto_actual = "Re Truco"
                elif canto_actual == "Re Truco":
                    canto_actual = "Vale Cuatro" 
            elif boton_rechazar.detectar_clic():
                pygame.time.delay(500)
                print(f"Rechazaste el {canto_actual}.")
                respuesta = False
            turno = "jugador"  
            terminar_canto = True
        elif responde == "maquina":
            decision_maquina = "s" 
            print(f"¡La maquina acepto el {canto_actual}!")
            pygame.time.delay(500)
            if canto_actual == "Re Truco" and puntos_canto[canto_actual] > 0:
                decision_maquina = "s"
                respuesta = True
            elif canto_actual == "Vale Cuatro":
                decision_maquina = "s"
                respuesta = True
            else:
                decision_maquina = "re" if canto_actual != "Vale Cuatro" else "n"

            if decision_maquina == "n":               
                print(f"La máquina rechazó el {canto_actual}.")
                respuesta = False
            else:
                respuesta = True
            terminar_canto = True
            turno = "maquina"
        else:
            terminar_canto = True

    return canto_actual, respuesta, turno

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

def manejar_turno_maquina(mano_maquina: list, cartas_jugadas: list, valores_truco: dict, turno_actual: str,
                           manos_ganadas: dict, cartas_maquina: list) -> str:
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