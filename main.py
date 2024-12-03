import pygame
from funciones.mazo import *
from funciones.botones import *
from funciones.puntuacion import *
from funciones.juego import *
from funciones.paletas_colores import *

# Inicialización de pygame
pygame.init()

# Configuración de pantalla
ancho, alto = 800, 600
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Truco Argentino")

fondo_menu = pygame.image.load("Truco\\truco\\imagenes\\cartas\\menu.jpg")
fondo_menu = pygame.transform.smoothscale(fondo_menu, (ancho, alto))

# Mostrar el menú principal
mostrar_menu_principal(pantalla, fondo_menu)

# Llamar a la función al inicio del juego
nombre = pedir_nombre(pantalla, ancho, alto)

# Selección de puntos antes de iniciar el juego
seleccion = seleccionar_puntos(pantalla, ancho, alto)

# Cargar la imagen de fondo
fondo = pygame.image.load("Truco\\Truco\\imagenes\\cartas\\bg.jpg")
fondo = pygame.transform.smoothscale(fondo, (ancho, alto))

# Variables iniciales
mazo, rutas_imagenes, valores_truco = crear_mazo()
imagenes_cartas = cargar_imagenes_cartas(rutas_imagenes)
mano_jugador, mano_maquina = repartir_cartas(mazo)

boton_truco = Boton(100, 550, 200, 30, "Truco")
boton_envido = Boton(300, 550, 200, 30, "Envido")
boton_mazo = Boton(500, 550, 200, 30, "Mazo")

puntos_jugador, puntos_maquina = 0, 0
jugando = True
turno_actual = "jugador"  # Define quién inicia la primera mano
cartas_jugadas = []  # Guarda las cartas jugadas en la ronda actual
puntos_truco = 0  # Puntos en juego por el Truco
envido_jugado = False  # Controla si el Envido ya fue jugado en la ronda
ronda_activa = True  # Controla si la ronda está activa
manos_ganadas = {"jugador": 0, "maquina": 0}  # Cuenta las manos ganadas por cada jugador
inicia_ronda = "jugador"  # Alterna quién inicia la ronda
cartas_maquina = []
inicio_ronda = True
empate = 0
ganador_primera = ""
canto_actual = ""
respuesta = False
turno_truco = "jugador"

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
                if len(cartas_maquina) == 0:
                    carta_maquina = jugar_maquina(mano_maquina, carta_seleccionada)
                    mano_maquina.remove(carta_maquina)
                    cartas_jugadas.append((carta_seleccionada, carta_maquina))
                    print(f"Jugaste: {carta_seleccionada}, La máquina jugó: {carta_maquina}")
                else:
                    cartas_jugadas.append((carta_seleccionada, cartas_maquina[0]))
                    print(f"Jugaste: {carta_seleccionada}, La máquina jugó: {cartas_maquina[0]}")

                # Evaluar quién ganó la mano
                ganador_mano = evaluar_mano(cartas_jugadas[-1], valores_truco)
                if ganador_mano == "jugador":
                    print("Ganaste esta mano.")
                    manos_ganadas["jugador"] += 1
                    turno_actual = "jugador"
                    if inicio_ronda == True or empate > 0:
                        ganador_primera = "jugador"
                elif ganador_mano == "maquina":
                    print("La máquina ganó esta mano.")
                    manos_ganadas["maquina"] += 1
                    turno_actual = "maquina"
                    if inicio_ronda == True or empate > 0:
                        ganador_primera = "maquina"
                else:
                    print("Empate en esta mano.")
                    turno_actual = "jugador"
                    empate += 1
                cartas_maquina = []
                inicio_ronda = False
                #inicia_ronda = "maquina" if inicia_ronda == "jugador" else "jugador"

    # Verificar si alguien ganó dos manos
    if manos_ganadas["jugador"] == 2 or manos_ganadas["maquina"] == 2 or (empate > 0 and (manos_ganadas["jugador"] == 1 or manos_ganadas["maquina"] == 1)):
        ronda_activa = False
        puntos_jugador, puntos_maquina = determinar_ganador_final(
        puntos_jugador, puntos_maquina, ganador_primera, manos_ganadas, puntos_truco)
        reiniciar_ronda(mazo, mano_jugador, mano_maquina, cartas_jugadas, manos_ganadas, inicia_ronda)
        inicio_ronda = True
        inicia_ronda = "maquina" if inicia_ronda == "jugador" else "jugador"
        turno_actual = inicia_ronda
        ronda_activa = True
        envido_jugado = False
        empate = 0
    else:
        # Turno de la máquina
        if (turno_actual == "maquina" or (inicia_ronda == "maquina" and inicio_ronda == True)) and ronda_activa:
            turno_actual = manejar_turno_maquina(mano_maquina, cartas_jugadas, valores_truco, turno_actual, manos_ganadas, cartas_maquina)
            inicio_ronda = False

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
        canto_actual, respuesta, turno_truco = gestionar_truco_interfaz(pantalla, turno_truco, canto_actual, respuesta)

        '''if truco_terminado:
            print(f"El Truco fue resuelto. Puntos actuales - jugador: {puntos_jugador}, maquina: {puntos_maquina}.")
            inicio_ronda = True
            inicia_ronda = "maquina" if inicia_ronda == "jugador" else "jugador"
            turno_actual = inicia_ronda
            ronda_activa = True
            envido_jugado = False
            empate = 0 ''' 

    # Detectar clic en el botón Mazo
    if boton_mazo.detectar_clic() and ronda_activa:
        print("Clic en el botón Mazo detectado")
        ronda_activa = False
        if turno_actual == "jugador" and envido_jugado == True:
            print("Te fuiste al mazo. La máquina gana 1 punto.")
            puntos_maquina += 1
        elif turno_actual == "jugador" and inicio_ronda == False:
            print("Te fuiste al mazo. La máquina gana 1 punto.")
            puntos_maquina += 1
        elif turno_actual == "jugador" and envido_jugado == False:
            print("Te fuiste al mazo. La máquina gana 2 puntos.")
            puntos_maquina += 2
        elif turno_actual == "maquina" and envido_jugado == True:
            print("La máquina se fue al mazo. Sumás 1 punto.")
            puntos_jugador += 1
        elif turno_actual == "maquina" and inicio_ronda == False:
            print("La máquina se fue al mazo. Sumás 1 punto.")
            puntos_jugador += 1
        else:
            print("La máquina se fue al mazo. Sumás 2 puntos.")
            puntos_jugador += 1

        reiniciar_ronda(mazo, mano_jugador, mano_maquina, cartas_jugadas, manos_ganadas, inicia_ronda)
        inicio_ronda = True
        inicia_ronda = "maquina" if inicia_ronda == "jugador" else "jugador"
        turno_actual = inicia_ronda
        ronda_activa = True
        envido_jugado = False
        empate = 0

    # Verificar fin del juego
    if puntos_jugador >= seleccion or puntos_maquina >= seleccion:
        print("¡Juego finalizado!")
        if puntos_jugador >= seleccion:
            print("¡Ganaste la partida!")
            guardar_puntaje(nombre, 1)
        else:
            print("La máquina ganó la partida.")
        jugando = False

    # Actualizar pantal
    pygame.display.flip()

pygame.quit()