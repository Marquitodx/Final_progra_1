import pygame, sys, sqlite3, json
from GUI.Formularios.GUI_form_principal import FormPrincipal



ANCHO, ALTO = 1280, 720
FPS = 30


pygame.init()
pygame.mixer.init()
RELOJ = pygame.time.Clock()
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))


form_principal = FormPrincipal(PANTALLA,
                                195, 15, 800, 700,
                                "cyan", "yellow",
                                5, True,
                                r"GUI\Recursos_gui\fondo_menu.png")


while True:
    RELOJ.tick(FPS)

    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT or form_principal.quit_game:
            with open("Datos_actuales.json", "r", encoding = "UTF8") as archivo:
                datos = json.load(archivo)
                nombre = datos[0]["nombre_actual"]
                puntuacion_total = datos[0]["puntaje_nivel_1"] + \
                    datos[0]["puntaje_nivel_2"] + datos[0]["puntaje_nivel_3"]
            
            with sqlite3.connect("base_de_datos_puntuacion.db") as conexion:
                try:
                    sentencia = """
                    insert into Usuarios (nombre, puntuacion_total) values (?,?)
                                """
                    conexion.execute(sentencia, (nombre, puntuacion_total))
                except Exception as e:
                    print("Error", e)
            pygame.quit()
            sys.exit()


    form_principal.update(lista_eventos)

    pygame.display.flip()