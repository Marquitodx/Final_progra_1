import pygame
import os
import sqlite3

from pygame.locals import *
from GUI.UI.GUI_button import *
from GUI.UI.GUI_slider import *
from GUI.UI.GUI_textbox import *
from GUI.UI.GUI_label import *
from GUI.UI.GUI_form import *
from GUI.UI.GUI_button_image import *

from GUI.Formularios.GUI_form_menu_score import *
from GUI.Formularios.GUI_form_menu_play import *
from GUI.Formularios.GUI_form_config import FormConfig

class FormPrincipal(Form):
    def __init__(self, screen, x, y, w, h,
                color_background,
                color_border = "Grey",
                border_size = -1,
                active = True,
                path_background = None):
        
        super().__init__(screen, x, y, w, h,
                        color_background,
                        color_border,
                        border_size,
                        active)
        
        self.flag_player = True
        self.volumen = 0.2

        self.quit_game = False

        self.posicion_x = x
        self.posicion_y = y
        self.path_background = path_background
        if self.path_background != None:
            path_image = self.path_background
            self.path_background = pygame.image.load(path_image)
            self.path_background = pygame.transform.scale(self.path_background, (w,h))
        

        formato_de_datos_vacio = \
        [
            {
                "nombre_actual": "Sin_nombre",
                "puntaje_nivel_1": 0,
                "puntaje_nivel_2": 0,
                "puntaje_nivel_3": 0,
                "puntaje_nivel_4": 0,
            }
        ]
        with open ("Datos_actuales.json", "w", encoding= "UTF8") as archivo:
            json.dump(formato_de_datos_vacio, archivo, indent = 4, ensure_ascii = False)
        
        if os.path.exists("base_de_datos_puntuacion.db"):
            pass
        else:
            with sqlite3.connect("base_de_datos_puntuacion.db") as conexion:
                try:
                    sentencia = """
                                create table Usuarios
                                ( id integer primary key autoincrement,
                                nombre text,
                                puntuacion_total real )
                                """
                    conexion.execute(sentencia)
                except Exception as e:
                    print("Error:", e)

            var_1 = "Sin_nombre"
            var_2 = 0
            for i in range(3):
                with sqlite3.connect("base_de_datos_puntuacion.db") as conexion:
                    try:
                        nombre = var_1
                        puntaje_total = var_2
                        sentencia = """
                        insert into Usuarios (nombre, puntuacion_total) values (?,?)
                                    """
                        conexion.execute(sentencia, (nombre, puntaje_total))
                    except Exception as e:
                        print("Error:", e)


        self.btn_config = Button_Image(self._slave, x, y,
                                    590, 508, 75, 75,
                                    r"GUI\Recursos_gui\Config_BTN.png",
                                    self.btn_config_click, "")
        
        self.btn_tabla = Button_Image(self._slave, x, y,
                                    250, 300, 300, 100,
                                    r"GUI\Recursos_gui\buttom_stadistics.png",
                                    self.btn_tabla_click, "")
        
        self.btn_play = Button_Image(self._slave, x, y,
                                    250, 200, 300, 100,
                                    r"GUI\Recursos_gui\button_play.png",
                                    self.btn_jugar_click, "")
        
        self.btn_quit = Button_Image(self._slave, x, y,
                                    250, 400, 300, 100,
                                    r"GUI\Recursos_gui\button_quit.png",
                                    self.btn_quit, "")
        
        self.lista_widgets.append(self.btn_config)
        self.lista_widgets.append(self.btn_tabla)
        self.lista_widgets.append(self.btn_play)
        self.lista_widgets.append(self.btn_quit)


    def render(self):
        if self.path_background != None:
            self._slave.blit(self.path_background, (0,0))
        else:
            self._slave.fill(self._color_background)

    def update(self, lista_eventos):
        if self.verificar_dialog_result():
            if self.active:
                self.draw()
                self.render()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)    
        else:
            self.hijo.update(lista_eventos)
    

    def btn_jugar_click(self, param):
        form_jugar = FormMenuPlay(screen = self._master,
                                x = self._master.get_width() / 2 - 250,
                                y = self._master.get_height() / 2 - 250,
                                w = 500,
                                h = 500,
                                color_background = (220, 0, 220),
                                color_border = (255, 255, 255),
                                active = True, 
                                path_image = r"GUI\Recursos_gui\fondo_naranja.png")
        self.show_dialog(form_jugar)
    
    
    def btn_tabla_click(self, param):
        with open("Datos_actuales.json", "r", encoding = "UTF8") as archivo:
            datos = json.load(archivo)
        nombre = datos[0]["nombre_actual"]
        puntuacion_total = datos[0]["puntaje_nivel_1"] + datos[0]["puntaje_nivel_2"] + \
        datos[0]["puntaje_nivel_3"]

        with sqlite3.connect("base_de_datos_puntuacion.db") as conexion:
            try:
                sentencia = """
                insert into Usuarios (nombre, puntuacion_total) values (?,?)
                            """
                conexion.execute(sentencia, (nombre, puntuacion_total))
            except Exception as e:
                print("Error:", e)
        
        lista_top_tres = []
        with sqlite3.connect("base_de_datos_puntuacion.db") as conexion:
            try:
                sentencia = "select nombre, puntuacion_total from Usuarios order by puntuacion_total desc limit 3"
                cursor = conexion.execute(sentencia)
                for fila in cursor:
                    lista_top_tres.append(fila)
            except Exception as e:
                print("Error:", e)


        diccionario = [
            {"Jugador":lista_top_tres[0][0], "Score": lista_top_tres[0][1]},
            {"Jugador":lista_top_tres[1][0], "Score": lista_top_tres[1][1]},
            {"Jugador":lista_top_tres[2][0], "Score": lista_top_tres[2][1]},]

        nuevo_form = FormMenuScore(screen = self._master,
                                    x = 300,
                                    y = 75,
                                    w = 800,
                                    h = 700,
                                    color_background = "green",
                                    color_border = "grey",
                                    active = True, 
                                    path_image = r"GUI\Recursos_gui\Window.png",
                                    scoreboard = diccionario,
                                    margen_x = 10,
                                    margen_y = 100,
                                    espacio = 10)
        
        self.show_dialog(nuevo_form)
    

    def btn_config_click(self, param):
        nuevo_form =  FormConfig(screen = self._master,
                                x = 300,
                                y = 75,
                                w = 800,
                                h = 700,
                                color_background = "green",
                                color_border = "grey",
                                active = True,
                                path_image = r"GUI\Recursos_gui\fondo_azul.png",
                                path_background = r"GUI\Recursos_gui\fondo_azul.png")
        self.show_dialog(nuevo_form)
    
    def btn_quit(self, param):
        self.quit_game = True