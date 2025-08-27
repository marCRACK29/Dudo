class ValidadorApuesta:
    def es_apuesta_valida(self, apuesta, apuesta_anterior, total_dados) -> bool:
        if not self.es_numero_valido(apuesta):
            return False, "Número inválido"
        if not self.es_cantidad_posible(apuesta, total_dados): 
            return False, "Cantidad de dados imposible"
        if not self.es_mayor_a_la_anterior(apuesta, apuesta_anterior):
            return False, "No se esta respetando la jerarquía"
        return True
    
    def es_numero_valido(self, apuesta) -> bool:
        return 1 <= apuesta[1] <= 6
    
    def es_cantidad_posible(self, apuesta, total_dados) -> bool:
        return 1 <= apuesta[0] <= total_dados
    
    def es_mayor_a_la_anterior(self, apuesta_actual, apuesta_anterior) -> bool: 
        if apuesta_actual[1] == apuesta_anterior[1]: # misma pinta 
            return apuesta_actual[0] > apuesta_anterior[0] # los números deben respetar la jerarquia
        else: #pintas distintas
            if apuesta_actual[0] >= apuesta_anterior[0]: # 3 cuadras y 3 quintas seria un ejemplo válido
                return apuesta_actual[1] > apuesta_anterior[1] # entonces las pintas deben respetar jerarquia
            else: #pintas distintas, pero no respeta la jerarquia de números
                #ej: (cuatro quintas) y luego (dos sextas) -> respeta pintas, pero no numeros
                return False