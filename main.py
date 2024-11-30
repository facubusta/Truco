import pygame
from funciones.mazo import *
from funciones.botones import *
from funciones.puntuacion import *
from funciones.juego import *

# Inicialización de pygame
pygame.init()

# Configuración de pantalla
ancho, alto = 800, 600
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Juego de Truco")

# Cargar la imagen de fondo
fondo = pygame.image.load("Truco\\Truco\\imagenes\\cartas\\bg.jpg")
fondo = pygame.transform.smoothscale(fondo, (ancho, alto))

# Variables iniciales
mazo, rutas_imagenes, valores_truco = crear_mazo()
imagenes_cartas = cargar_imagenes_cartas(rutas_imagenes)
mano_jugador, mano_maquina = repartir_cartas(mazo)

boton_truco = Boton(50, 550, 200, 30, "Truco")
boton_envido = Boton(250, 550, 200, 30, "Envido")
boton_mazo = Boton(450, 550, 200, 30, "Mazo")

puntos_jugador, puntos_maquina = 0, 0
jugando = True
turno_actual = "jugador"  # Define quién inicia la primera mano
cartas_jugadas = []  # Guarda las cartas jugadas en la ronda actual
puntos_truco = 0  # Puntos en juego por el Truco

# Bucle principal
while jugando:
    try:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

        # Dibujar fondo y elementos
        pantalla.blit(fondo, (0, 0))
        mostrar_puntajes(pantalla, puntos_jugador, puntos_maquina)

        # Mostrar cartas del jugador y la máquina
        carta_seleccionada = mostrar_cartas(pantalla, mano_jugador, imagenes_cartas, 300, es_jugador=True)
        mostrar_cartas(pantalla, mano_maquina, imagenes_cartas, 100, es_jugador=False)

        # Dibujar los botones
        boton_truco.dibujar(pantalla)
        boton_envido.dibujar(pantalla)
        boton_mazo.dibujar(pantalla)

        # Detectar clic en el botón Envido
        if boton_envido.detectar_clic() and turno_actual == "jugador":
            print("Botón Envido presionado")
            puntos_jugador, puntos_maquina = manejar_envido(puntos_jugador, puntos_maquina, mano_jugador, mano_maquina)

        # Detectar clic en el botón Truco
        if boton_truco.detectar_clic():
            print("Botón Truco presionado")
            puntos_truco = manejar_truco(turno_actual)
            if puntos_truco > 0:
                print(f"El Truco fue aceptado. Se jugará por {puntos_truco} puntos.")
            else:
                print("El Truco no fue aceptado.")

        # Detectar clic en el botón Mazo
        if boton_mazo.detectar_clic():
            print("Botón Mazo presionado")
            if turno_actual == "jugador":
                print("Te fuiste al mazo. La máquina gana 2 puntos.")
                puntos_maquina += 2
            else:
                print("La máquina se fue al mazo. Sumás 2 puntos.")
                puntos_jugador += 2
            # Reiniciar la ronda
            mazo, rutas_imagenes, valores_truco = crear_mazo()
            mano_jugador, mano_maquina = repartir_cartas(mazo)
            cartas_jugadas = []
            turno_actual = "jugador"  # Reinicia el turno
            puntos_truco = 0  # Reinicia el valor del Truco
            continue  # Salta a la siguiente iteración

        # Manejo de selección de carta
        if carta_seleccionada:
            if turno_actual == "jugador":
                mano_jugador.remove(carta_seleccionada)
                carta_maquina = jugar_maquina(mano_maquina, carta_seleccionada)
                mano_maquina.remove(carta_maquina)
                cartas_jugadas.append((carta_seleccionada, carta_maquina))
            else:
                carta_maquina = jugar_maquina(mano_maquina)
                mano_maquina.remove(carta_maquina)
                carta_seleccionada = mostrar_cartas(pantalla, mano_jugador, imagenes_cartas, 300, es_jugador=True)
                if carta_seleccionada:
                    mano_jugador.remove(carta_seleccionada)
                    cartas_jugadas.append((carta_seleccionada, carta_maquina))

            # Evaluar quién ganó la mano
            ganador_mano = evaluar_mano(cartas_jugadas[-1], valores_truco)
            if ganador_mano == "jugador":
                print("Ganaste esta mano.")
                turno_actual = "jugador"
            elif ganador_mano == "maquina":
                print("La máquina ganó esta mano.")
                turno_actual = "maquina"
            else:
                print("Empate en esta mano.")
                turno_actual = "jugador"  # En caso de empate, el jugador sigue siendo mano

        # Fin de ronda
        if not mano_jugador and not mano_maquina:
            print("¡Fin de la ronda!")

            # Calcular ganadores de cada mano
            ganadores_manos = {"jugador": 0, "maquina": 0}
            for carta_jugador, carta_maquina in cartas_jugadas:
                ganador_mano = evaluar_mano((carta_jugador, carta_maquina), valores_truco)
                if ganador_mano == "jugador":
                    ganadores_manos["jugador"] += 1
                elif ganador_mano == "maquina":
                    ganadores_manos["maquina"] += 1

            # Determinar ganador de la ronda
            ganador_ronda = determinar_ganador_ronda(ganadores_manos)

            if ganador_ronda == "jugador":
                puntos_jugador += puntos_truco  # Sumar puntos del Truco
                print(f"Ganaste la ronda y sumás {puntos_truco} puntos.")
            elif ganador_ronda == "maquina":
                puntos_maquina += puntos_truco  # Sumar puntos del Truco
                print(f"La máquina ganó la ronda y suma {puntos_truco} puntos.")
            else:
                print("La ronda terminó en empate.")

            # Reiniciar la ronda
            mazo, rutas_imagenes, valores_truco = crear_mazo()
            mano_jugador, mano_maquina = repartir_cartas(mazo)
            cartas_jugadas = []
            turno_actual = "jugador"  # Reinicia el turno
            puntos_truco = 0  # Reinicia el valor del Truco

        # Verificar fin del juego
        if puntos_jugador >= 15 or puntos_maquina >= 15:
            print("¡Juego finalizado!")
            if puntos_jugador >= 15:
                print("¡Ganaste la partida!")
            else:
                print("La máquina ganó la partida.")
            jugando = False

        # Actualizar pantalla
        pygame.display.flip()

    except Exception as e:
        print(f"Error: {e}")

pygame.quit()