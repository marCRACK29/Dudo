

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

def test_ganar_un_dado():
    # Asumimos que un jugador tiene 5 dados
    jugador = Jugador()
    cantidad_inicial_dados = len(jugador.dados)

    # Llamamos al método para ganar un dado
    jugador.ganar_dado()

    # La cantidad de dados debe ser ahora 6, pues puede ganar de a 1 dado
    assert len(jugador.dados) == cantidad_inicial_dados + 1

@pytest.mark.parametrize("cantidad_apuesta, pinta", [
    (2, 5),    
    (3, 1),    
    (6, 6)    
])
def test_realizar_una_apuesta(cantidad_apuesta, pinta):
    jugador = Jugador()
    apuesta = (cantidad_apuesta, pinta)
    
    jugador.realizar_apuesta(apuesta)
    
    assert jugador.apuesta_actual == apuesta

def test_elegir_un_jugador_valido(mocker):
    # Creamos una lista de jugadores simulados
    jugadores_disponibles = [Jugador(), Jugador(), Jugador()]
    
    mocker.patch(
        'src.juego.jugador.random.choice',
        return_value=jugadores_disponibles[1]
    )
     # Creamos un jugador "activo" para llamar al método
    jugador_activo = Jugador()

    # Elige un jugador El método interno ahora usará nuestro mock.
    jugador_elegido = jugador_activo.elegir_jugador(jugadores_disponibles)
    
     # Aseguramos que el jugador elegido es el que esperamos (el segundo).
    assert jugador_elegido == jugadores_disponibles[1]

def test_lanzar_dado(mocker):
    jugador = Jugador()

    MockDado = mocker.patch('src.juego.jugador.Dado')
    dado_mock = mocker.Mock()
    dado_mock.tirar.return_value = 6
    MockDado.return_value = dado_mock

    assert jugador.lanzar_un_dado() == 6
