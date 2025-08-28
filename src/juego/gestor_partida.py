from src.juego.jugador import Jugador

class GestorPartida:

    def __init__(self, cantidad_jugadores):
        self.jugadores = [Jugador() for i in range(cantidad_jugadores)]

