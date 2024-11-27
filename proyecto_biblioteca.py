import pygame
import sys 
import random

#tamaño de pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
GRIS = (169, 169, 169)
AZUL = (57, 93, 150)
COLOR_BOTONES = (165, 198, 250)
ACERTADO = (0, 255, 0)  
FALLADO = (255, 0, 0)  

FILAS = 10
COLUMNAS = 10
TAMANIO_CASILLA = 500// FILAS

#carga de imagenes
imagen_oceano = pygame.image.load("_ejerpygame_py\imagenes\oceano.jpg")
imagen_menu = pygame.image.load("_ejerpygame_py\imagenes\imagen_menu.jpg")
imagen_icono = pygame.image.load("_ejerpygame_py\imagenes\imagen_icono.jpg")
imagen_acierto = pygame.image.load("_ejerpygame_py\imagenes\explosion.png")

imagen_acierto = pygame.transform.scale(imagen_acierto, (TAMANIO_CASILLA, TAMANIO_CASILLA))
imagen_menu_agrandada = pygame.transform.scale(imagen_menu, (800, 600))
imagen_oceano_agrandada = pygame.transform.scale(imagen_oceano, (800, 600))


def inicializar_matriz(filas:int, columnas:int)->list:
    """
    Inicializa una matriz
    Recibe por parametro un numero de filas y otro de columnas
    Devuelve una matriz
    """
    matriz = []
    for _ in range(filas):
        fila = [0] * columnas
        matriz += [fila]
    return matriz

def chequear_casillas_disponibles(matriz, x, y, longitud_barco, orientacion):
    '''
    verifica si se puede colocar un barco en x - y, y que si no pase los limites del tablero 
    ni que haya otro barcoen las casillas

    '''
    retorno = True
    if orientacion == 'horizontal':
        if y + longitud_barco > 10:  # Verificar que el barco no se pase de los límites
            retorno = False
        for i in range(longitud_barco):   # Verificar que no haya otros barcos en el camino
            if y + i >= 10 or matriz[x][y + i] != 0:
                retorno = False
                break
    elif orientacion == 'vertical':
        if x + longitud_barco > 10:  
            retorno = False
        for i in range(longitud_barco):
            if x + i >= 10 or matriz[x + i][y] != 0:
                retorno = False
                break
    
    return retorno

def colocar_barco(matriz, longitud_barco, dificultad):
    """
    coloca un barco de longitud específica en el tablero en una posicion y orientacion aleatoria
    si no hay otro barco
    """
    orientaciones = ['horizontal', 'vertical']
    while True:
        if dificultad == "facil":
            x = random.randint(0, 9) 
            y = random.randint(0, 9) 
        elif dificultad == "normal":
            x = random.randint(0, 19) 
            y = random.randint(0, 19) 
        elif dificultad == "dificil":
            x = random.randint(0, 39) 
            y = random.randint(0, 39) 
        orientacion = random.choice(orientaciones)  
        if chequear_casillas_disponibles(matriz, x, y, longitud_barco, orientacion):
            
            if orientacion == 'horizontal':   # Si puede colocar el barco, lo coloca
                for i in range(longitud_barco):
                    matriz[x][y + i] = 1
            elif orientacion == 'vertical':
                for i in range(longitud_barco):
                    matriz[x + i][y] = 1
            break


def colocar_todos_los_barcos(tablero : list, dificultad :str) ->None:
    '''
    coloca todos los barcos en el tablero
    
    '''
    if dificultad == "facil":
        barcos = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4 ]
    elif dificultad == "normal":
        barcos = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4 ] * 2
    elif dificultad == "dificil":
        barcos = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4 ] * 3

    for longitud_barco in barcos:
        colocar_barco(tablero, longitud_barco, dificultad)


def dibujar_grilla(pantalla:pygame.Surface, tablero:list, FILAS:int, COLUMNAS:int)->None:
    '''
    Dibuja la grilla del juego en la pantalla
    '''
    TAMANIO_CASILLA = 500// FILAS
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            x = columna * TAMANIO_CASILLA
            y = fila * TAMANIO_CASILLA
            
            if tablero[fila][columna] == 2:  # Acertado
                pantalla.blit(imagen_acierto, (x, y))  

            elif tablero[fila][columna] == -1:  # Fallado
                pygame.draw.rect(pantalla, FALLADO, (x, y, TAMANIO_CASILLA, TAMANIO_CASILLA))  

            else:
                pygame.draw.rect(pantalla, GRIS, (x, y, TAMANIO_CASILLA, TAMANIO_CASILLA))  
            
            pygame.draw.rect(pantalla, NEGRO, (x, y, TAMANIO_CASILLA, TAMANIO_CASILLA), 1)

def pantalla_juego(pantalla:pygame.Surface, puntaje:int, tablero:list, FILAS:int, COLUMNAS:int):
    '''
    Muestra la pantalla del juego (la matriz y el puntaje)
    '''
    pantalla.fill(BLANCO)
    pantalla.blit(imagen_oceano_agrandada, (0, 0))
    dibujar_grilla(pantalla, tablero, FILAS, COLUMNAS)

    fuente = pygame.font.Font(None, 36)
    texto_puntaje = fuente.render(f"Puntaje: {puntaje:04d}", True, NEGRO)
    pantalla.blit(texto_puntaje, (600, 50))
    
    puntaje_rect = pygame.Rect(580, 40, 185, 50)  
    pygame.draw.rect(pantalla, (255, 255, 0), puntaje_rect)

    salir_rect = pygame.Rect(600, 550, 100, 40)
    mouse_pos = pygame.mouse.get_pos()
    texto_salir = fuente.render("Salir", True, NEGRO)
    
    reiniciar_rect = pygame.Rect(600, 500, 120, 40)
    texto_reiniciar = fuente.render("Reiniciar", True, NEGRO)

    dibujar_rectangulo_interactivo(pantalla, salir_rect, mouse_pos, AZUL, COLOR_BOTONES)
    dibujar_rectangulo_interactivo(pantalla, reiniciar_rect, mouse_pos, AZUL, COLOR_BOTONES)
    
    pantalla.blit(texto_puntaje, (600, 50))
    pantalla.blit(texto_salir, (salir_rect.x + 20, salir_rect.y + 10))
    pantalla.blit(texto_reiniciar, (reiniciar_rect.x + 5, reiniciar_rect.y + 10))


    pygame.display.flip()
    return salir_rect, reiniciar_rect




def dibujar_rectangulo_interactivo(pantalla:pygame.Surface, rectangulo:pygame.Rect, mouse_pos:int, color_interactivo:int, color_normal:int, radio_borde=5)->None:
    '''
    Hace que los botones sean interactivos: cuando se le pasa el cursor por encima se cambia de color
    '''
    if rectangulo.collidepoint(mouse_pos):
        color = color_interactivo 
        pygame.draw.rect(pantalla, color, rectangulo, border_radius=radio_borde)
    else:
        color = color_normal
        pygame.draw.rect(pantalla, color, rectangulo, border_radius=radio_borde)


def menu_principal(pantalla :pygame.surface):
    '''
    muestra el menu principal del juego donde el usuario puede elegir entre iniciar el juego,
    seleccionar dificultad, ver puntajes o salir.
    '''

    seleccion = None
    
    font = pygame.font.Font(None, 50)
    texto_dificultad = font.render("Dificultad", True, NEGRO)
    texto_jugar = font.render("Jugar", True, NEGRO)
    texto_puntajes = font.render("Ver Puntajes", True, NEGRO)
    texto_salir = font.render("Salir", True, NEGRO)

    dificultad_rect = pygame.Rect(270, 80, 250, 50)
    jugar_rect = pygame.Rect(270, 140, 250, 50)
    puntajes_rect = pygame.Rect(270, 200, 250, 50)
    salir_rect = pygame.Rect(270, 260, 250, 50)

    while True:
        pantalla.fill(BLANCO)
        pantalla.blit(imagen_menu_agrandada, (0, 0))
        
        mouse_pos = pygame.mouse.get_pos()
        
        dibujar_rectangulo_interactivo(pantalla, dificultad_rect, mouse_pos, AZUL, COLOR_BOTONES)
        dibujar_rectangulo_interactivo(pantalla, jugar_rect, mouse_pos, AZUL, COLOR_BOTONES)
        dibujar_rectangulo_interactivo(pantalla, puntajes_rect, mouse_pos, AZUL, COLOR_BOTONES)
        dibujar_rectangulo_interactivo(pantalla, salir_rect, mouse_pos, AZUL, COLOR_BOTONES)
        
        pantalla.blit(texto_dificultad, (dificultad_rect.x + 40, dificultad_rect.y + 10))
        pantalla.blit(texto_jugar, (jugar_rect.x + 70, jugar_rect.y + 10))
        pantalla.blit(texto_puntajes, (puntajes_rect.x + 20, puntajes_rect.y + 10))
        pantalla.blit(texto_salir, (salir_rect.x + 80, salir_rect.y + 10))

        pygame.display.flip()

    
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                sonido_botones = pygame.mixer.Sound("_ejerpygame_py\sonidos\sonido_boton.wav")
                sonido_botones.play()
                
                if jugar_rect.collidepoint(evento.pos):
                    seleccion = "jugar"
                elif puntajes_rect.collidepoint(evento.pos):
                    seleccion = "puntajes"
                elif dificultad_rect.collidepoint(evento.pos):
                    seleccion = "Dificultad"
                elif salir_rect.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()
        return seleccion
        

def detectar_clic(tablero:list, fila:int, columna:int, puntaje:int)->int:
    '''
    detecta si es agua o barco y actualiza el tablero y el puntaje.
    '''
    if tablero[fila][columna] == 1:  # Barco
        tablero[fila][columna] = 2  # Marcado como acertado
        puntaje += 5
    elif tablero[fila][columna] == 0:  # Agua
        tablero[fila][columna] = -1  # Marcado como fallado
        puntaje -= 1
    return puntaje


def mostrar_pantalla_dificultad(pantalla :pygame.surface):
    '''
    crea y muesta la pantalla de dificultad
    '''
    dificultad_seleccionada = None
    corriendo_dificultad = True

    rectangulo_facil = pygame.Rect(270, 100, 200, 50)
    rectangulo_normal = pygame.Rect(270, 160, 200, 50)
    rectangulo_dificil = pygame.Rect(270, 220, 200, 50)

    fuente = pygame.font.Font(None, 50)
    texto_dificultad = fuente.render("Dificultad", True, NEGRO)
    texto_facil = fuente.render("Fácil", True, NEGRO)
    texto_normal = fuente.render("Normal", True, NEGRO)
    texto_dificil = fuente.render("Difícil", True, NEGRO)

    while corriendo_dificultad == True:
        
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                coordenadas_click = pygame.mouse.get_pos()
                sonido_botones = pygame.mixer.Sound("_ejerpygame_py\sonidos\sonido_boton.wav")
                if rectangulo_facil.collidepoint(coordenadas_click):
                
                    sonido_botones.play()
                    dificultad_seleccionada = "facil"
                    print(f"dificultad selecionada: {dificultad_seleccionada}")
                    corriendo_dificultad = False

                elif rectangulo_normal.collidepoint(coordenadas_click):
                    sonido_botones.play()
                    dificultad_seleccionada = "normal"
                    print(f"dificultad selecionada: {dificultad_seleccionada}")
                    corriendo_dificultad = False

                elif rectangulo_dificil.collidepoint(coordenadas_click):
                    sonido_botones.play()
                    dificultad_seleccionada = "dificil"
                    print(f"dificultad selecionada: {dificultad_seleccionada}")
                    corriendo_dificultad = False
        

        pantalla.fill(NEGRO)
        pantalla.blit(imagen_menu_agrandada, (0, 0))

        pygame.draw.rect(pantalla, COLOR_BOTONES, rectangulo_facil, 0 ,5)
        pygame.draw.rect(pantalla, COLOR_BOTONES, rectangulo_normal, 0 ,5)
        pygame.draw.rect(pantalla, COLOR_BOTONES, rectangulo_dificil, 0 ,5)


        dibujar_rectangulo_interactivo(pantalla, rectangulo_facil, mouse_pos, AZUL, COLOR_BOTONES)
        dibujar_rectangulo_interactivo(pantalla, rectangulo_normal, mouse_pos, AZUL, COLOR_BOTONES)
        dibujar_rectangulo_interactivo(pantalla, rectangulo_dificil, mouse_pos, AZUL, COLOR_BOTONES)
    
        pantalla.blit(texto_facil, (rectangulo_facil.x + 30, rectangulo_facil.y + 10))
        pantalla.blit(texto_normal, (rectangulo_normal.x + 30, rectangulo_normal.y + 10))
        pantalla.blit(texto_dificil, (rectangulo_dificil.x + 30, rectangulo_dificil.y + 10))


        pygame.display.update()
    return dificultad_seleccionada


def mostrar_pantalla_puntajes(pantalla :pygame.surface):
    '''
    crea y muestra la pantalla puntajes con los valores ordenados de mayor a menor.
    '''
    corriendo_puntaje = True
    rectangulo_salir = pygame.Rect(600, 550, 100, 40)
    rectangulo_texto = pygame.Rect(250, 150, 200, 200)
    fuente = pygame.font.Font(None, 36)
    texto_salir = fuente.render("Salir", True, NEGRO)
    ##############################################################
    lista_puntajes = leer_archivos_txt("_ejerpygame_py/puntaje.txt")
    diccionarios = []
    for linea in lista_puntajes:

        nombre, puntos = linea.split(" : ")
        diccionarios.append({"nombre": nombre, "puntaje": int(puntos)})  

        # metodo de burbujeo para ordenar los puntajes
    largo_lista_dicc = len(diccionarios)
    for i in range(largo_lista_dicc):
        for j in range(0, largo_lista_dicc - i - 1):
            if diccionarios[j]["puntaje"] < diccionarios[j+1]["puntaje"]:
                diccionarios[j], diccionarios[j+1] = diccionarios[j+1], diccionarios[j]

    while corriendo_puntaje == True:
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                coordenadas_click = pygame.mouse.get_pos()
                sonido_botones = pygame.mixer.Sound("_ejerpygame_py/sonidos/sonido_boton.wav")

                if rectangulo_salir.collidepoint(coordenadas_click):
                    sonido_botones.play()
                    corriendo_puntaje = False
        pantalla.fill(NEGRO)
        pantalla.blit(imagen_menu_agrandada, (0, 0))
        
        dibujar_rectangulo_interactivo(pantalla, rectangulo_salir, mouse_pos, BLANCO, COLOR_BOTONES)
        dibujar_rectangulo_interactivo(pantalla, rectangulo_texto,mouse_pos, GRIS, BLANCO )
        pantalla.blit(texto_salir, (rectangulo_salir.x + 20, rectangulo_salir.y + 10))
        

        y = rectangulo_texto.y + 10  
        for diccionario in diccionarios:
            texto_puntaje = fuente.render(f"{diccionario['nombre']}: {diccionario['puntaje']}", True, (NEGRO))  # Texto del puntaje
            pantalla.blit(texto_puntaje, (rectangulo_texto.x + 10, y))
            y += 40  
        
        pygame.display.update()
    return rectangulo_salir


def guardar_puntaje(nombre:str, puntaje:int)->None:
    """Guarda el puntaje del jugador en un archivo de texto.
    """
    with open("_ejerpygame_py/puntaje.txt", "a") as archivo:
        archivo.write(f"{nombre} : {puntaje}\n")


def pedir_nombre(pantalla, puntaje):
    '''
    crea una pantalla basica(en blanco) para que el usuario ponga su nombre al ahcer click en "salir"
    '''
    fuente = pygame.font.Font(None, 36)
    
    texto = fuente.render("Introduce tu Nombre:", True, NEGRO)
    pantalla.fill(BLANCO)
    pantalla.blit(texto, (250, 200)) 

    caja_texto = pygame.Rect(250, 250, 300, 40)
    pygame.draw.rect(pantalla, NEGRO, caja_texto, 2) 

    nombre = ''
    activo = True
    while activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  
                    activo = False
                elif evento.key == pygame.K_BACKSPACE:  
                    nombre = nombre[:-1]
                else:
                    nombre += evento.unicode 

        
        texto_nombre = fuente.render(nombre, True, NEGRO)
        pantalla.blit(texto_nombre, (caja_texto.x + 5, caja_texto.y + 5))

        pygame.display.flip()

    guardar_puntaje(nombre, puntaje)



def leer_archivos_txt(ruta:str)-> list:
    '''
    lee linea por linea y devuelve una lista de lineas.
    '''
    with open(ruta, "r") as mi_archivo:
        dato = mi_archivo.readlines()
    return dato

