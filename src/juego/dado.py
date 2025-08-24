import random
class Dado: 
    _pintas = {
        1: "as",
        2: "tonto",
        3: "tren",
        4: "cuadra", 
        5: "quina", 
        6: "sexta"
    }

    def __init__(self, generador_numeros=random.randint):
        self._generador = generador_numeros
        self._ultimo_resultado = None
    
    def tirar(self) -> int:
        self._ultimo_resultado = self._generador(1,len(self._pintas))
        return self._ultimo_resultado
    
    @property
    def get_pinta(self) -> str: 
        if self._ultimo_resultado is None: 
            raise ValueError("El dado aún no ha sido tirado.")
        return self._pintas[self._ultimo_resultado]
    
    @property
    def ultimo_resultado(self) -> int:
        if self._ultimo_resultado is None: 
            raise ValueError("El dado aún no ha sido tirado.")
        return self._ultimo_resultado