def caminar(self, pantalla, plataformas):
        velocidad_actual = self.velocidad
        if self.que_hace == "Izquierda" or self.que_hace == "CorreDisparaIzq":
            velocidad_actual *= -1


        self.rectangulo_principal.x += velocidad_actual
        self.esta_chocando = False
        

        for plataforma in plataformas:
            if self.rectangulo_principal.colliderect(plataforma.rectangulo_principal):
                #print("chocando")
                if velocidad_actual > 0:  # Moviendo hacia la derecha
                    self.rectangulo_principal.right = plataforma.rectangulo.left
                    self.esta_chocando = True
                elif velocidad_actual < 0:  # Moviendo hacia la izquierda
                    self.rectangulo_principal.left = plataforma.rectangulo.right
                    self.esta_chocando = True
        
        # Reposicionar los rectángulos secundarios
        self.rectangulos = obtener_rectangulos(self.rectangulo_principal)

# ----------------------------------------------------------------

def caminar(self, pantalla, plataformas):
        velocidad_actual = self.velocidad
        if self.que_hace == "Izquierda" or self.que_hace == "CorreDisparaIzq":
            velocidad_actual *= -1


        self.rectangulo_principal.x += velocidad_actual
        self.esta_chocando = False
        

        for plataforma in plataformas:
            if self.rectangulos["right"].colliderect(plataforma.rectangulos["left"]):
                print("chocando")
                # if velocidad_actual > 0:  # Moviendo hacia la derecha
                #     self.rectangulo_principal.right = plataforma.rectangulo.left
                #     self.esta_chocando = True
                # elif velocidad_actual < 0:  # Moviendo hacia la izquierda
                #     self.rectangulo_principal.left = plataforma.rectangulo.right
                #     self.esta_chocando = True
        
        # Reposicionar los rectángulos secundarios
        self.rectangulos = obtener_rectangulos(self.rectangulo_principal)
# ----------------------------------------------------------------

def caminar(self, pantalla, plataformas):
        velocidad_actual = self.velocidad
        if self.que_hace == "Izquierda" or self.que_hace == "CorreDisparaIzq":
            velocidad_actual *= -1

        # Intenta mover primero el rectángulo principal
        self.rectangulo_principal.x += velocidad_actual
        self.esta_chocando = False
        

        for plataforma in plataformas:
            if self.rectangulos["right"].colliderect(plataforma.rectangulos["left"]):
                print("chocando")
                # if velocidad_actual > 0:  # Moviendo hacia la derecha
                #     self.rectangulo_principal.right = plataforma.rectangulo.left
                #     self.esta_chocando = True
                # elif velocidad_actual < 0:  # Moviendo hacia la izquierda
                #     self.rectangulo_principal.left = plataforma.rectangulo.right
                #     self.esta_chocando = True
        
        # Reposicionar los rectángulos secundarios
        self.rectangulos = obtener_rectangulos(self.rectangulo_principal)

# ----------------------------------------------------------------

