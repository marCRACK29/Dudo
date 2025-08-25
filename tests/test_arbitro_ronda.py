import pytest
from src.juego.arbitro_ronda import ArbitroRonda


@pytest.mark.parametrize(
    "inicial, cantidad, esperado",
    [
        (1, 6, 2),
        (3, 5, 4),
        (4, 6, 5),
        (1, 2, 0)
    ],
    ids=["empieza_1","empieza_3","empieza_4", "empieza_2_y_da_vuelta"]
)
def test_rotacion_jugadores_horaria(inicial,cantidad, esperado):
    arbitro = ArbitroRonda(inicial, cantidad)
    arbitro.siguiente_jugador()
    assert arbitro.jugador_actual_id == esperado