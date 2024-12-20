
import pygame
import sys
from proyecto_biblioteca import *


pygame.init()

pygame.display.set_caption("Batalla Naval")


pygame.display.set_icon(imagen_icono)


pygame.mixer.music.load("_ejerpygame_py\sonidos\sonido_menuu.wav")
pygame.mixer.music.set_volume(0.2)  # 0 - 1 -> 0.2 es el 20% del volumen
pygame.mixer.music.play(-1, 0.0)
sonido_clic_juego = pygame.mixer.Sound("_ejerpygame_py\sonidos\sonido_cañones.wav")
pygame.mixer.Sound.set_volume((sonido_clic_juego), 0.2)



puntaje = 0000
dificultad = "facil"
sonido = True

while True:
    mouse_pos = pygame.mouse.get_pos()
    
    seleccion = menu_principal(pantalla)

    
    if seleccion == "Dificultad":
        dificultad = mostrar_pantalla_dificultad(pantalla)
        if dificultad == "facil":
            FILAS = 10
            COLUMNAS = 10
            TAMANIO_CASILLA = 500// FILAS
        elif dificultad == "normal":
            FILAS = 20
            COLUMNAS = 20
            TAMANIO_CASILLA = 500// FILAS
        elif dificultad == "dificil":
            FILAS = 40
            COLUMNAS = 40
            TAMANIO_CASILLA = 500// FILAS
        
    if seleccion == "puntajes":
        puntajes_personas = mostrar_pantalla_puntajes(pantalla)

    if seleccion == "jugar" :

        pygame.mixer.music.stop()  
        pygame.mixer.music.load("_ejerpygame_py\sonidos\sonido_oceano.mp3")
        pygame.mixer.music.set_volume(1)  
        pygame.mixer.music.play(-1, 0.0) 

        tablero = inicializar_matriz(FILAS, COLUMNAS)
        barcos_ocupados = colocar_todos_los_barcos(tablero, dificultad)
        puntaje = 0000
        juego_en_curso = True



        while juego_en_curso:
            mouse_pos = pygame.mouse.get_pos()
            salir_rect, reiniciar_rect = pantalla_juego(pantalla, puntaje, tablero, FILAS, COLUMNAS)
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = mouse_pos
                    columna = mouse_x // TAMANIO_CASILLA
                    fila = mouse_y // TAMANIO_CASILLA



                    if 0 <= fila < FILAS and 0 <= columna < COLUMNAS:
                        puntaje = detectar_clic(tablero, fila, columna, puntaje, barcos_ocupados)
                        #sonido del cañon 
                        sonido_clic_juego.play()  
                        pygame.time.wait(150)
                        sonido_clic_juego.stop()

                    if salir_rect.collidepoint(mouse_pos):
                        juego_en_curso = False
                        pedir_nombre(pantalla, puntaje)
                        break
                    if reiniciar_rect.collidepoint(mouse_pos):
                        tablero = inicializar_matriz(FILAS, COLUMNAS)
                        colocar_todos_los_barcos(tablero, dificultad)
                        puntaje = 0000
                        break

