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
    Actualiza los puntajes después de cada ronda
    '''
    puntos_a_sumar = {
        "truco": 1,
        "retruco": 3,
        "vale cuatro": 4,
        "envido": 2,
        "envido no querido": 1
                         }.get(tipo, 0)

    if ganador == "jugador":
        puntos_jugador += puntos_a_sumar
    elif ganador == "maquina":
        puntos_maquina += puntos_a_sumar

    return puntos_jugador, puntos_maquina

def mostrar_mensaje(pantalla: pygame.surface, mensaje: str, x: int, y: int):
    fuente = pygame.font.Font(None, 48)
    texto = fuente.render(mensaje, True, (0, 0, 0))  # Texto negro
    rect = texto.get_rect(center=(x, y))
    pygame.draw.rect(pantalla, (255, 255, 255), rect.inflate(20, 20))  # Fondo blanco para el mensaje
    pantalla.blit(texto, rect)


'''# Función para calcular puntos de Envido
def calcular_envido(cartas):
    por_palo = {}
    figuras = {'11', '12', '10'}
    for valor, palo in cartas:
        if valor in figuras:
            puntos = 0
        else:
            puntos = int(valor) if valor.isdigit() else 0
        por_palo[palo] = por_palo.get(palo, []) + [puntos]
    
    max_envido = 0
    for palo, puntos in por_palo.items():
        if len(puntos) > 1:
            max_envido = max(max_envido, sum(sorted(puntos, reverse=Tru'''