from enum import Enum

from src.juego.validador_apuesta import ValidadorApuesta

class OpcionesJuego(Enum):
    DUDO = 1
    CALZO = 2
    APUESTO = 3

class Rotacion(Enum):
    HORARIO = 1
    ANTIHORARIO = -1

class ArbitroRonda:
    def __init__(self, primer_jugador_id, jugadores, rotacion=Rotacion.HORARIO):
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

    def _siguiente_jugador(self):
        self.jugador_actual_id = (self.jugador_actual_id + self.rotacion.value) % self.cantidad_jugadores

    def definir_ganador(self, adivinanza):
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

    def _setear_inicio_ronda(self, jugador):
        if jugador not in self.jugadores:
            raise ValueError("El jugador no pertenece a esta ronda")
        self.jugador_actual_id = self.jugadores.index(jugador)

    def procesar_jugada(self, opcion_juego, apuesta_actual):
        validador_apuesta = ValidadorApuesta()
        total_dados_en_juego = sum(jugador.total_de_dados_en_juego() for jugador in self.jugadores)
        jugador_actual = self.jugadores[self.jugador_actual_id]
        jugador_anterior = self.jugadores[(self.jugador_actual_id - self.rotacion.value) % len(self.jugadores)]

        if opcion_juego == OpcionesJuego.APUESTO:
            es_valido, msg = validador_apuesta.es_apuesta_valida(
                apuesta_actual,
                self.apuesta_anterior,
                total_dados_en_juego
            )
            if not es_valido:
                return
            self.apuesta_anterior = apuesta_actual
            self._siguiente_jugador()

        elif opcion_juego == OpcionesJuego.DUDO:
            cantidad_real = self.definir_ganador(self.apuesta_anterior)
            dudo_fue_correcto = cantidad_real < self.apuesta_anterior[0]

            if dudo_fue_correcto:
                jugador_anterior.perder_dado()
                self._setear_inicio_ronda(jugador_anterior)
            else:
                jugador_actual.perder_dado()
                self._setear_inicio_ronda(jugador_actual)

        elif opcion_juego == OpcionesJuego.CALZO:
            cantidad_real = self.definir_ganador(self.apuesta_anterior)
            calzo_fue_correcto = cantidad_real == self.apuesta_anterior[0]

            if calzo_fue_correcto:
                jugador_actual.ganar_dado()
                self._setear_inicio_ronda(jugador_actual)
            else:
                jugador_actual.perder_dado()
                self._setear_inicio_ronda(jugador_actual)

    def es_jugador_con_un_dado(self):
        jugador_actual = self.jugadores[self.jugador_actual_id]
        return jugador_actual.total_de_dados_en_juego() == 1