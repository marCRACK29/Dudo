from .dado import Dado

class Cacho:
    def __init__(self):
        self.dados = []

        for _ in range (5):
            self.dados.append(Dado())
    
    def agitar(self) -> str:
        for dado in self.dados:
            dado.tirar()
        return "Cacho agitado!"