from .dado import Dado

class Cacho:
    """Representa un cacho con un conjunto de dados."""

    MAX_DADOS = 5
    def __init__(self):
        """Inicializa el cacho con la cantidad máxima de dados."""
        self._dados = [Dado() for _ in range(self.MAX_DADOS)]
    
    def agitar(self) -> str:
        """Agita el cacho y tira todos los dados.

               Returns:
                   str: Mensaje indicando que el cacho fue agitado.
        """
        for dado in self._dados:
            dado.tirar()
        return "Cacho agitado!"
    
    @property
    def resultados_numericos(self) -> list[int]:
        """Obtiene los resultados numéricos de los dados.

        Raises:
            ValueError: Si el cacho aún no ha sido agitado.

        Returns:
            list[int]: Lista de valores obtenidos en la última tirada.
        """
        if any(dado._ultimo_resultado is None for dado in self._dados):
            raise ValueError("El cacho no se ha agitado todavía.")
        return [dado.ultimo_resultado for dado in self._dados]
    
    def pierde_dado(self) -> Dado:
        """Elimina un dado del cacho.

        Raises:
            ValueError: Si no quedan dados en el cacho.

        Returns:
            Dado: El dado que fue retirado.
        """
        if len(self._dados) > 0:
            return self._dados.pop()
        raise ValueError("No quedan dados. Jugador fuera.")
    
    def gana_dado(self, dado: Dado) -> str:
        """Agrega un dado al cacho.

        Args:
            dado (Dado): El dado a agregar.

        Raises:
            ValueError: Si el cacho ya tiene la cantidad máxima de dados.

        Returns:
            str: Mensaje indicando que se ganó un dado.
        """
        if len(self._dados) >= self.MAX_DADOS:
            raise ValueError("Límite de 5 dados alcanzado. Dejar dado en depósito del jugador.")
        else:
            self._dados.append(dado)
            return "Haz ganado un dado!"
    @property
    def dados_actuales(self) -> list[Dado]:
        """Devuelve la lista de dados que están actualmente en el cacho, no en la lista de dados calzados"""
        return self._dados