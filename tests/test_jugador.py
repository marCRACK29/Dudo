

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

def test_cuantos_dados_tiene_el_jugador():
    # Asume un jugador con 5 dados al inicio.
    jugador = Jugador()
    
    # El método debe devolver 5.
    cantidad_dados = jugador.total_de_dados()
    
    # Afirma que el resultado es 5.
    assert cantidad_dados == 5

def test_perder_un_dado():
    # Asume un jugador con 5 dados
    jugador = Jugador()
    cantidad_inicial_dados = len(jugador.dados)
    
    # Llama al método para perder un dado
    jugador.perder_dado()
    
    # La cantidad de dados debe ser ahora 4, pues siempre se pierde de a 1 dado
    assert len(jugador.dados) == cantidad_inicial_dados - 1