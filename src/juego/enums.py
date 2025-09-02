from enum import Enum


class OpcionesJuego(Enum):
    DUDO = 1
    CALZO = 2
    APUESTO = 3


class OpcionesDudoEspecial(Enum):
    ABIERTO = 1
    CERRADO = 2


class Rotacion(Enum):
    HORARIO = 1
    ANTIHORARIO = -1
