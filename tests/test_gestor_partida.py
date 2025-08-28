import pytest
from src.juego.gestor_partida import GestorPartida
from src.juego.jugador import Jugador


@pytest.mark.parametrize("cantidad_jugadores",
    [2, 5, 6, 8]
)
def test_creacion_jugadores(cantidad_jugadores):
    partida = GestorPartida(cantidad_jugadores)
    jugadores = partida.jugadores
    assert len(jugadores) == cantidad_jugadores
    for jugador in jugadores:
        assert isinstance(jugador, Jugador)


def test_seis_jugadores_lanzan_controlado(mocker):
    # Parchea Dado EN EL MÓDULO donde se usa (jugador.py)
    MockDado = mocker.patch('src.juego.jugador.Jugador')
    # Cada llamada a .tirar() devolverá, en orden: 1,2,3,4,5,6
    MockDado.return_value.tirar.side_effect = [1, 2, 3, 4, 5, 6]

    partida = GestorPartida(6)


    assert partida.primer_jugador == 5
