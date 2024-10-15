import pygame
import json

from pygame.locals import *
from GUI.UI.GUI_form import *
from GUI.UI.GUI_button_image import *
from GUI.Formularios.GUI_contenedor_nivel import *
from manejador_niveles import Manejador_niveles



class FormMenuPlay(Form):
    def __init__(self, screen, x, y, w, h,
                    color_background, 
                    color_border = "black", 
                    border_size = -1, 
                    active = True, 
                    path_image = r"GUI\Recursos_gui\fondo_menu.png"):
        
        super().__init__(screen, x, y, w, h,
                        color_background, 
                        color_border,
                        border_size, 
                        active)
        
        self.manejador_niveles = Manejador_niveles(self._master)
        aux_image = pygame.image.load(path_image)
        aux_image = pygame.transform.scale(aux_image, (w,h))
        self._slave = aux_image


        self._btn_level_1 = Button_Image(screen = self._slave,
                                        x = 55,
                                        y = 50,
                                        master_x = x,
                                        master_y = y,
                                        w = 150,
                                        h = 150,
                                        onclick = self.entrar_nivel,
                                        onclick_param = "Nivel_uno",
                                        path_image = r"GUI\Recursos_gui\button_lvl_1.png")

        self._btn_level_2 = Button_Image(screen = self._slave,
                                        x = 255,
                                        y = 50,
                                        master_x = x,
                                        master_y = y,
                                        w = 150,
                                        h = 150,
                                        onclick = self.entrar_nivel,
                                        onclick_param = "Nivel_dos",
                                        path_image = r"GUI\Recursos_gui\button_lvl_2.png")

        self._btn_level_3 = Button_Image(screen = self._slave,
                                        x = 55,
                                        y = 250,
                                        master_x = x,
                                        master_y = y,
                                        w = 150,
                                        h = 150,
                                        onclick = self.entrar_nivel,
                                        onclick_param = "Nivel_tres",
                                        path_image = r"GUI\Recursos_gui\button_lvl_3.png")
        
        self._btn_home = Button_Image(screen = self._slave,
                                        x = 430,
                                        y = 430,
                                        master_x = x,
                                        master_y = y,
                                        w = 50,
                                        h = 50,
                                        onclick = self._btn_home_click,
                                        onclick_param = "",
                                        path_image = r"GUI\Recursos_gui\button_home_2.png")
        
        with open("Datos_actuales.json", "r", encoding = "UTF8") as archivo:
            datos = json.load(archivo)
        
        self.lista_widgets.append(self._btn_level_1)
        self.lista_widgets.append(self._btn_level_2)
        self.lista_widgets.append(self._btn_level_3)
        self.lista_widgets.append(self._btn_home)



    def on(self, parametro):
        print("Hola", parametro)


    def update(self, lista_eventos):
        if self.verificar_dialog_result():
            for widget in self.lista_widgets:
                widget.update(lista_eventos)
            self.draw()
        else:
            self.hijo.update(lista_eventos)



    def entrar_nivel(self, nombre_nivel):
        nivel = self.manejador_niveles.get_nivel(nombre_nivel)
        form_contenedor_nivel = FormContenedorNivel(self._master, nivel)
        self.show_dialog(form_contenedor_nivel)



    def _btn_home_click(self, param):
        self.end_dialog()