import random
import os
import pygame



def crear_mazo() -> tuple:
    '''
    Crea y devuelve un mazo de cartas mezcladas, sus rutas de imágenes y los valores del truco.
    '''
    palos = ("espadas", "bastos", "oros", "copas")
    valores = (1, 2, 3, 4, 5, 6, 7, 10, 11, 12)
    mazo = []
    rutas_imagenes = {}
    
    for palo in palos:
        for valor in valores:
            carta = (valor, palo)  # Formato de carta como tupla
            ruta_imagen = os.path.join(os.path.dirname(__file__), "..", "imagenes", "cartas", f"{valor} de {palo}.jpg")
            mazo.append(carta)
            rutas_imagenes[carta] = ruta_imagen  # Clave en formato (valor, palo)
    
    random.shuffle(mazo)  # Mezclar el mazo
    valores_truco = cargar_valores_truco("archivos/valores_truco.txt")
    return mazo, rutas_imagenes, valores_truco

def cargar_imagenes_cartas(rutas_imagenes: dict) -> dict:
    '''
    Carga las imágenes de las cartas desde las rutas proporcionadas.
    '''
    imagenes = {}
    for carta, ruta in rutas_imagenes.items():
        
        imagenes[carta] = pygame.image.load(ruta)
    
    ruta_boca_abajo = os.path.join(os.path.dirname(__file__), "..", "imagenes", "cartas", "carta_boca_abajo.jpg")
    imagenes["boca_abajo"] = pygame.image.load(ruta_boca_abajo)

    return imagenes

def repartir_cartas(mazo: list) -> tuple:
    '''
    Reparte tres cartas para el jugador y tres para la máquina.
    '''
    jugador = [mazo.pop() for _ in range(3)]  # Extraer 3 cartas para el jugador
    maquina = [mazo.pop() for _ in range(3)]  # Extraer 3 cartas para la máquina
    return jugador, maquina

def cargar_valores_truco(archivo: str) -> dict:
    '''
    Carga los valores de las cartas del truco desde un archivo de texto.
    '''
    valores_truco = {}
    ruta = os.path.join(os.path.dirname(__file__), "..", archivo)
    with open(ruta, "r") as f:
        for linea in f:
            carta, valor = linea.strip().split(",")
            valores_truco[carta] = int(valor)
    return valores_truco

def mostrar_cartas(pantalla: pygame.Surface, mano: list, imagenes: dict, y: int, es_jugador: bool) -> tuple:
    '''
    Dibuja las cartas en pantalla y permite la selección de una carta si es del jugador.
    '''
    x = 50
    carta_seleccionada = None

    for carta in mano:
        carta_rect = pygame.Rect(x, y, 100, 150)  # Area de la carta
        
        if es_jugador:
            pantalla.blit(imagenes[carta], (x, y)) 
        else:
            pantalla.blit(imagenes["boca_abajo"], (x, y))

        # Detectar clic
        if es_jugador and carta_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(pantalla, (255, 0, 0), carta_rect, 3)  # Resaltar la carta con un borde rojo
            if pygame.mouse.get_pressed()[0]:  # Si se hace clic con el botón izquierdo
                carta_seleccionada = carta

        x += 150  

    return carta_seleccionada

def arrastrar_carta(pantalla: pygame.Surface, carta_seleccionada: str, imagenes: dict, y: int) -> None:
    '''
    Permite al jugador arrastrar la carta seleccionada a una nueva posición.
    '''
    x, y_pos = pygame.mouse.get_pos()  # Obtener la posición del ratón

    # Dibujar la carta en la nueva posición del ratón
    pantalla.blit(imagenes[carta_seleccionada], (x - 50, y_pos - 75))  # Ajusta la posición para centrar la carta al clic

def mostrar_ganador(pantalla: pygame.Surface, carta_ganadora: str, imagenes: dict, x: int, y: int) -> None:
    '''
    Muestra la carta ganadora encima de la carta perdedora.
    '''
    pantalla.blit(imagenes[carta_ganadora], (x, y))  # Muestra la carta ganadora encima

