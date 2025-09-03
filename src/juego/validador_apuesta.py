from typing import Optional, Tuple
Apuesta = Tuple[int, int]  # (cantidad, pinta)

class ValidadorApuesta:
    def es_apuesta_valida(
        self,
        apuesta: Apuesta,
        apuesta_anterior: Apuesta | None,
        total_dados: int, 
        jugador_con_un_dado: bool = False
    ) -> tuple[bool, str]:
        """Valida si una apuesta cumple las reglas del juego.

               Args:
                   apuesta (Apuesta): Apuesta actual (cantidad, pinta).
                   apuesta_anterior (Apuesta | None): Apuesta previa o None si es la primera.
                   total_dados (int): Cantidad total de dados en juego.
                   jugador_con_un_dado (bool, optional): Indica si el jugador tiene un dado.

               Returns:
                   tuple[bool, str]: True y mensaje si es válida, False y motivo si no.
               """
        if apuesta_anterior is None and apuesta[1] == 1:
            if not jugador_con_un_dado:
                return False, "No puedes comenzar apostando con as si tienes más de un dado"
        if not self._es_numero_valido(apuesta):
            return False, "Número inválido"
        if not self._es_cantidad_posible(apuesta, total_dados): 
            return False, "Cantidad de dados imposible"
        if apuesta_anterior is not None:
            if apuesta[1] == 1 and apuesta_anterior[1] != 1: # si se cambia de "pintas normales" a ases
                if not self._cambiar_a_ases(apuesta, apuesta_anterior):
                    return False, "No se respeta el cambio a ases"
            elif apuesta[1] != 1 and apuesta_anterior[1] == 1: # si se cambia de ases a "pintas normales"
                if not self._cambiar_de_ases(apuesta, apuesta_anterior):
                    return False, "No se respeta el cambio desde ases"
            else: 
                if not self._es_mayor_a_la_anterior(apuesta, apuesta_anterior):
                    return False, "No se esta respetando la jerarquía"
        return True, "OK"
    
    def _es_numero_valido(self, apuesta: Apuesta) -> bool:
        """Verifica que la pinta esté entre 1 y 6."""
        return 1 <= apuesta[1] <= 6
    
    def _es_cantidad_posible(self, apuesta: Apuesta, total_dados: int) -> bool:
        """Verifica que la cantidad esté dentro de los dados en juego."""
        return 1 <= apuesta[0] <= total_dados
    
    def _es_mayor_a_la_anterior(self, apuesta_actual: Apuesta, apuesta_anterior: Apuesta) -> bool:
        """Comprueba si la apuesta actual supera a la anterior según jerarquía."""
        if apuesta_anterior is None:
            return True
        if apuesta_actual[1] == apuesta_anterior[1]: # misma pinta
            return apuesta_actual[0] > apuesta_anterior[0] # los números deben respetar la jerarquia

        if apuesta_actual[0] >= apuesta_anterior[0]: # 3 cuadras y 3 quintas seria un ejemplo válido
            return apuesta_actual[1] > apuesta_anterior[1] # entonces las pintas deben respetar jerarquia

        #pintas distintas, pero no respeta la jerarquia de números
        #ej: (cuatro quintas) y luego (dos sextas) -> respeta pintas, pero no numeros
        return False
    
    def _cambiar_a_ases(self, apuesta_actual, apuesta_anterior) -> bool:
        """Valida el cambio de pintas normales a ases según las reglas."""
        res = apuesta_anterior[0]//2 + 1
        if res == apuesta_actual[0]: 
            return True
        else: 
            return False
        
    def _cambiar_de_ases(self, apuesta_actual, apuesta_anterior) -> bool:
        """Valida el cambio de ases a pintas normales según las reglas."""
        res = apuesta_anterior[0]*2 + 1
        if res == apuesta_actual[0]:
            return True
        else: 
            return False
