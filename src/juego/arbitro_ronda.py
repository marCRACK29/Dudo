"""
Módulo arbitro_ronda
--------------------

Define la clase `ArbitroRonda`, responsable de administrar
el flujo de una ronda en el juego Dudo.
"""

from typing import Optional, Tuple

from src.juego.enums import OpcionesJuego, OpcionesDudoEspecial, Rotacion
from src.juego.validador_apuesta import ValidadorApuesta
from src.juego.jugador import Jugador

class ArbitroRonda:


    def __init__(self, primer_jugador_id: int, jugadores: list[Jugador],
                 rotacion: Rotacion = Rotacion.HORARIO):
        """Inicializa la ronda con un jugador inicial y una rotación.

               Args:
                   primer_jugador_id (int): Índice del jugador que comienza.
                   jugadores (list[Jugador]): Lista de jugadores en la ronda.
                   rotacion (Rotacion, optional): Dirección de la rotación.
        """
        cantidad_jugadores = len(jugadores)
        if primer_jugador_id < 0:
            raise ValueError("Jugador inicial negativo")
        if primer_jugador_id >= cantidad_jugadores:
            raise ValueError("Jugador inicial superior a cantidad de jugadores")
        if not isinstance(rotacion, Rotacion):
            raise ValueError("Valor dado no es una Rotacion")

        self.cantidad_jugadores = cantidad_jugadores
        self.jugador_actual_id = primer_jugador_id
        self.rotacion = rotacion
        self.jugadores = jugadores
        self.apuesta_anterior = None

    def definir_ganador(self, adivinanza: Tuple[int, int]) -> int:
        """Cuenta la cantidad real de dados que coinciden con una adivinanza.

        Args:
            adivinanza (tuple[int, int]): Cantidad y valor de la apuesta.

        Returns:
            int: Cantidad total encontrada en todos los jugadores.
        """
        cantidad_adivinada = 0
        cantidad_ases = 0
        for jugador in self.jugadores:
            cacho = jugador.cacho
            dados_resultados = cacho.resultados_numericos
            cantidad_adivinada += dados_resultados.count(adivinanza[1])
            cantidad_ases += dados_resultados.count(1)
        if adivinanza[1] != 1:
            cantidad_adivinada = cantidad_adivinada + cantidad_ases

        return cantidad_adivinada

    def procesar_jugada(self, opcion_juego: OpcionesJuego, apuesta_actual: Tuple[int, int], opcion_dudo_especial: Optional[
        OpcionesDudoEspecial] = None):
        """Procesa la jugada del jugador actual según la opción elegida.

        Args:
            opcion_juego (OpcionesJuego): Tipo de jugada (apuesto, dudo, calzo).
            apuesta_actual (tuple[int, int]): Apuesta realizada.
            opcion_dudo_especial (OpcionesDudoEspecial, optional):
                Variante especial de dudo.
        """
        validador_apuesta = ValidadorApuesta()
        total_dados_en_juego = sum(jugador.total_de_dados_en_juego() for jugador in self.jugadores)
        jugador_actual = self.jugadores[self.jugador_actual_id]
        jugador_anterior = self.jugadores[(self.jugador_actual_id - self.rotacion.value) % len(self.jugadores)]

        if opcion_juego == OpcionesJuego.APUESTO:
            self._validar_resolver_apuesta(apuesta_actual, total_dados_en_juego, validador_apuesta)

        elif opcion_juego == OpcionesJuego.DUDO:
            self._resolver_dudo(jugador_actual, jugador_anterior, opcion_dudo_especial)

        elif opcion_juego == OpcionesJuego.CALZO:
            self._resolver_calzo(jugador_actual)

    def es_jugador_con_un_dado(self):
        """Verifica si el jugador actual tiene un único dado.

        Returns:
            bool: True si tiene un dado, False en caso contrario.
        """
        jugador_actual = self.jugadores[self.jugador_actual_id]
        return jugador_actual.total_de_dados_en_juego() == 1

    def reiniciar_ronda(self):
        """Reinicia el estado de la ronda, limpiando la apuesta previa."""
        self.apuesta_anterior = None

    def iniciar_ronda(self):
        """Configura el inicio de ronda en caso de jugadores con un dado."""
        for jugador_id, jugador in enumerate(self.jugadores):
            if jugador.total_de_dados_en_juego() == 1 and not jugador.ya_tuvo_ronda_especial:
                self.jugador_actual_id = jugador_id
                jugador.ya_tuvo_ronda_especial = True # aqui sabemos que tuvo su ronda especial
                return

    def dudo_abierto_resuelve(self):
        """Resuelve la variante de dudo abierto para el jugador actual."""
        jugador_actual = self.jugadores[self.jugador_actual_id]

        #asumimos que el jugador tiene un solo dado y accedemos a esa posicion
        resultado_dado = jugador_actual.cacho.resultados_numericos[0]

        valor_apuesta = self.apuesta_anterior[1]

        if resultado_dado ==valor_apuesta:
            jugador_actual.ganar_dado()
        else:
            jugador_actual.perder_dado()

    def dudo_cerrado_resuelve(self):
        """Resuelve la variante de dudo cerrado para el jugador actual."""
        jugador_actual = self.jugadores[self.jugador_actual_id]

        # Obtenemos la cantidad real de dados usando el método ya probado
        cantidad_real = self.definir_ganador(self.apuesta_anterior)

        cantidad_apuesta = self.apuesta_anterior[0]

        if cantidad_real < cantidad_apuesta:
            jugador_actual.ganar_dado()
        else:
            jugador_actual.perder_dado()

    def _siguiente_jugador(self):
        """Avanza al siguiente jugador en la ronda según la rotación."""
        self.jugador_actual_id = (self.jugador_actual_id + self.rotacion.value) % self.cantidad_jugadores

    def _setear_inicio_ronda(self, jugador: Jugador):
        """Asigna el turno inicial a un jugador específico de la ronda.

        Lanza un ValueError si el jugador no pertenece a la ronda.

        Args:
            jugador (Jugador): El jugador al que se le asignará el turno.
        """
        if jugador not in self.jugadores:
            raise ValueError("El jugador no pertenece a esta ronda")
        self.jugador_actual_id = self.jugadores.index(jugador)

    def _resolver_calzo(self, jugador_actual: Jugador):
        """Resuelve la acción de calzo y aplica sus consecuencias.

        Valida que el calzo sea con al menos la mitad de los dados en juego.
        Si el calzo es correcto, el jugador gana un dado.
        Si es incorrecto, el jugador pierde un dado.

        Args:
            jugador_actual (Jugador): El jugador que realiza la acción de calzo.
        """
        apuesta_anterior = self.apuesta_anterior
        total_dados_en_juego = sum(j.total_de_dados_en_juego() for j in self.jugadores)

        if apuesta_anterior[0] < (total_dados_en_juego / 2):
            raise ValueError("El calzo debe ser con al menos la mitad de los dados en juego")

        cantidad_real = self.definir_ganador(apuesta_anterior)
        calzo_fue_correcto = cantidad_real == apuesta_anterior[0]
        
        if calzo_fue_correcto:
            jugador_actual.ganar_dado()
            self._setear_inicio_ronda(jugador_actual)
        else:
            jugador_actual.perder_dado()
            self._setear_inicio_ronda(jugador_actual)
            
    def _resolver_dudo(self, jugador_actual: Jugador, jugador_anterior: Jugador, opcion_dudo_especial: Optional[
        OpcionesDudoEspecial] = None):
        """Resuelve la acción de dudo aplicando las reglas.

        Maneja la lógica especial si el jugador tiene un solo dado.
        Si el dudo es correcto, el jugador anterior pierde un dado.
        Si el dudo es incorrecto, el jugador actual pierde un dado.

        Args:
            jugador_actual (Jugador): El jugador que realiza la acción de dudo.
            jugador_anterior (Jugador): El jugador que realizó la apuesta previa.
            opcion_dudo_especial (OpcionesDudoEspecial, optional): Tipo de dudo especial.
        """
        if self.es_jugador_con_un_dado() and opcion_dudo_especial:
            if opcion_dudo_especial == OpcionesDudoEspecial.ABIERTO:
                self.dudo_abierto_resuelve()
            elif opcion_dudo_especial == OpcionesDudoEspecial.CERRADO:
                self.dudo_cerrado_resuelve()
        else:
            cantidad_real = self.definir_ganador(self.apuesta_anterior)
            dudo_fue_correcto = cantidad_real < self.apuesta_anterior[0]
            if dudo_fue_correcto:
                jugador_anterior.perder_dado()
                self._setear_inicio_ronda(jugador_anterior)
            else:
                jugador_actual.perder_dado()
                self._setear_inicio_ronda(jugador_actual)

    def _validar_resolver_apuesta(self, apuesta_actual: Tuple[int, int], total_dados_en_juego: int,
                                  validador_apuesta: ValidadorApuesta):
        """Valida una apuesta y avanza el turno si es correcta.

        Args:
            apuesta_actual (tuple[int, int]): La apuesta realizada.
            total_dados_en_juego (int): El total de dados en la ronda.
            validador_apuesta (ValidadorApuesta): Instancia para validar la apuesta.
        """
        es_valido, msg = validador_apuesta.es_apuesta_valida(
            apuesta_actual,
            self.apuesta_anterior,
            total_dados_en_juego
        )
        if es_valido:
            self.apuesta_anterior = apuesta_actual
            self._siguiente_jugador()