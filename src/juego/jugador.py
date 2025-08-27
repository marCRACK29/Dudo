from src.juego.cacho import Cacho
from src.juego.dado import Dado

class Jugador:
    def __init__(self):
        self.cacho = Cacho()
        self.dados = [Dado() for _ in range(5)]

    def total_de_dados(self):
        return len(self.dados)
    
    def perder_dado(self):
        self.dados.pop()

    def ganar_dado(self):
        self.dados.append(Dado())

    def realizar_apuesta(self, apuesta_actual):
        self.apuesta_actual = apuesta_actual
        

