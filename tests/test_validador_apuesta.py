import pytest
from src.juego.validador_apuesta import ValidadorApuesta

@pytest.fixture
def validador():
    return ValidadorApuesta()

def test_es_numero_valido(validador):
    apuesta_uno = (3, 4) # 3 cuadras - valido
    apuesta_dos = (3, 7) # 3 siete - inválido

    apuesta_anterior = (0,0) # para este test no es importante la apuesta anterior

    valido = validador.es_apuesta_valida(apuesta_uno, apuesta_anterior,  total_dados=10)
    invalido = validador.es_apuesta_valida(apuesta_dos, apuesta_anterior, total_dados=10)

    assert valido == (True, "OK")
    assert invalido == (False, 'Número inválido')

def test_cantidad_imposible(validador):
    total_dados = 10
    apuesta = (11, 4) # 11 cuadras y hay solo 10 dados
    apuesta_anterior = (0,0) # para este test no es importante la apuesta anterior

    invalido = validador.es_apuesta_valida(apuesta, apuesta_anterior, total_dados)
    
    assert invalido == (False, 'Cantidad de dados imposible')

def test_apuesta_respetando_jerarquia_pinta(validador):
    apuesta_uno = (3, 3) # tres trenes
    apuesta_dos = (3, 2) # tres tontos
    
    # De tres trenes a tres tontos -> no se puede bajar de pinta
    invalido = validador.es_apuesta_valida(apuesta_dos, apuesta_anterior=apuesta_uno, total_dados=10)

    valido = validador.es_apuesta_valida(apuesta_uno, apuesta_dos, total_dados=10)
    
    assert invalido == (False, 'No se esta respetando la jerarquía')
    assert valido == (True, "OK")
    
def test_apuesta_respetando_jerarquia_numero(validador):
    apuesta_uno = (3, 3) # tres trenes
    apuesta_dos = (2, 3) # dos trenes
    
    # De tres trenes a dos trenes -> no se puede bajar de número
    invalido = validador.es_apuesta_valida(apuesta_dos, apuesta_anterior=apuesta_uno, total_dados=10)
    valido = validador.es_apuesta_valida(apuesta_uno, apuesta_dos, total_dados=10)
    
    assert invalido == (False, 'No se esta respetando la jerarquía')
    assert valido == (True,  "OK") #imprime: False, No se respeta el cambio desde ases'

def test_cambiar_a_ases(validador):
    apuesta_normal = (8, 3) # 8 trenes
    apuesta_ases_uno = (5, 1) # 5 ases
    apuesta_ases_dos = (4, 1) # 4 ases


    valido = validador.es_apuesta_valida(apuesta=apuesta_ases_uno, apuesta_anterior=apuesta_normal, total_dados=10)
    invalido = validador.es_apuesta_valida(apuesta=apuesta_ases_dos, apuesta_anterior=apuesta_normal, total_dados=10)

    assert invalido == (False, "No se respeta el cambio a ases")
    assert valido == (True, "OK")

def test_cambiar_de_ases(validador):
    apuesta_normal = (7, 3) # 7 trenes
    apuesta_ases_uno = (4, 1) # 4 ases
    apuesta_ases_dos = (3, 1) # 3 ases


    valido = validador.es_apuesta_valida(apuesta=apuesta_normal, apuesta_anterior=apuesta_ases_dos, total_dados=10)
    invalido = validador.es_apuesta_valida(apuesta=apuesta_normal, apuesta_anterior=apuesta_ases_uno, total_dados=10)

    assert invalido == (False, "No se respeta el cambio desde ases")
    assert valido == (True, "OK")

def test_primera_apuesta_con_as(validador):
    apuesta = (3,1)
    valido = validador.primero_ases(apuesta, apuesta_anterior=None, jugador_con_un_dado=True)
    invalido = validador.primero_ases(apuesta, apuesta_anterior=(3, 2), jugador_con_un_dado=False)

    assert valido == True
    assert invalido == False



