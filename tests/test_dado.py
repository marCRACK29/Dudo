import pytest
from src.juego.dado import Dado

# Ejecutar test 3 veces con 3 valores (1, 3, y 6)
@pytest.mark.parametrize("numero_esperado", [1, 3, 6])
def test_tirar_dado(mocker, numero_esperado):
    mock_prueba = mocker.Mock(return_value=numero_esperado)

    dado_prueba = Dado(mock_prueba)
    resultado = dado_prueba.tirar()

    assert resultado == numero_esperado
    mock_prueba.assert_called_once_with(1, 6)

@pytest.mark.parametrize("numero", "pinta_esperada", [
    (1, "as"),
    (2, "tonto"), 
    (3, "tren"),
    (4, "cuadra"), 
    (5, "quina"), 
    (6, "sexta")
])
def test_get_pinta(mocker, numero, pinta_esperada):
    mock_prueba = mocker.Mock(return_value=numero)

    dado_prueba = Dado(mock_prueba)
    dado_prueba.tirar()
    resultado = dado_prueba.get_pinta()

    assert resultado == pinta_esperada

