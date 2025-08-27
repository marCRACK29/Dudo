import pytest
from src.juego.jugador import Jugador
from src.juego.validador_apuesta import ValidadorApuesta

@pytest.fixture
def validador():
    return ValidadorApuesta()

def test_es_numero_valido(validador):
    jugador_uno = Jugador()
    jugador_dos = Jugador()

    jugador_uno.realizar_apuesta((3, 4)) # 3 cuadras - válido
    jugador_dos.realizar_apuesta((3, 7)) # 3 siete - inválido

    apuesta_uno = jugador_uno.apuesta_actual
    apuesta_dos = jugador_dos.apuesta_actual

    valido = validador.es_apuesta_valida(apuesta_uno, total_dados=10)
    invalido = validador.es_apuesta_valida(apuesta_dos, total_dados=10)

    assert valido == True
    assert invalido == (False, 'Número inválido')

def test_cantidad_imposible(validador):
    jugador_uno = Jugador()
    total_dados = 10
    jugador_uno.realizar_apuesta((11, 4)) # 11 cuadras y hay solo 10 dados
    apuesta = jugador_uno.apuesta_actual
    invalido = validador.es_apuesta_valida(apuesta, total_dados)

    assert invalido == (False, 'Cantidad de dados imposible')

def test_apuesta_respetando_jerarquia_pinta(validador):
    jugador_uno = Jugador()
    jugador_dos = Jugador()
    jugador_uno.realizar_apuesta((3, 3)) # tres trenes
    jugador_dos.realizar_apuesta((3, 2)) # tres tontos -> baja de pinta y eso no se puede 
    apuesta_uno = jugador_uno.apuesta_actual
    apuesta_dos = jugador_dos.apuesta_actual
    
    invalido = validador.es_mayor_a_la_anterior_pinta(apuesta_actual=apuesta_dos, apuesta_anterior=apuesta_uno)
    valido = validador.es_mayor_a_la_anterior_pinta(apuesta_uno, apuesta_dos)
    
    assert invalido == False
    assert valido == True
    
    
