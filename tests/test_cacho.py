import pytest
from src.juego.cacho import Cacho

def test_agitar(mocker):
    mock_tirar = mocker.patch('src.juego.dado.Dado.tirar')

    cacho_prueba = Cacho()
    mensaje = cacho_prueba.agitar()

    assert mensaje == "Cacho agitado!"
    assert mock_tirar.call_count == 5 #Para verificar que se tiraron 5 dados
