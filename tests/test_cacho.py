import pytest
from src.juego.cacho import Cacho

def test_agitar(mocker):
    mock_tirar = mocker.patch('src.juego.dado.Dado.tirar')

    cacho_prueba = Cacho()
    mensaje = cacho_prueba.agitar()

    assert mensaje == "Cacho agitado!"
    assert mock_tirar.call_count == 5 #Para verificar que se tiraron 5 dados

def test_resultados(mocker):
    resultados_esperados = [1, 2, 3, 4, 5]

    MockDado = mocker.patch('src.juego.cacho.Dado')

    # Creamos 5 mocks, cada uno con ultimo_resultado configurado
    dados_mock = []
    for valor in resultados_esperados:
        dado_mock = mocker.Mock() 
        dado_mock.ultimo_resultado = valor   
        dados_mock.append(dado_mock)

    MockDado.side_effect = dados_mock

    cacho_prueba = Cacho()
    cacho_prueba.agitar() # Importante agitar el cacho antes del assert (para generar valores)
    valores_obtenidos = cacho_prueba.resultados_numericos

    assert valores_obtenidos == resultados_esperados

def test_pierde_dado():
    cacho_prueba = Cacho() # cacho recien iniciado con sus 5 dados
    cacho_prueba.pierde_dado() # el método debe quitar solo un dado

    assert len(cacho_prueba._dados) == 4