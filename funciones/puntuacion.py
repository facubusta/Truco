import pygame
from funciones.paletas_colores import *

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
    elif tipo_envido == "envido envido no querido":
        return 3 
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

def mostrar_puntajes(pantalla: pygame.Surface, puntos_jugador: int, puntos_maquina: int) -> None:
    '''
    Muestra los puntajes del jugador y la máquina en la pantalla.
    '''
    fuente = pygame.font.Font(None, 36)
    texto_jugador = fuente.render(f"Jugador: {puntos_jugador}", True, MENTA)
    texto_maquina = fuente.render(f"Máquina: {puntos_maquina}", True, MENTA)
    pantalla.blit(texto_jugador, (50, 20))  # Posición del texto del jugador
    pantalla.blit(texto_maquina, (50, 60))  # Posición del texto de la máquina
