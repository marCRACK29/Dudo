import pytest

def test_tirar_dado():
    dado = Dado()
    resultado = dado.tirar_dado()
    assert resultado == 4
