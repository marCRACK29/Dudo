import pytest
from src.juego.jugador import Jugador

def test_es_numero_valido():
    jugador_uno = Jugador()
    jugador_dos = Jugador()

    jugador_uno.realizar_apuesta((3, 4)) # 3 cuadras - válido
    jugador_dos.realizar_apuesta((3, 7)) # 3 siete - inválido

    validador_prueba = ValidadorPrueba()

    apuesta_uno = jugador_uno.apuesta_actual
    apuesta_dos = jugador_dos.apuesta_actual

    valido = validador_prueba.es_apuesta_valida(apuesta_uno)
    invalido = validador_prueba.es_apuesta_valida(apuesta_dos)

    assert valido == True
    assert invalido == False
