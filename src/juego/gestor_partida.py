from src.juego.jugador import Jugador
from src.juego.arbitro_ronda import ArbitroRonda
from src.juego.enums import OpcionesJuego, Rotacion


class GestorPartida:
    """Orquesta el desarrollo de una partida completa de Dudo."""

    def __init__(self, cantidad_jugadores: int):
        """Inicializa la partida con la cantidad de jugadores indicada.

        Args:
            cantidad_jugadores (int): Número total de jugadores.
        """
        self.jugadores = [Jugador() for i in range(cantidad_jugadores)]
        self._elegir_primer_jugador(cantidad_jugadores)

    def generar_arbitro(self, rotacion: Rotacion):
        """Crea un árbitro de ronda asociado a la partida.

        Args:
            rotacion (Rotacion): Dirección de la rotación de turnos.
        """
        self.arbitro = ArbitroRonda(self.primer_jugador, self.jugadores, rotacion=rotacion)

    def jugar_ronda(self, proveedor_desiciones) -> bool:
        """Ejecuta una ronda del juego.

        Args:
            proveedor_desiciones: Objeto que define la lógica de toma de decisiones.

        Returns:
            bool: True si queda un solo jugador (fin de partida),
            False en caso contrario.
        """
        while True:

            decision, apuesta = proveedor_desiciones.decidir()
            self.arbitro.procesar_jugada(decision, apuesta)
            self._eliminar_jugadores_sin_dados()
            if decision in (OpcionesJuego.DUDO, OpcionesJuego.CALZO):
                break
        self.arbitro.reiniciar_ronda()
        return len(self.jugadores) == 1

    def _eliminar_jugadores_sin_dados(self):
        """Elimina de la partida a los jugadores que se quedaron sin dados."""
        self.jugadores = [j for j in self.jugadores if j.total_de_dados_en_juego() > 0]

    def _elegir_primer_jugador(self, cantidad_jugadores: int):
        """Determina al primer jugador mediante una tirada de dados.

        Args:
            cantidad_jugadores (int): Número de jugadores en la partida.
        """
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