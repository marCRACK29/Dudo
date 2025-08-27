class ValidadorApuesta:
    def es_apuesta_valida(self, apuesta, total_dados) -> bool:
        if not self.es_numero_valido(apuesta):
            return False, "Número inválido"
        if not self.es_cantidad_posible(apuesta, total_dados): 
            return False, "Cantidad de dados imposible"
        return True
    
    def es_numero_valido(self, apuesta) -> bool:
        return 1 <= apuesta[1] <= 6
    
    def es_cantidad_posible(self, apuesta, total_dados) -> bool:
        return 1 <= apuesta[0] <= total_dados

    def es_mayor_a_la_anterior_pinta(self, apuesta_actual, apuesta_anterior) -> bool:
        return apuesta_actual[1] > apuesta_anterior[1]
    
    def es_mayor_a_la_anterior_num(self, apuesta_actual, apuesta_anterior) -> bool:
        return apuesta_actual[0] > apuesta_anterior[0]