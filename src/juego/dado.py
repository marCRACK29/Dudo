import random
class Dado:
    """Representa un dado del juego Dudo."""
    _pintas = {
        1: "as",
        2: "tonto",
        3: "tren",
        4: "cuadra",
        5: "quina",
        6: "sexta"
    }

    def __init__(self, generador_numeros=random.randint):
        """Inicializa el dado con un generador de números aleatorios.

        Args:
            generador_numeros (Callable): Función que genera números aleatorios.
                Por defecto es random.randint.
        """
        self._generador = generador_numeros
        self._ultimo_resultado = None

    def tirar(self) -> int:
        """Lanza el dado y guarda el resultado.

        Returns:
            int: El valor numérico obtenido (1-6).
        """
        self._ultimo_resultado = self._generador(1, len(self._pintas))
        return self._ultimo_resultado

    @property
    def pinta(self) -> str:
        """Devuelve la pinta asociada al último resultado.

        Raises:
            ValueError: Si el dado aún no ha sido tirado.

        Returns:
            str: Nombre de la pinta correspondiente.
        """
        if self._ultimo_resultado is None:
            raise ValueError("El dado aún no ha sido tirado.")
        return self._pintas[self._ultimo_resultado]

    @property
    def ultimo_resultado(self) -> int:
        """Obtiene el último valor numérico del dado.

        Raises:
            ValueError: Si el dado aún no ha sido tirado.

        Returns:
            int: Último valor numérico (1-6).
        """
        if self._ultimo_resultado is None:
            raise ValueError("El dado aún no ha sido tirado.")
        return self._ultimo_resultado