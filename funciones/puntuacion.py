import pygame

def calcular_puntos_truco(ganador_truco: str) -> int:
    '''
    Calcula los puntos del truco obtenidos en una mano
    '''
    if ganador_truco == "truco":
        return 2
    elif ganador_truco == "retruco":
        return 3
    elif ganador_truco == "vale cuatro":
        return 4
    return 1

def calcular_puntos_envido(tipo_envido: str, puntos_jugador: int = 0, maquina_puntos: int = 0,
                            puntos_victoria: int = 30) -> int:
    '''
    Calcula los puntos del envido comparando los
    puntos del jugador y de la maquina
    '''


    if tipo_envido == "envido no querido":
        return 1
    elif tipo_envido == "envido ganado":
        return 2
    elif tipo_envido == "envido envido":
        return 4
    elif tipo_envido == "real envido":
        return 5
    elif tipo_envido == "envido envido real envido":
        return 7
    elif tipo_envido == "falta envido no querido":
        return 2
    elif tipo_envido == "falta envido":
        puntos_faltantes_jugador = puntos_victoria - puntos_jugador
        puntos_faltantes_maquina = puntos_victoria - maquina_puntos
        return max(puntos_faltantes_jugador, puntos_faltantes_maquina)
    
    return 0 

def actualizar_puntajes(puntos_jugador: int, puntos_maquina: int, resultado_ronda: dict) -> tuple:
    '''
    Actualiza los puntajes del jugador y la máquina en base al resultado de una ronda.
    '''
    puntos_jugador += resultado_ronda.get('jugador', 0)
    puntos_maquina += resultado_ronda.get('maquina', 0)
    return puntos_jugador, puntos_maquina

def mostrar_puntajes(pantalla: pygame.Surface, puntos_jugador: int, puntos_maquina: int) -> None:
    '''
    Muestra los puntajes del jugador y de la máquina en la pantalla.
    '''
    fuente = pygame.font.Font(None, 36)
    texto_jugador = fuente.render(f"Puntaje Jugador: {puntos_jugador}", True, (0, 0, 0))
    texto_maquina = fuente.render(f"Puntaje Máquina: {puntos_maquina}", True, (0, 0, 0))
    pantalla.blit(texto_jugador, (50, 50))
    pantalla.blit(texto_maquina, (50, 100))

def mostrar_puntajes(pantalla: pygame.Surface, puntos_jugador: int, puntos_maquina: int) -> None:
    '''
    Muestra los puntajes del jugador y la máquina en la pantalla.
    '''
    fuente = pygame.font.Font(None, 36)
    texto_jugador = fuente.render(f"Puntaje Jugador: {puntos_jugador}", True, (0, 0, 0))
    texto_maquina = fuente.render(f"Puntaje Máquina: {puntos_maquina}", True, (0, 0, 0))
    pantalla.blit(texto_jugador, (50, 20))  # Posición del texto del jugador
    pantalla.blit(texto_maquina, (50, 60))  # Posición del texto de la máquina

def actualizar_puntajes(puntos_jugador: int, puntos_maquina: int, ganador: str, tipo: str) -> tuple:
    '''
    Actualiza los puntajes después de cada ronda.

    Parámetros:
        puntos_jugador (int): Puntaje actual del jugador.
        puntos_maquina (int): Puntaje actual de la máquina.
        ganador (str): "jugador" o "maquina", el ganador de la ronda.
        tipo (str): Tipo de jugada, "envido" o "truco".

    Retorno:
        tuple: (puntos_jugador, puntos_maquina) con los puntajes actualizados.
    '''
    if tipo == "envido":
        puntos_a_sumar = 2  # Por ahora, asumimos que se gana un envido simple
    elif tipo == "truco":
        puntos_a_sumar = 1  # Un truco simple vale 1 punto
    else:
        puntos_a_sumar = 0

    if ganador == "jugador":
        puntos_jugador += puntos_a_sumar
    elif ganador == "maquina":
        puntos_maquina += puntos_a_sumar

    return puntos_jugador, puntos_maquina