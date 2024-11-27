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