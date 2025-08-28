import pytest

from src.juego.arbitro_ronda import ArbitroRonda, Rotacion
from src.juego.jugador import Jugador

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
    jugadores = [Jugador() for i in range(cantidad)]
    arbitro = ArbitroRonda(inicial, jugadores=jugadores)
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
    jugadores = [Jugador() for i in range(cantidad)]
    arbitro = ArbitroRonda(inicial, jugadores, Rotacion.ANTIHORARIO)
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
    jugadores = [Jugador() for i in range(cantidad)]
    with pytest.raises(ValueError, match=excepcion_str):
        arbitro = ArbitroRonda(inicial, jugadores)


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
        jugadores = [Jugador() for i in range(5)]
        arbitro = ArbitroRonda(4,jugadores=jugadores, rotacion=rotacion_invalida)


def _set_mano(monkeypatch, jugador: Jugador, mano: list[int]):
    """
    Sombrea la property `resultados_numericos` SOLO en la instancia jugador.cacho
    para no depender de `agitar()`. Permite manos distintas por jugador.
    """
    monkeypatch.setattr(jugador.cacho, "resultados_numericos", list(mano), raising=False)

@pytest.mark.parametrize(
    "manos, adivinanza, esperado",
    [
        # Apuesta normal: ases como comodines
        (
            [[3, 3, 2, 6, 1], [4, 1, 3, 2, 5]],  # total trenes efectivos: 5
            (4, 3),
            True
        ),
        # Apuesta a ases: no hay comodín (cuentan solo los 1)
        (
            [[1, 3, 1, 6, 2], [4, 1, 3, 2, 5]],  # total ases: 3
            (3, 1),
            True
        ),
        # Insuficiente: incluso contando comodines no alcanza
        (
            [[5, 2, 3, 6, 2], [4, 1, 3, 2, 5]],  # quinas reales 2 + ases 1 = 3
            (6, 5),
            False
        ),
        # Varios jugadores, mezcla de reales y ases
        (
            [[4, 4, 1, 2, 6], [2, 4, 3, 1, 1], [6, 6, 6, 2, 4]],  # cuatros efectivos: (2+1)+(1+2)+(1)=7
            (5, 4),
            True
        ),
    ],
    ids=[
        "apuesta_normal_con_ases_comodin",
        "apuesta_a_ases_sin_comodin",
        "apuesta_insuficiente",
        "varios_jugadores_mezcla"
    ]
)
def test_definir_ganador(manos, adivinanza, esperado, monkeypatch):
    jugadores = [Jugador() for _ in range(len(manos))]
    for j, mano in zip(jugadores, manos):
        _set_mano(monkeypatch, j, mano)

    arbitro = ArbitroRonda(0, jugadores)
    assert arbitro.definir_ganador(adivinanza) is esperado



