import pytest
from src.juego.jugador import Jugador
from src.juego.cacho import Cacho
from src.juego.dado import Dado

def test_jugador_se_inicializa_correctamente():
    jugador = Jugador()
    
    # 1. Verifica que el jugador tiene un cacho
    assert isinstance(jugador.cacho, Cacho)
    
    # 2. Verifica que la lista de dados calzados está vacía al inicio
    assert isinstance(jugador.dados_calzados, list)
    assert len(jugador.dados_calzados) == 0
    
    # 3. Verifica que el cacho tiene 5 dados al inicio
    # Nota: esto asume que tienes una propiedad en Cacho que expone la lista de dados
    assert len(jugador.cacho.dados_actuales) == 5
 
def test_perder_un_dado_de_la_reserva_de_dados():
    jugador = Jugador() #creamos un jugador con 5 dados

    jugador.dados_calzados.append(Dado()) #agregamos un dado a la lista de dados extra, es decir dados calzados

    jugador.perder_dado() # aplicamos perder dado para que logicamente revise si hay dados extra que pueda eliminar o no

    assert len(jugador.dados_calzados) == 0 #hacemos un assert a la lista de dados extra, que antes tenia uno y ahora debe tener 0 
    assert len(jugador.cacho.dados_actuales) == 5 #hacemos un assert a la lista de dados del cacho, que antes tenia 5 y deberia tener 5 

def test_perder_un_dado_si_no_hay_dados_extra(mocker):
    jugador = Jugador()

    mocker.patch.object(jugador.cacho, 'pierde_dado')

    jugador.perder_dado()

    jugador.cacho.pierde_dado.assert_called_once()

    assert len(jugador.cacho.dados_actuales) == 5


def test_ganar_un_dado_si_hay_dados_extra():
    jugador = Jugador()

    jugador.ganar_dado()

    assert len(jugador.cacho.dados_actuales) == 5
    assert len(jugador.dados_calzados) == 1

def test_ganar_dados_si_no_cacho_no_esta_lleno(mocker):
    jugador = Jugador()

    mocker.patch.object(jugador.cacho, '_dados')
    jugador.cacho._dados = ([Dado() for _ in range(4)])

    jugador.ganar_dado()

    assert len(jugador.cacho.dados_actuales) == 5
    assert len(jugador.dados_calzados) == 0

    


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
