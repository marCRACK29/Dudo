import pytest

from src.juego.arbitro_ronda import ArbitroRonda, Rotacion


@pytest.mark.parametrize(
    "inicial, cantidad, esperado",
    [
        (1, 6, 2),
        (3, 5, 4),
        (4, 6, 5),
        (1, 2, 0)
    ],
    ids=["empieza_1","empieza_3","empieza_4", "empieza_1_y_da_vuelta"]
)
def test_rotacion_jugadores_horaria(inicial,cantidad, esperado):
    arbitro = ArbitroRonda(inicial, cantidad)
    arbitro.siguiente_jugador()
    assert arbitro.jugador_actual_id == esperado

@pytest.mark.parametrize(
    "inicial, cantidad, esperado",
    [
        (1, 6, 0),
        (0, 5, 4),
        (4, 6, 3),
        (0, 2, 1)
    ],
    ids=["empieza_1","empieza_0","empieza_4", "empieza_0_y_da_vuelta"]
)
def test_rotacion_jugadores_antihoraria(inicial, cantidad, esperado):
    arbitro = ArbitroRonda(inicial, cantidad, Rotacion.ANTIHORARIO)
    arbitro.siguiente_jugador()
    assert arbitro.jugador_actual_id == esperado

@pytest.mark.parametrize(
    "inicial, cantidad, excepcion_str",
    [
        (-2, 2, "Jugador inicial negativo"),
        (5, 4, "Jugador inicial superior a cantidad de jugadores"),
        (4, 4, "Jugador inicial superior a cantidad de jugadores"), # se empiezan a contar los jugadores desde el 0

    ],
    ids=[
        "Cantidad negativa",
        "Jugador con id superior a la cantidad",
        "Jugador con id superior a la cantidad (verificando cantidad igual)"
    ]
)
def test_parametros_imposibles(inicial, cantidad, excepcion_str):
    with pytest.raises(ValueError, match=excepcion_str):
        arbitro = ArbitroRonda(inicial, cantidad)


@pytest.mark.parametrize(
    "rotacion_invalida",
    [
        "hola mundo",
        5,
        -1
    ],
    ids=[
        "instancia incorrecta de string",
        "instancia incorrecta de int",
        "instancia incorrecta de float"
    ]
)
def test_no_es_rotacion(rotacion_invalida):
    with pytest.raises(ValueError, match="Valor dado no es una Rotacion"):
        arbitro = ArbitroRonda(4,5, rotacion_invalida)


