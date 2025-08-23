class Dado: 
    def __init__(self, generador_numeros):
        self._generador = generador_numeros
        self._ultimo_resultado = None
    
    def tirar(self) -> int:
        self._ultimo_resultado = self._generador(1,6)
        return self._ultimo_resultado
        