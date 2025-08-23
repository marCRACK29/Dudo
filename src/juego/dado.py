import random

class Dado: 
    def __init__(self):
        self.numero = None
    
    def tirar_dado(self) -> int:
        self.numero = random.randint(1, 6)
        return self.numero
        