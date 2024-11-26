import pygame
from funciones.mazo import *
from funciones.botones import *
from funciones.puntuacion import *
from funciones.juego import *

# Inicialización de pygame
pygame.init()

# Tamaño de la pantalla
ancho = 800
alto = 600
pantalla = pygame.display.set_mode((ancho, alto))

# Llamada para crear el mazo y obtener las rutas de las imágenes
mazo, rutas_imagenes, valores_truco = crear_mazo()

# Ahora pasamos el diccionario rutas_imagenes a cargar_imagenes_cartas
imagenes_cartas = cargar_imagenes_cartas(rutas_imagenes)

# Crear botones
boton_truco = Boton(300, 500, 200, 50, "Truco")
boton_envido = Boton(300, 550, 200, 50, "Envido")

# Repartir cartas
mano_jugador, mano_maquina = repartir_cartas(mazo)

# Variables iniciales
carta_ganadora = None
cartas_jugadas = []  # Almacena las cartas jugadas en la ronda
jugando = True
puntos_jugador = 0
puntos_maquina = 0

# Bucle principal del juego
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

    # Rellenar el fondo de la pantalla
    pantalla.fill((255, 255, 255))

    # Mostrar las cartas del jugador
    carta_seleccionada = mostrar_cartas(pantalla, mano_jugador, imagenes_cartas, 400, es_jugador=True)

    # Mostrar las cartas de la máquina
    mostrar_cartas(pantalla, mano_maquina, imagenes_cartas, 100, es_jugador=False)

    # Dibujar los botones
    boton_truco.dibujar(pantalla)
    boton_envido.dibujar(pantalla)

    # Detectar clic en los botones
    if boton_truco.detectar_clic():
        print("Botón Truco presionado")
        puntos_jugador, puntos_maquina = manejar_truco(puntos_jugador, puntos_maquina)  # Lógica del truco
    
    if boton_envido.detectar_clic():
        print("Botón Envido presionado")
        puntos_jugador, puntos_maquina = manejar_envido(puntos_jugador, puntos_maquina, mano_jugador, mano_maquina)

   # Si el jugador selecciona una carta
    if carta_seleccionada:
        if mano_maquina:  # Verificar que la máquina aún tenga cartas
            carta_maquina = mano_maquina.pop(0)  # La máquina juega la primera carta de su mano
            mano_jugador.remove(carta_seleccionada)
            print(f"Jugador jugó: {carta_seleccionada}, Máquina jugó: {carta_maquina}")
        else:
            print("No quedan cartas en la mano de la máquina.")

    # Si no quedan cartas en ninguna mano, finalizar la partida
    if not mano_jugador and not mano_maquina:
        print("¡Fin de la partida!")
        jugando = False

    # Actualizar la pantalla
    pygame.display.flip()

# Finalizar pygame
pygame.quit()