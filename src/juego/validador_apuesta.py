class ValidadorApuesta:
    def es_apuesta_valida(self, apuesta) -> bool:
        if not self.es_numero_valido(apuesta):
            return False, "Número inválido"
        return True
    
    def es_numero_valido(self, apuesta) -> bool:
        return 1 <= apuesta[1] <= 6