import pytest
from src.juego.gestor_partida import GestorPartida
from src.juego.arbitro_ronda import OpcionesJuego, Rotacion
from src.juego.jugador import Jugador
import src.juego.arbitro_ronda as modulo_arbitro
from src.servicios.desiciones_simuladas import ProveedorScripted


@pytest.mark.parametrize("cantidad_jugadores",
    [2, 5, 6, 8]
)
def test_creacion_jugadores(cantidad_jugadores):
    partida = GestorPartida(cantidad_jugadores)
    jugadores = partida.jugadores
    assert len(jugadores) == cantidad_jugadores
    for jugador in jugadores:
        assert isinstance(jugador, Jugador)

@pytest.mark.parametrize("datos_lanzamientos, resultado",
    [
        ([1, 2, 3, 4, 5, 6], 5),
        ([1, 2, 3, 4, 6, 6, 6, 1], 4),
        ([6, 6, 6, 6, 6, 6, 1, 1, 6, 1, 6, 1, 3, 5], 4)
    ]
)
def test_seis_jugadores_lanzan_controlado(mocker, datos_lanzamientos, resultado):
    # Parchea Dado EN EL MÓDULO donde se usa (jugador.py)
    MockDado = mocker.patch('src.juego.gestor_partida.Jugador')
    # Cada llamada a .tirar() devolverá, en orden: 1,2,3,4,5,6
    MockDado.return_value.lanzar_un_dado.side_effect = datos_lanzamientos

    partida = GestorPartida(6)

    assert partida.primer_jugador == resultado

def _set_mano(jugador, mano):
    """Fija una mano determinista en el cacho del jugador."""
    class _FakeDado:
        def __init__(self, val):
            self._ultimo_resultado = val
        @property
        def ultimo_resultado(self):
            return self._ultimo_resultado
        def tirar(self):
            return self._ultimo_resultado
    # Sustituimos los dados internos del cacho
    jugador.cacho._dados = [_FakeDado(v) for v in mano]


@pytest.mark.parametrize(
    "manos, llamadas_esperadas, resultado",
    [
        # Caso A: J0 apuesta (2,5) -> J1 apuesta (3,5) -> J2 DUDO
        # Con las manos dadas, quinas reales+ases determinan si J2 gana o pierde un dado.
        (
            [[3, 3, 2, 6, 1],   # J0
             [4, 1, 3, 2, 5],   # J1
             [6, 6, 2, 2, 5]],  # J2
            [
                (OpcionesJuego.APUESTO, (2, 5)),
                (OpcionesJuego.APUESTO, (3, 5)),
                (OpcionesJuego.DUDO, None),
            ],
            # resultado = (ganador_id, perdedor_id)
            # Con estas manos: quinas=2 (J1 y J2) + ases=2 (J0 y J1 cuando cara!=1) => total=4
            # Apuesta anterior fue (3,5) -> DUDO es INCORRECTO si total >= 3, por lo tanto J2 pierde un dado
            [5, 5, 4],
        ),
        # Caso B: J0 apuesta (1,1) -> J1 CALZO
        (
            [[1, 1, 2, 3, 4],  # J0
             [1, 2, 3, 4, 5]], # J1
            [
                (OpcionesJuego.APUESTO, (1, 1)),
                (OpcionesJuego.CALZO, None),
            ],
            # Contar 1s exactos = 3; calzo con apuesta=1 es INCORRECTO, J1 pierde un dado
            [5, 4],
        ),
    ],
    ids=[
        "apuesto_apuesto_dudo",
        "apuesto_calzo",
    ]
)
def test_jugar_ronda(monkeypatch, manos, llamadas_esperadas, resultado):
    num_jugadores = len(manos)

    # 1) Forzar primer jugador determinista (0) para no depender de tiradas iniciales
    monkeypatch.setattr(
        GestorPartida,
        "_elegir_primer_jugador",
        lambda self, n: setattr(self, "primer_jugador", 0),
    )

    # 2) Parchear ValidadorApuesta para que siempre "valide" la apuesta sin lanzar
    class _ValidadorFake:
        def es_apuesta_valida(self, *args, **kwargs):
            return (True, "ok")
    monkeypatch.setattr(modulo_arbitro, "ValidadorApuesta", lambda: _ValidadorFake())

    # 3) Crear partida y árbitro real
    partida = GestorPartida(num_jugadores)
    partida.generar_arbitro(Rotacion.HORARIO)

    # 4) Fijar manos deterministas
    for j, mano in zip(partida.jugadores, manos):
        _set_mano(j, mano)

    # 5) Se genera un proveedor de desiciones a modo de mock. En un entorno real va seria con input directo del usuario
    proveedor = ProveedorScripted(llamadas_esperadas)

    # 6) Ejecutar la ronda
    partida.jugar_ronda(proveedor)

    # 7) Snapshot de dados después y detectar quién empieza la próxima ronda
    despues = [jug.total_de_dados_en_juego() for jug in partida.jugadores]


    assert despues == resultado
