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

    # Mostrar puntajes en la pantalla
    mostrar_puntajes(pantalla, puntos_jugador, puntos_maquina)

    # Mostrar las cartas del jugador y permitir selección
    carta_seleccionada = mostrar_cartas(pantalla, mano_jugador, imagenes_cartas, 400, es_jugador=True)

    # Mostrar las cartas de la máquina boca abajo
    mostrar_cartas(pantalla, mano_maquina, imagenes_cartas, 100, es_jugador=False)

    # Preguntar si se canta envido (al inicio de la mano)
    if not cartas_jugadas:  # Solo preguntar al inicio de la ronda
        puntos_jugador, puntos_maquina = manejar_envido(puntos_jugador, puntos_maquina, mano_jugador, mano_maquina)

    # Si el jugador selecciona una carta
    if carta_seleccionada:
        # La máquina juega automáticamente la primera carta de su mano
        carta_maquina = mano_maquina.pop(0)
        mano_jugador.remove(carta_seleccionada)

        # Determinar el ganador de la ronda
        if valores_truco[carta_seleccionada] > valores_truco[carta_maquina]:
            ganador = "jugador"
        else:
            ganador = "maquina"

        # Actualizar los puntos del truco
        puntos_jugador, puntos_maquina = actualizar_puntajes(puntos_jugador, puntos_maquina, ganador, tipo="truco")

        print(f"Jugador jugó: {carta_seleccionada}, Máquina jugó: {carta_maquina}")
        print(f"Ganador de la ronda: {ganador}")

    # Actualizar la pantalla
    pygame.display.flip()

# Finalizar pygame
pygame.quit()