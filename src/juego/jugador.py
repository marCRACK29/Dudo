from src.juego.cacho import Cacho
from src.juego.dado import Dado
import random
from typing import Optional, Tuple
Apuesta = Tuple[int, int]

class Jugador:
    """Representa a un jugador dentro del juego Dudo."""
    def __init__(self):
        """Inicializa un jugador con un cacho y sin dados calzados."""
        self.cacho = Cacho()
        self.dados_calzados = []
        self.apuesta_actual = None
        self.ya_tuvo_ronda_especial = False

    def total_de_dados_en_juego(self):
        """Cuenta los dados disponibles en el cacho.

        Returns:
            int: Número de dados en el cacho.
        """
        return len(self.cacho.dados_actuales)

    def perder_dado(self):
        """Elimina un dado del jugador.

        - Si tiene dados calzados, pierde uno de ellos.
        - En caso contrario, pierde un dado de su cacho.
        """
        if len(self.dados_calzados) > 0:
            self.dados_calzados.pop()
        else:
            self.cacho.pierde_dado()

    def ganar_dado(self):
        """Agrega un dado al jugador.

        - Si el cacho no está lleno, se añade ahí.
        - Si el cacho ya tiene 5 dados, se guarda como calzado.
        """
        dado_ganado = Dado()
        if len(self.cacho.dados_actuales) < 5:
            self.cacho.gana_dado(dado_ganado)
        else:
            self.dados_calzados.append(dado_ganado)

    def realizar_apuesta(self, apuesta_actual: Apuesta):
        """Registra la apuesta realizada por el jugador.

        Args:
            apuesta_actual (Apuesta): Apuesta representada como (cantidad, valor).
        """
        self.apuesta_actual = apuesta_actual

    def elegir_jugador(self, jugadores_disponibles):
        """Elige aleatoriamente a otro jugador.

        Args:
            jugadores_disponibles (list[Jugador]): Lista de jugadores posibles.

        Returns:
            Jugador: El jugador elegido al azar.
        """
        jugador_elegido = random.choice(jugadores_disponibles)

        return jugador_elegido

    def lanzar_un_dado(self):
        """Lanza un dado independiente.

        Returns:
            int: Valor obtenido en la tirada.
        """
        dado = Dado()
        return dado.tirar()


