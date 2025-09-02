from src.juego.cacho import Cacho
from src.juego.dado import Dado
import random
from typing import Optional, Tuple
Apuesta = Tuple[int, int]

class Jugador:
    def __init__(self):
        self.cacho = Cacho()
        self.dados_calzados = []
        self.apuesta_actual = None
        self.ya_tuvo_ronda_especial = False

    def total_de_dados_en_juego(self):
        return len(self.cacho.dados_actuales)
    
    def perder_dado(self):
        if len(self.dados_calzados) > 0:
            self.dados_calzados.pop()          
        else:
            self.cacho.pierde_dado()

    def ganar_dado(self):
        dado_ganado = Dado()
        if len(self.cacho.dados_actuales) < 5:
            self.cacho.gana_dado(dado_ganado)
        else:
            self.dados_calzados.append(dado_ganado)

    def realizar_apuesta(self, apuesta_actual: Apuesta):
        self.apuesta_actual = apuesta_actual
    
    def elegir_jugador(self, jugadores_disponibles):
        jugador_elegido = random.choice(jugadores_disponibles)

        return jugador_elegido

    def lanzar_un_dado(self):
        dado = Dado()
        return dado.tirar()


