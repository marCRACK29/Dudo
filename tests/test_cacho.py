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
    dados_mock = []

    for numero in resultados_esperados:
        dado_mock = mocker.Mock()
        dado_mock.tirar.return_value = numero
        dados_mock.append(dado_mock)
    
    MockDado.side_effect = dados_mock

    cacho_prueba = Cacho()
    valores_obtenidos = cacho_prueba.resultados()
    assert valores_obtenidos == resultados_esperados

       
