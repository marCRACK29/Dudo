import pytest
from src.juego.cacho import Cacho

def test_agitar(capsys):
    cacho_prueba = Cacho()
    mensaje = cacho_prueba.agitar()

    assert mensaje == "Cacho agitado!"
