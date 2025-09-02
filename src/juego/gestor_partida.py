from src.juego.jugador import Jugador
from src.juego.arbitro_ronda import ArbitroRonda, Rotacion, OpcionesJuego
class GestorPartida:

    def __init__(self, cantidad_jugadores: int):
        self.jugadores = [Jugador() for i in range(cantidad_jugadores)]
        self._elegir_primer_jugador(cantidad_jugadores)

    def generar_arbitro(self, rotacion: Rotacion):
        self.arbitro = ArbitroRonda(self.primer_jugador, self.jugadores, rotacion=rotacion)

    def _eliminar_jugadores_sin_dados(self):
        self.jugadores = [j for j in self.jugadores if j.total_de_dados_en_juego() > 0]

    def jugar_ronda(self, proveedor_desiciones):
        while True:
            decision, apuesta = proveedor_desiciones.decidir()
            self.arbitro.procesar_jugada(decision, apuesta)
            self._eliminar_jugadores_sin_dados()
            if decision in (OpcionesJuego.DUDO, OpcionesJuego.CALZO):
                break

    def _elegir_primer_jugador(self, cantidad_jugadores: int):
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