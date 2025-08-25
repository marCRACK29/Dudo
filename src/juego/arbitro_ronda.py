from enum import Enum

class Rotacion(Enum):
    HORARIO = 1
    ANTIHORARIO = -1

class ArbitroRonda:
    def __init__(self, primer_jugador_id, cantidad_jugadores, rotacion=Rotacion.HORARIO):
        if primer_jugador_id < 0:
            raise ValueError("Jugador inicial negativo")
        if primer_jugador_id >= cantidad_jugadores:
            raise ValueError("Jugador inicial superior a cantidad de jugadores")

        self.cantidad_jugadores = cantidad_jugadores
        self.jugador_actual_id = primer_jugador_id
        self.rotacion = rotacion


    def siguiente_jugador(self):
        self.jugador_actual_id = (self.jugador_actual_id + self.rotacion.value) % self.cantidad_jugadores

