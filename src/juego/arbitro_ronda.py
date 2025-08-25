from enum import Enum

class Rotacion(Enum):
    HORARIO = 1
    ANTIHORARIO = -1

class ArbitroRonda:
    def __init__(self, first_player_id, cantidad_jugadores, rotacion=Rotacion.HORARIO):
        self.cantidad_jugadores = cantidad_jugadores
        self.jugador_actual_id = first_player_id
        self.rotacion = rotacion


    def siguiente_jugador(self):
        self.jugador_actual_id = (self.jugador_actual_id + self.rotacion.value) % self.cantidad_jugadores

