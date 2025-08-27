class ValidadorApuesta:
    def es_apuesta_valida(self, apuesta) -> bool:
        if not self.es_numero_valido(apuesta):
            return False, "Número inválido"
        return True
    
    def es_numero_valido(self, apuesta) -> bool:
        return 1 <= apuesta[1] <= 6
    
    def es_cantidad_posible(self, apuesta, total_dados) -> bool:
        return 1 <= apuesta[0] <= total_dados