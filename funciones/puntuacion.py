import pygame
import csv
import os
from funciones.paletas_colores import *
from funciones.botones import *

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

def guardar_puntaje(nombre: str, puntaje: int, archivo: str = "ranking.csv") -> None:
    """
    Guarda el puntaje del jugador en un archivo CSV.
    Si el jugador ya existe, actualiza su puntaje si es mayor al anterior.
    """
    ranking = []
    archivo_completo = os.path.join("C:\\Users\\pc\\Desktop\\utn facu\\Programacion_1\\Git\\Truco\\truco\\archivos", archivo)

    # Leer el archivo existente
    if os.path.exists(archivo_completo):
        with open(archivo_completo, "r", newline="", encoding="utf-8") as file:
            lector = csv.reader(file)
            ranking = list(lector)

    # Actualizar o agregar al ranking
    actualizado = False
    for fila in ranking:
        if fila[0] == nombre:
            fila[1] = str(int(fila[1]) + 1)
            actualizado = True
            break
    if not actualizado:
        ranking.append([nombre, str(puntaje)])

    # Guardar los datos actualizados
    with open(archivo_completo, "w", newline="", encoding="utf-8") as file:
        escritor = csv.writer(file)
        escritor.writerows(ranking)

def mostrar_ranking(pantalla: pygame.Surface, fondo: pygame.Surface, archivo: str = "ranking.csv") -> None:

    """
    Muestra el ranking en la pantalla.
    """
    fuente = pygame.font.Font(None, 36)
    archivo_completo = os.path.join("C:\\Users\\pc\\Desktop\\utn facu\\Programacion_1\\Git\\Truco\\truco\\archivos", archivo)

    # Leer el ranking
    if os.path.exists(archivo_completo):
        with open(archivo_completo, "r", newline="", encoding="utf-8") as file:
            lector = csv.reader(file)
            ranking = sorted(lector, key=lambda x: int(x[1]), reverse=True)  # Ordenar por puntaje descendente
    else:
        ranking = []

    # Bucle para mostrar el ranking
    mostrando = True
    while mostrando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:  # Salir con Enter
                mostrando = False

        pantalla.blit(fondo, (0, 0))  # Dibuja el fondo

        # Mostrar título y ranking
        titulo = fuente.render("Puntaje historico", True, OCRE)
        pantalla.blit(titulo, (300, 50))
        y = 100
        for i, (nombre, puntaje) in enumerate(ranking[:10], start=1):  # Mostrar solo el top 10
            texto = fuente.render(f"{i}. {nombre} - {puntaje}", True, BLANCO)
            pantalla.blit(texto, (200, y))
            y += 40
          
        volver_a_menu = Boton(300, 500, 200, 50, "Volver a menu", VERDE_OLIVA)
        volver_a_menu.dibujar(pantalla)
        if volver_a_menu.detectar_clic():
            break

        pygame.display.flip()

def pedir_nombre(pantalla: pygame.Surface, ancho: int, alto: int) -> str:
    """
    Solicita al usuario ingresar su nombre mediante una interfaz gráfica.

    Parámetros:
        pantalla (pygame.Surface): La superficie de pygame donde se renderizará la entrada.
        ancho (int): Ancho de la pantalla.
        alto (int): Alto de la pantalla.

    Retorno:
        str: Nombre ingresado por el usuario.
    """
    pygame.font.init()
    pantalla.fill(LAVANDA)
    fuente = pygame.font.Font(None, 36)

    # Renderizar el título
    texto_titulo = fuente.render("Ingresa tu nombre", True, (255, 255, 255))  # BLANCO
    pantalla.blit(texto_titulo, (ancho // 2 - texto_titulo.get_width() // 2, 100))

    # Variables para el nombre
    nombre = ""
    continuar = True
    input_rect = pygame.Rect(325, 200, 140, 32)

    while continuar:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif evt.key == pygame.K_RETURN or evt.key == pygame.K_KP_ENTER:
                    continuar = False
                else:
                    nombre += evt.unicode

        # Actualizar pantalla
        pantalla.fill(VINO)  # Fondo
        pantalla.blit(texto_titulo, (ancho // 2 - texto_titulo.get_width() // 2, 100))  # Título

        # Rectángulo de entrada
        pygame.draw.rect(pantalla, (VERDE_OLIVA), input_rect) 
        if  input_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(pantalla, (BLANCO), input_rect, 2)
        text_surface = fuente.render(nombre, True, (255, 255, 255))  # Texto en blanco
        pantalla.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.flip()

    return nombre

def seleccionar_puntos(pantalla: pygame.Surface, ancho: int, alto: int) -> int:
    """
    Muestra una pantalla para seleccionar la cantidad de puntos a jugar (15 o 30).
    
    Args:
        pantalla (pygame.Surface): La pantalla donde se dibujará el menú.
        ancho (int): Ancho de la ventana.
        alto (int): Alto de la ventana.

    Returns:
        int: La cantidad de puntos seleccionados (15 o 30).
    """
    pantalla.fill((0, 128, 0))
    fuente = pygame.font.Font(None, 50)
    texto_titulo = fuente.render("¿A cuánto querés jugar?", True, (255, 255, 255))  # BLANCO
    pantalla.blit(texto_titulo, (ancho // 2 - texto_titulo.get_width() // 2, 100))

    boton_quince = Boton(ancho // 2 - 150, 200, 300, 50, "Jugar a 15 puntos", (189, 183, 107))  # VERDE_OLIVA
    boton_treinta = Boton(ancho // 2 - 150, 300, 300, 50, "Jugar a 30 puntos", (189, 183, 107))  # VERDE_OLIVA

    seleccion = 0

    while seleccion == 0:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Redibujar pantalla
        pantalla.fill((0, 128, 0))
        pantalla.blit(texto_titulo, (ancho // 2 - texto_titulo.get_width() // 2, 100))
        boton_quince.dibujar(pantalla)
        boton_treinta.dibujar(pantalla)

        # Detectar clic en los botones
        if boton_quince.detectar_clic():
            seleccion = 15
        elif boton_treinta.detectar_clic():
            seleccion = 30

        pygame.display.flip()

    return seleccion

def mostrar_menu_principal(pantalla: pygame.Surface, fondo: pygame.Surface) -> None:
    """
    Muestra el menú principal con las opciones de Jugar o Ver Ranking.
    """
    mostrar_menu = True
    while mostrar_menu:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        pantalla.blit(fondo, (0, 0))  # Fondo del menú
        titulo = pygame.font.Font(None, 48).render("Menú Principal", True, (255, 255, 255))
        pantalla.blit(titulo, (300, 100))

        boton_ranking = Boton(300, 250, 200, 50, "Ver Ranking")
        boton_jugar = Boton(300, 350, 200, 50, "Jugar")
        boton_ranking.dibujar(pantalla)
        boton_jugar.dibujar(pantalla)

        if boton_ranking.detectar_clic():
            mostrar_ranking(pantalla, fondo)  # Llama a la función del ranking

        if boton_jugar.detectar_clic():
            mostrar_menu = False  # Sal del menú para iniciar el juego

        pygame.display.flip()