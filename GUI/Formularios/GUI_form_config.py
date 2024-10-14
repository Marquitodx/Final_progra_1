import pygame
from pygame.locals import *
from GUI.UI.GUI_button import *
from GUI.UI.GUI_slider import *
from GUI.UI.GUI_textbox import *
from GUI.UI.GUI_label import *
from GUI.UI.GUI_form import *
from GUI.UI.GUI_button_image import *
from GUI.Formularios.GUI_form_menu_score import *
from GUI.Formularios.GUI_form_menu_play import *


class FormConfig(Form):
    def __init__(self, screen, x, y, w, h,
                color_background,
                color_border,
                active,
                path_image,
                path_background = None):
        
        super().__init__(screen, x, y, w, h,
                        color_background,
                        color_border,
                        active)

        aux_image = pygame.image.load(path_image)
        aux_image = pygame.transform.scale(aux_image, (w, h))
        self._slave = aux_image


        self.volumen = 0.2
        self.flag_play = True
        self.path_background = path_background
        if self.path_background != None:
            path_image = self.path_background
            aux_image = pygame.image.load(path_image)
            aux_image = pygame.transform.scale(self.path_background, (w, h))
        
        self.lista_widgets = []

        self.txt_nombre = TextBox(self._slave, x, y, 
                                207, 73, 150, 30,
                                "grey", "white", "red", "blue", 2,
                                "Arial", 15, "black")

        self.btn_play = Button(self._slave, x, y,
                                50, 185, 100, 50,
                                "red", "blue",
                                self.btn_play_click,
                                "hola", "pause", "Verdana", 15, "white")
        
        self.slider_volumen = Slider(self._slave, x, y,
                                    160, 203, 500, 15,
                                    self.volumen,
                                    "red", "white",
                                    r"GUI\Recursos_gui\botton_volume.png")

        porcentaje_volumen = f"{self.volumen * 100}%"

        self.label_volumen = Label(self._slave, 675, 193, 100, 50,
                                    porcentaje_volumen,
                                    "Arial", 15, "black",
                                    r"GUI\Recursos_gui\Table.png")
        

        self.btn_home = Button_Image(screen = self._slave,
                                    master_x= x,
                                    master_y= y,
                                    x = w - 70,
                                    y = h - 70,
                                    w = 50,
                                    h = 50,
                                    path_image= r"GUI\Recursos_gui\home.png",
                                    onclick= self.btn_home_click,
                                    onclick_param= "")


        self.lista_widgets.append(self.txt_nombre)
        self.lista_widgets.append(self.btn_play)
        self.lista_widgets.append(self.slider_volumen)
        self.lista_widgets.append(self.label_volumen)
        self.lista_widgets.append(self.btn_home)

    def btn_home_click(self, param):
        self.end_dialog()

    def update_volumen(self, lista_eventos):
        self.volumen = self.slider_volumen.value
        self.label_volumen.update(lista_eventos)
        self.label_volumen.set_text(f"{round(self.volumen * 100)}%")
        pygame.mixer.music.set_volume(self.volumen)

    def btn_jugar_click(self, param):
        if self.flag_play:
            pygame.mixer.music.pause()
            self.btn_play._color_background = "blue"
            self.btn_play.set_text("Play")
        else:
            pygame.mixer.music.unpause()
            self.btn_play._color_background = "red"
            self.btn_play.set_text("Pause")

        self.flag_play = not self.flag_play

    def update(self, lista_eventos):
            if self.active:
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)
                self.update_volumen(lista_eventos)    
                self.draw()
                self.render()

    def render(self):
        if self.path_background != None:
            self._slave.blit(self.path_background, (0,0))
        else:
            self._slave.fill(self._color_background)