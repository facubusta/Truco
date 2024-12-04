import pygame

class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_boton=(0, 128, 0), color_texto=(255, 255, 255)):
        """
        Constructor para inicializar los atributos del botón.
        """
        self.rect = pygame.Rect(x, y, ancho, alto)  # Rectángulo del botón
        self.texto = texto  # Texto que mostrará el botón
        self.color_boton = color_boton  # Color del botón
        self.color_texto = color_texto  # Color del texto
        self.fuente = pygame.font.Font(None, 36)  # Fuente para el texto
        self.superficie_texto = self.fuente.render(self.texto, True, self.color_texto)  # Crear el texto como superficie

    def dibujar(self, pantalla):
        """
        Dibuja el botón en la pantalla.
        """
        pygame.draw.rect(pantalla, self.color_boton, self.rect)  # Dibujar el rectángulo del botón
        # Dibujar el texto del botón centrado
        pantalla.blit(self.superficie_texto, (self.rect.x + (self.rect.width - self.superficie_texto.get_width()) // 2, 
                                              self.rect.y + (self.rect.height - self.superficie_texto.get_height()) // 2))

    def detectar_clic(self) -> bool:
        """
        Detecta si el botón fue clickeado.

        Retorna:
            True si el botón fue clickeado, False si no.
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        return False
    
def manejar_irse_al_mazo(turno_actual: str, envido_jugado: bool, inicio_ronda: bool, puntos_jugador: int,
                          puntos_maquina: int) -> tuple:
    """
    Maneja la lógica de "irse al mazo" y actualiza los puntajes.

    Parámetros:
        turno_actual (str): Quién está en turno ("jugador" o "maquina").
        envido_jugado (bool): Si el envido ya fue jugado.
        inicio_ronda (bool): Si la ronda fue iniciada por la máquina o el jugador.
        puntos_jugador (int): Puntaje actual del jugador.
        puntos_maquina (int): Puntaje actual de la máquina.

    Retorno:
        tuple: (puntos_jugador, puntos_maquina).
    """
    if turno_actual == "jugador" and envido_jugado:
        print("Te fuiste al mazo. La máquina gana 1 punto.")
        puntos_maquina += 1
    elif turno_actual == "jugador" and not inicio_ronda:
        print("Te fuiste al mazo. La máquina gana 1 punto.")
        puntos_maquina += 1
    elif turno_actual == "jugador" and not envido_jugado:
        print("Te fuiste al mazo. La máquina gana 2 puntos.")
        puntos_maquina += 2
    elif turno_actual == "maquina" and envido_jugado:
        print("La máquina se fue al mazo. Sumás 1 punto.")
        puntos_jugador += 1
    elif turno_actual == "maquina" and not inicio_ronda:
        print("La máquina se fue al mazo. Sumás 1 punto.")
        puntos_jugador += 1
    else:
        print("La máquina se fue al mazo. Sumás 2 puntos.")
        puntos_jugador += 2

    return puntos_jugador, puntos_maquina