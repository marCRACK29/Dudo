class ValidadorApuesta:
    def es_apuesta_valida(self, apuesta) -> bool:
        return 1 <= apuesta[1] <= 6