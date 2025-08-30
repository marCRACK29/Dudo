from enum import Enum

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


    def siguiente_jugador(self):
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
    
    def procesar_jugada(self, opcion_juego, validador_apuesta, apuesta_actual):
        total_dados_en_juego = len(self.jugadores) * 5

        if opcion_juego == OpcionesJuego.APUESTO:
            validador_apuesta.es_apuesta_valida(
                apuesta_actual,
                self.apuesta_anterior, 
                total_dados_en_juego
            )
            self.apuesta_anterior = apuesta_actual
            # Este método no necesita retornar nada por ahora
            
        elif opcion_juego == OpcionesJuego.DUDO:
            cantidad_real = self.definir_ganador(self.apuesta_anterior)
            return cantidad_real < self.apuesta_anterior[0] # Retorna True si la apuesta fue mayor
            
        elif opcion_juego == OpcionesJuego.CALZO:
            cantidad_real = self.definir_ganador(self.apuesta_anterior)
            return cantidad_real == self.apuesta_anterior[0] # Retorna True si la apuesta fue exacta
