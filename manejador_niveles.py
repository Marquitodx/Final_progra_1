from pygame.locals import *
from Nivel1 import Nivel_1
from Nivel2 import Nivel_2
from Nivel3 import Nivel_3


class Manejador_niveles:
    def __init__(self, pantalla) -> None:
        self.__slave = pantalla
        self.niveles = {"Nivel_uno": Nivel_1,
                        "Nivel_dos": Nivel_2,
                        "Nivel_tres": Nivel_3}

    def get_nivel(self, nombre_nivel):
        return self.niveles[nombre_nivel](self.__slave)