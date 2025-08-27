from src.juego.cacho import Cacho
from src.juego.dado import Dado

class Jugador:
    def __init__(self):
        self.cacho = Cacho()
        self.dados = [Dado() for _ in range(5)]
        self.cantidad_dados = len(self.dados)

    def total_de_dados(self):
        return self.cantidad_dados