from .dado import Dado

class Cacho:
    def __init__(self):
        self.dados = [Dado() for _ in range(5)]
    
    def agitar(self) -> str:
        for dado in self.dados:
            dado.tirar()
        return "Cacho agitado!"