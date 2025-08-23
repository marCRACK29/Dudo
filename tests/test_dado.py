import pytest
from src.juego.dado import Dado

def test_tirar_dado(mocker):
    numero_esperado = 3
    mocker.patch('src.juego.dado.random.randint', return_value=numero_esperado)

    dado_prueba = Dado()
    resultado = dado_prueba.tirar_dado()

    assert resultado == numero_esperado

