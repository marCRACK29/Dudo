class ArbitroRonda:
    def __init__(self, first_player_id, cantidad_jugadores):
        self.cantidad_jugadores = cantidad_jugadores
        self.jugador_actual_id = first_player_id


    def siguiente_jugador(self):
        self.jugador_actual_id = (self.jugador_actual_id + 1) % self.cantidad_jugadores


