import pygame, sys
from V_Configuraciones import *
from V_Disparos import *

diccionario_animaciones = {"Quieto": personaje_quieto,
                        "Derecha": personaje_corre,
                        "Izquierda": personaje_camina_izquierda,
                        "Salta": personaje_salta,
                        "QuietoIzq": personaje_quieto_izquierda,
                        "SaltaIzq": personaje_salta_izquierda,
                        "DisparaDer": personaje_dispara,
                        "DisparaIzq": personaje_dispara_izquierda,
                        "CorreDisparaDer": personaje_corre_dispara,
                        "CorreDisparaIzq": personaje_corre_dispara_izquierda}


class Personaje:
    def __init__(self, tamaño, piso, velocidad):
        self.animaciones = diccionario_animaciones
        reescalar_imagenes(self.animaciones, 50, 70)
        self.rectangulo_principal = self.animaciones["Quieto"][0].get_rect()
        self.rectangulo_principal.x = piso.x
        self.rectangulo_principal.y = piso.y - 75
        self.velocidad = velocidad
        self.contador_pasos = 0
        self.que_hace = "Quieto"
        self.animacion_actual = self.animaciones["Quieto"]
        self.direccion = "derecha"
        self.disparo = True
        self.esta_chocando = False
        self.toco_portal = False

        self.rectangulos = obtener_rectangulos(self.rectangulo_principal)
    
    # ------  VITALIDAD  -------
        self.vida = 100
        self.puntaje = 0

    # ------  SALTO  -------
        self.desplazamiento_y = 0 
        self.potencia_salto = -17
        self.limite_velocidad_salto = 17 
        self.esta_saltando = True
        self.gravedad = 1 

    # ------  DISPAROS  -------
        self.esta_disparando = False
        self.lista_disparos = []
        self.avanzar = True

        self.sonido_collec = pygame.mixer.Sound(SONIDO_MONEDA)
        self.sonido_vida   = pygame.mixer.Sound(SONIDO_VIDA)
    

    def caminar(self, pantalla, plataformas):
        velocidad_actual = self.velocidad
        
        if self.que_hace == "Izquierda" or self.que_hace == "CorreDisparaIzq":
            velocidad_actual *= -1

        self.rectangulo_principal.x += velocidad_actual
        self.esta_chocando = False

        for plataforma in plataformas:
            if self.rectangulo_principal.colliderect(plataforma.rectangulo):
                if velocidad_actual > 0:  # Moviendo hacia la derecha
                    self.rectangulo_principal.right = plataforma.rectangulo.left
                    self.esta_chocando = True
                elif velocidad_actual < 0:  # Moviendo hacia la izquierda
                    self.rectangulo_principal.left = plataforma.rectangulo.right
                    self.esta_chocando = True

        # Reposicionar los rectángulos secundarios
        self.rectangulos = obtener_rectangulos(self.rectangulo_principal)


    def animar(self, pantalla):
        largo = len(self.animacion_actual)
        if self.contador_pasos >= largo:
            self.contador_pasos = 0
        pantalla.blit(self.animacion_actual[self.contador_pasos], self.rectangulo_principal)
        self.contador_pasos += 1


    def saltar(self):
        if not self.esta_saltando:
            if self.direccion == "derecha":
                self.esta_saltando = True
                self.desplazamiento_y = self.potencia_salto
                self.animacion_actual = self.animaciones["Salta"]
            elif self.direccion == "izquierda":
                self.esta_saltando = True
                self.desplazamiento_y = self.potencia_salto
                self.animacion_actual = self.animaciones["SaltaIzq"]


    def aplicar_gravedad(self, pantalla, plataformas):
        
        velocidad_salto = self.desplazamiento_y

        if self.esta_saltando:
            self.animar(pantalla)

            for lado in self.rectangulos:
                self.rectangulos[lado].y += self.desplazamiento_y

            if self.desplazamiento_y + self.gravedad < self.limite_velocidad_salto:
                self.desplazamiento_y += self.gravedad

        for piso in plataformas:
            if self.rectangulos["bottom"].colliderect(piso.rectangulo):
                self.desplazamiento_y = 0
                self.esta_saltando = False
                self.rectangulos["main"].bottom = piso.rectangulo.top
                reubicar_rectangulos(self.rectangulo_principal, self.rectangulos)
                break

            elif self.rectangulos["top"].colliderect(piso.rectangulos["bottom"]):
                self.desplazamiento_y *= -1

            else:
                self.esta_saltando = True


    def detectar_colision(self, enemigos, height, plataforma_revive):
        lista_proyectiles = self.lista_disparos
        
        if self.rectangulo_principal.top > height:
            self.reiniciar(plataforma_revive)

        for enemigo in enemigos:
            if self.rectangulos["main"].colliderect(enemigo.rectangulo_principal):
                self.vida -= 1
            
            for proyectil in lista_proyectiles:
                if proyectil.rectangulo.colliderect(enemigo.rectangulo_principal):
                    self.puntaje += 1


    def reiniciar(self, plataforma_revive):

        self.rectangulo_principal.x = plataforma_revive.x
        self.rectangulo_principal.y = plataforma_revive.y - 75
        self.vida -= 10
        self.esta_saltando = False
        self.desplazamiento_y = 0
        self.que_hace = "Quieto"
        self.rectangulos = obtener_rectangulos(self.rectangulo_principal)


    def disparar(self):
        if self.direccion == "derecha":
            x = self.rectangulos["main"].x + 35
            y = self.rectangulos["main"].y + 32
        elif self.direccion == "izquierda":
            x = self.rectangulos["main"].centerx - 25
            y = self.rectangulos["main"].centery
        
        nuevo_disparo = Disparo(x, y, self.direccion, PROYECTIL_JUGADOR)
        nuevo_disparo.sonido_disparo.play()
        self.lista_disparos.append(nuevo_disparo)


    def you_win(self, fuente, color_letras, color_fondo, pantalla, superficie_opaca):
        
        tiempo_inicio = pygame.time.get_ticks()  # obtengo tiempo actual
        
        mensaje = fuente.render("¡GANASTE!", True, color_letras, color_fondo)
        mitad_x = pantalla.get_width() // 2 - mensaje.get_width() // 2
        pantalla.blit(superficie_opaca, (0,0))
        pantalla.blit(mensaje, (mitad_x, 360))


        pygame.display.flip()  # actualizo la pantalla

        # con este bucle creamos una espera de 2 segundos antes de cerrar la ventana
        while pygame.time.get_ticks() - tiempo_inicio < 2000: # (2000 milisegundos = 2 segundos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        pygame.quit()
        sys.exit()


    def game_over(self, fuente, color_letras, color_fondo, pantalla, superficie_opaca):
        '''
        esta funcion recibe una fuente, algunos colores, la pantalla donde
        se va a mostrar el "game over" y la superficie opaca es una surface
        con 50% de opacidad, una cuestion estetica.
        
        esta funcion la utilizo cuando el jugador se equivoca o se queda sin tiempo
        '''
        
        tiempo_inicio = pygame.time.get_ticks()  # obtengo tiempo actual
        
        mensaje = fuente.render("GAME OVER", True, color_letras, color_fondo)
        pantalla.blit(superficie_opaca, (0,0))
        pantalla.blit(mensaje, (275, 243))
            
        pygame.display.flip() 

        while pygame.time.get_ticks() - tiempo_inicio < 2000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        pygame.quit()
        sys.exit()


    def actualizar(self, pantalla, plataformas, enemigos, jugador,
                    fuente, color_letras, color_fondo, 
                    superficie_opaca, tiempo_agotado):
        
        TECLA_DERECHA = pygame.K_RIGHT
        TECLA_IZQUIERDA = pygame.K_LEFT
        TECLA_ESPACIO = pygame.K_SPACE
        TECLA_F = pygame.K_f
        
        keys = pygame.key.get_pressed()

        # --- camina a la derecha
        if keys[TECLA_DERECHA]:
            if keys[pygame.K_f]:
                self.que_hace = "CorreDisparaDer"
                self.disparar()
            else:
                self.que_hace = "Derecha"
            self.direccion = "derecha"

        # --- camina a la izquierda
        elif keys[TECLA_IZQUIERDA]:
            if keys[pygame.K_f]:
                self.que_hace = "CorreDisparaIzq"
                self.disparar()
            else:
                self.que_hace = "Izquierda"
            self.direccion = "izquierda"

        # --- salta
        elif keys[TECLA_ESPACIO]:
            self.saltar()

        # --- dispara quieto
        elif keys[TECLA_F]:
            if self.direccion == "derecha":
                self.que_hace = "DisparaDer"
                self.disparar()
            elif self.direccion == "izquierda":
                self.que_hace = "DisparaIzq"
                self.disparar()


        # --- esta quieto izquierda
        elif self.direccion == "izquierda":
            self.que_hace = "QuietoIzq"

        # --- esta quieto derecha
        elif self.direccion == "derecha":
                self.que_hace = "Quieto"

        
        
        match self.que_hace:

            case "Derecha":
                if not self.esta_saltando:
                    self.animacion_actual = self.animaciones["Derecha"]
                    self.animar(pantalla)
                self.caminar(pantalla, plataformas)

            case "Izquierda":
                if not self.esta_saltando:
                    self.animacion_actual = self.animaciones["Izquierda"]
                    self.animar(pantalla)
                self.caminar(pantalla, plataformas)

            case "Quieto":
                if not self.esta_saltando and not self.esta_chocando:
                    self.animacion_actual = self.animaciones["Quieto"]
                    self.animar(pantalla)
            
            case "QuietoIzq":
                if not self.esta_saltando and not self.esta_chocando:
                    self.animacion_actual = self.animaciones["QuietoIzq"]
                    self.animar(pantalla)
            
            case "DisparaDer":
                self.animacion_actual = self.animaciones["DisparaDer"]
                self.animar(pantalla)
            
            case "DisparaIzq":
                self.animacion_actual = self.animaciones["DisparaIzq"]
                self.animar(pantalla)
            
            case "CorreDisparaDer":
                self.animacion_actual = self.animaciones["CorreDisparaDer"]
                self.animar(pantalla)
                self.caminar(pantalla, plataformas)
            
            case "CorreDisparaIzq":
                self.animacion_actual = self.animaciones["CorreDisparaIzq"]
                self.animar(pantalla)
                self.caminar(pantalla, plataformas)

        if self.toco_portal:
            self.you_win(fuente, color_letras, color_fondo, pantalla, superficie_opaca)

        elif self.vida <= 0 or tiempo_agotado:
                self.game_over(fuente, color_letras, color_fondo, pantalla, superficie_opaca)    

        self.aplicar_gravedad(pantalla, plataformas)

        i = 0
        while i < len(self.lista_disparos):
            self.lista_disparos[i].actualizar(pantalla, enemigos, plataformas, jugador)
            if self.lista_disparos[i].choco:
                del self.lista_disparos[i]
                i -= 1
            i += 1


'''
    def mover_verticalmente(self, plataformas):

        self.rectangulo_principal.y += self.desplazamiento_y

        for plataforma in plataformas:
            if self.rectangulo_principal.colliderect(plataforma.rectangulo):
                if self.desplazamiento_y > 0:  # Colisión por abajo
                    self.rectangulo_principal.bottom = plataforma.rectangulo.top
                    self.desplazamiento_y = 0
                    self.esta_saltando = False
                elif self.desplazamiento_y < 0:  # Colisión por arriba
                    self.rectangulo_principal.top = plataforma.rectangulo.bottom
                    self.desplazamiento_y = 0

        # Actualizar los rectángulos secundarios
        self.rectangulos = obtener_rectangulos(self.rectangulo_principal)

'''