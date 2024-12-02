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
pygame.display.set_caption("Truco Argentino")

# Cargar la imagen de fondo
fondo = pygame.image.load("Truco\\Truco\\imagenes\\cartas\\bg.jpg")
fondo = pygame.transform.smoothscale(fondo, (ancho, alto))

# Variables iniciales
mazo, rutas_imagenes, valores_truco = crear_mazo()
imagenes_cartas = cargar_imagenes_cartas(rutas_imagenes)
mano_jugador, mano_maquina = repartir_cartas(mazo)

boton_truco = Boton(200, 550, 200, 30, "Truco")
boton_envido = Boton(400, 550, 200, 30, "Envido")
boton_mazo = Boton(600, 550, 200, 30, "Irse al Mazo")

puntos_jugador, puntos_maquina = 0, 0
jugando = True
turno_actual = "jugador"  # Define quién inicia la primera mano
cartas_jugadas = []  # Guarda las cartas jugadas en la ronda actual
puntos_truco = 0  # Puntos en juego por el Truco
envido_jugado = False  # Controla si el Envido ya fue jugado en la ronda
ronda_activa = True  # Controla si la ronda está activa
manos_ganadas = {"jugador": 0, "maquina": 0}  # Cuenta las manos ganadas por cada jugador

# Función para reiniciar la ronda
def reiniciar_ronda():
    global mazo, mano_jugador, mano_maquina, cartas_jugadas, turno_actual, manos_ganadas, puntos_truco, envido_jugado, ronda_activa
    print("Comienza una nueva ronda.")
    mazo, rutas_imagenes, valores_truco = crear_mazo()
    mano_jugador, mano_maquina = repartir_cartas(mazo)
    cartas_jugadas = []
    turno_actual = "jugador"  # Reinicia el turno al jugador por defecto
    manos_ganadas = {"jugador": 0, "maquina": 0}
    puntos_truco = 0
    envido_jugado = False
    ronda_activa = True
    pygame.time.delay(500)

# Bucle principal
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

        # Detectar clic en cartas solo si la ronda está activa y es el turno del jugador
        if evento.type == pygame.MOUSEBUTTONDOWN and ronda_activa and turno_actual == "jugador":
            carta_seleccionada = mostrar_cartas(pantalla, mano_jugador, imagenes_cartas, 300, es_jugador=True)

            if carta_seleccionada and carta_seleccionada in mano_jugador:
                # El jugador juega su carta
                mano_jugador.remove(carta_seleccionada)
                carta_maquina = jugar_maquina(mano_maquina, carta_seleccionada)
                mano_maquina.remove(carta_maquina)
                cartas_jugadas.append((carta_seleccionada, carta_maquina))
                print(f"Jugaste: {carta_seleccionada}, La máquina jugó: {carta_maquina}")

                # Evaluar quién ganó la mano
                ganador_mano = evaluar_mano(cartas_jugadas[-1], valores_truco)
                if ganador_mano == "jugador":
                    print("Ganaste esta mano.")
                    manos_ganadas["jugador"] += 1
                    turno_actual = "jugador"
                elif ganador_mano == "maquina":
                    print("La máquina ganó esta mano.")
                    manos_ganadas["maquina"] += 1
                    turno_actual = "maquina"
                else:
                    print("Empate en esta mano.")
                    turno_actual = "jugador"

                # Verificar si alguien ganó dos manos
                if manos_ganadas["jugador"] == 2 or manos_ganadas["maquina"] == 2:
                    ronda_activa = False
                    puntos_jugador, puntos_maquina = determinar_ganador_final(
                        puntos_jugador, puntos_maquina, cartas_jugadas, manos_ganadas, puntos_truco
                    )
                    reiniciar_ronda()

    # Turno de la máquina
    if turno_actual == "maquina" and ronda_activa:
        pygame.time.delay(500)  # Simular un retraso para la jugada de la máquina
        
        # Verificar si es una nueva jugada o una respuesta
        if not cartas_jugadas or cartas_jugadas[-1][1] is not None:  # No hay jugada incompleta
            carta_maquina = mano_maquina.pop(0)  # La máquina juega su carta más alta disponible
            cartas_jugadas.append((None, carta_maquina))  # La máquina comienza la jugada
            print(f"La máquina jugó: {carta_maquina}")
            turno_actual = "jugador"  # Cambia el turno al jugador para responder
        elif cartas_jugadas[-1][0] is not None and cartas_jugadas[-1][1] is None:
            # Responder a la jugada del jugador
            carta_jugador = cartas_jugadas[-1][0]
            carta_maquina = jugar_maquina(mano_maquina, carta_jugador)  # Jugar en respuesta
            mano_maquina.remove(carta_maquina)
            cartas_jugadas[-1] = (carta_jugador, carta_maquina)  # Completar la jugada
            print(f"La máquina jugó: {carta_maquina}")

            # Evaluar quién ganó la mano
            ganador_mano = evaluar_mano(cartas_jugadas[-1], valores_truco)
            if ganador_mano == "jugador":
                print("Ganaste esta mano.")
                manos_ganadas["jugador"] += 1
                turno_actual = "jugador"  # El jugador comienza la siguiente jugada
            elif ganador_mano == "maquina":
                print("La máquina ganó esta mano.")
                manos_ganadas["maquina"] += 1
                turno_actual = "maquina"  # La máquina sigue jugando
            else:
                print("Empate en esta mano.")
                turno_actual = "jugador"  # Por defecto, turno al jugador en caso de empate

            # Verificar si alguien ganó dos manos
            if manos_ganadas["jugador"] == 2 or manos_ganadas["maquina"] == 2:
                ronda_activa = False
                puntos_jugador, puntos_maquina = determinar_ganador_final(
                    puntos_jugador, puntos_maquina, cartas_jugadas, manos_ganadas, puntos_truco
                )
                reiniciar_ronda()

    # Dibujar fondo y elementos
    pantalla.blit(fondo, (0, 0))
    mostrar_puntajes(pantalla, puntos_jugador, puntos_maquina)

    # Mostrar cartas del jugador y la máquina
    mostrar_cartas(pantalla, mano_jugador, imagenes_cartas, 300, es_jugador=True)
    mostrar_cartas(pantalla, mano_maquina, imagenes_cartas, 100, es_jugador=False)

    # Dibujar los botones
    boton_truco.dibujar(pantalla)
    boton_envido.dibujar(pantalla)
    boton_mazo.dibujar(pantalla)

    # Detectar clic en el botón Envido
    if boton_envido.detectar_clic() and turno_actual == "jugador" and not envido_jugado:
        print("Botón Envido presionado")
        puntos_jugador, puntos_maquina = manejar_envido(puntos_jugador, puntos_maquina, mano_jugador, mano_maquina)
        envido_jugado = True

    # Detectar clic en el botón Truco
    if boton_truco.detectar_clic() and turno_actual == "jugador":
        print("Botón Truco presionado")
        puntos_truco = manejar_truco(turno_actual)
        if puntos_truco > 0:
            print(f"El Truco fue aceptado. Se jugará por {puntos_truco} puntos.")
        else:
            print("El Truco no fue aceptado.")

    # Detectar clic en el botón Mazo
    if boton_mazo.detectar_clic() and ronda_activa:
        print("Clic en el botón Mazo detectado")
        ronda_activa = False
        if turno_actual == "jugador":
            print("Te fuiste al mazo. La máquina gana 2 puntos.")
            puntos_maquina += 2
        else:
            print("La máquina se fue al mazo. Sumás 2 puntos.")
            puntos_jugador += 2
        reiniciar_ronda()

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

pygame.quit()