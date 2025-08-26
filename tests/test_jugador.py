

import pytest
from src.juego.jugador import Jugador
from src.juego.cacho import Cacho
from src.juego.dado import Dado

def test_jugador_se_inicializa_con_cacho_y_dados():
   
    jugador = Jugador() #aqui creo una instancia de jugador    
    
    assert isinstance(jugador.cacho, Cacho) #aqui verifico que el jugador tenga un cacho

    assert isinstance(jugador.dados, list) # aqui verifico  que el jugador tenga 5 dados al iniciar la partida
    assert len(jugador.dados) == 5
    
    # Verifica que cada elemento en dados es una instancia de Dado.
    for dado in jugador.dados:
        assert isinstance(dado, Dado)