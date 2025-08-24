import pytest
from src.juego.cacho import Cacho

def test_agitar(capsys):
    cacho_prueba = Cacho()
    cacho_prueba.agitar()

    mensaje = capsys.readouterr()

    assert mensaje.out == "Cacho agitado!"
