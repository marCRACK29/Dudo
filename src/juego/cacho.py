from .dado import Dado

class Cacho:
    def __init__(self):
        self._dados = [Dado() for _ in range(5)]
    
    def agitar(self) -> str:
        for dado in self._dados:
            dado.tirar()
        return "Cacho agitado!"
    
    @property
    def resultados_numericos(self) -> list[int]:
        if any(dado._ultimo_resultado is None for dado in self._dados):
            raise ValueError("El cacho no se ha agitado todavía.")
        return [dado.ultimo_resultado for dado in self._dados]