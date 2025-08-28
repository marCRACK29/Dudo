from src.juego.jugador import Jugador

class GestorPartida:

    def __init__(self, cantidad_jugadores):
        self.jugadores = [Jugador() for i in range(cantidad_jugadores)]
        self._elegir_primer_jugador(cantidad_jugadores)


    def _elegir_primer_jugador(self, cantidad_jugadores):
        dados_empate = list(range(0, cantidad_jugadores))

        while len(dados_empate) != 1:
            empates_en_ronda = []
            tirada_mayor = -1
            for dado_id in dados_empate:
                tirada = self.jugadores[dado_id].lanzar_un_dado()
                if tirada_mayor == tirada:
                    empates_en_ronda.append(dado_id)
                elif tirada_mayor < tirada:
                    tirada_mayor = tirada
                    empates_en_ronda = [dado_id]
            dados_empate = empates_en_ronda
        self.primer_jugador = dados_empate[0]




