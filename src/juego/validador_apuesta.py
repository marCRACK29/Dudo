from typing import Optional, Tuple
Apuesta = Tuple[int, int]  # (cantidad, pinta)

class ValidadorApuesta:
    def es_apuesta_valida(
        self,
        apuesta: Apuesta,
        apuesta_anterior: Apuesta | None,
        total_dados: int
    ) -> tuple[bool, str]:
        if not self._es_numero_valido(apuesta):
            return False, "Número inválido"
        if not self._es_cantidad_posible(apuesta, total_dados): 
            return False, "Cantidad de dados imposible"
        if not self._es_mayor_a_la_anterior(apuesta, apuesta_anterior):
            return False, "No se esta respetando la jerarquía"
        return True, "OK"
    
    def _es_numero_valido(self, apuesta: Apuesta) -> bool:
        return 1 <= apuesta[1] <= 6
    
    def _es_cantidad_posible(self, apuesta: Apuesta, total_dados: int) -> bool:
        return 1 <= apuesta[0] <= total_dados
    
    def _es_mayor_a_la_anterior(self, apuesta_actual: Apuesta, apuesta_anterior: Apuesta) -> bool:
        if apuesta_anterior is None:
            return True
        if apuesta_actual[1] == apuesta_anterior[1]: # misma pinta
            return apuesta_actual[0] > apuesta_anterior[0] # los números deben respetar la jerarquia

        if apuesta_actual[0] >= apuesta_anterior[0]: # 3 cuadras y 3 quintas seria un ejemplo válido
            return apuesta_actual[1] > apuesta_anterior[1] # entonces las pintas deben respetar jerarquia

        #pintas distintas, pero no respeta la jerarquia de números
        #ej: (cuatro quintas) y luego (dos sextas) -> respeta pintas, pero no numeros
        return False