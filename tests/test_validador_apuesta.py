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

    valido = validador.es_apuesta_valida(apuesta_uno)
    invalido = validador.es_apuesta_valida(apuesta_dos)

    assert valido == True
    assert invalido == (False, 'Número inválido')

def test_cantidad_imposible(validador):
    jugador_uno = Jugador()
    total_dados = 10
    jugador_uno.realizar_apuesta((11, 4)) # 11 cuadras y hay solo 10 dados
    apuesta = jugador_uno.apuesta_actual
    invalido = validador.es_cantidad_posible(apuesta, total_dados)

    assert invalido == False

