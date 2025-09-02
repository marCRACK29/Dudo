import pytest
import src.juego.arbitro_ronda as modulo_arbitro

from src.juego.gestor_partida import GestorPartida
from src.juego.enums import OpcionesJuego, Rotacion
from src.juego.jugador import Jugador
from src.servicios.desiciones_simuladas import ProveedorScripted

class ArbitroDummy:
    """Stub de árbitro para tests de GestorPartida."""
    def __init__(self):
        self.jugador_actual_id = 0
        self.apuesta_anterior = None  # mismo atributo que usa el real

    def procesar_jugada(self, decision, apuesta):
        if decision == OpcionesJuego.APUESTO:
            self.apuesta_anterior = apuesta

    def siguiente_jugador(self):
        pass

    def reiniciar_ronda(self):
        self.apuesta_anterior = None

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

def _set_mano_respetando_cantidad(jugador: Jugador, valores):
    """Solo usa tantos valores como dados tenga el jugador actualmente."""
    k = len(jugador.cacho._dados)
    _set_mano(jugador, valores[:k])

@pytest.mark.parametrize("cantidad_jugadores",
    [2, 5, 6, 8]
)
def test_creacion_jugadores(cantidad_jugadores):
    """ Test para verificar la cantidad de jugadores creados"""
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
    ], ids = ["Gana_sin_empate_5", "Gana_un_empate_4", "Gana_dos_empate_4"]
)
def test_seis_jugadores_lanzan_controlado(mocker, datos_lanzamientos, resultado):
    """Test para simular el primer jugador que juega con lanzamientos de dados deterministas"""
    MockDado = mocker.patch('src.juego.gestor_partida.Jugador')
    MockDado.return_value.lanzar_un_dado.side_effect = datos_lanzamientos

    partida = GestorPartida(6)

    assert partida.primer_jugador == resultado

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
                (OpcionesJuego.APUESTO, (1, 2)),
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
    """Test para simular una sola ronda y verificar la cantidad de dados con jugadas simuladas"""
    num_jugadores = len(manos)

    monkeypatch.setattr(
        GestorPartida,
        "_elegir_primer_jugador",
        lambda self, n: setattr(self, "primer_jugador", 0),
    )

    partida = GestorPartida(num_jugadores)
    partida.generar_arbitro(Rotacion.HORARIO)

    # Fijar manos deterministas
    for j, mano in zip(partida.jugadores, manos):
        _set_mano(j, mano)

    # Mock de las desiciones que se toman
    proveedor = ProveedorScripted(llamadas_esperadas)

    partida.jugar_ronda(proveedor)

    # Snapshot de dados después y detectar quién empieza la próxima ronda
    despues = [jug.total_de_dados_en_juego() for jug in partida.jugadores]

    assert despues == resultado

def test_jugar_dos_rondas(monkeypatch):
    """Se verifica que jugando 2 rondas la partida no tenga problemas"""
    monkeypatch.setattr(
        GestorPartida,
        "_elegir_primer_jugador",
        lambda self, n: setattr(self, "primer_jugador", 0),
    )
    partida = GestorPartida(3)
    partida.generar_arbitro(Rotacion.ANTIHORARIO)

    # ---------- RONDA 1 ----------
    manos_r1 = [
        [3, 3, 2, 6, 1],   # J0
        [4, 1, 3, 2, 5],   # J1
        [6, 6, 2, 2, 5],   # J2
    ]
    for j, mano in zip(partida.jugadores, manos_r1):
        _set_mano_respetando_cantidad(j, mano)

    proveedor_r1 = ProveedorScripted([
        (OpcionesJuego.APUESTO, (2, 5)),
        (OpcionesJuego.APUESTO, (3, 5)),
        (OpcionesJuego.DUDO, None),
    ])

    partida.jugar_ronda(proveedor_r1)

    despues_r1 = [jug.total_de_dados_en_juego() for jug in partida.jugadores]
    assert despues_r1 == [5, 4, 5]   # pierde J2 (dudó incorrectamente frente a 3×5)

    # ---------- RONDA 2 (empieza quien defina tu árbitro; no tocamos nada) ----------
    # Secuencia: APUESTO(2×3) -> DUDO
    # Elegimos manos para que el DUDO sea CORRECTO (total efectivos de 3 < 2),
    # de modo que pierda un dado el apostador previo.
    manos_r2 = [
        [1, 3, 4, 5, 6],
        [2, 4, 5, 6],
        [2, 4, 6, 5, 2],
    ]
    for j, mano in zip(partida.jugadores, manos_r2):
        _set_mano_respetando_cantidad(j, mano)

    proveedor_r2 = ProveedorScripted([
        (OpcionesJuego.APUESTO, (2, 3)),
        (OpcionesJuego.DUDO, None),
    ])

    partida.jugar_ronda(proveedor_r2)

    despues_r2 = [jug.total_de_dados_en_juego() for jug in partida.jugadores]
    assert despues_r2 == [4, 4, 5]

def test_tres_rondas_dos_jugadores(monkeypatch):
    """Test de 3 rondas diferentes"""
    monkeypatch.setattr(
        GestorPartida,
        "_elegir_primer_jugador",
        lambda self, n: setattr(self, "primer_jugador", 0),
    )

    partida = GestorPartida(2)
    partida.generar_arbitro(Rotacion.HORARIO)

    # ---------- RONDA 1 (tu Caso B) ----------
    manos_r1 = [
        [1, 1, 2, 3, 4],  # J0
        [1, 2, 3, 4, 5],  # J1
    ]
    for j, mano in zip(partida.jugadores, manos_r1):
        _set_mano_respetando_cantidad(j, mano)

    proveedor_r1 = ProveedorScripted([
        (OpcionesJuego.APUESTO, (1, 2)),
        (OpcionesJuego.CALZO, None),
    ])
    partida.jugar_ronda(proveedor_r1)
    assert [j.total_de_dados_en_juego() for j in partida.jugadores] == [5, 4]  # pierde J1

    # ---------- RONDA 2 ----------
    # Secuencia: APUESTO(2×6) -> DUDO, diseñamos manos para que el DUDO sea CORRECTO (efectivos de 6 < 2),
    # y así pierda quien apostó (el previo).
    manos_r2 = [
        [2, 3, 4, 5, 1],  # J0: 1 as, 0 seises  => 1 efectivo
        [2, 3, 4, 5],     # J1 (4 dados): 0 ases, 0 seises => 0 efectivos
    ]
    for j, mano in zip(partida.jugadores, manos_r2):
        _set_mano_respetando_cantidad(j, mano)

    proveedor_r2 = ProveedorScripted([
        (OpcionesJuego.APUESTO, (2, 6)),
        (OpcionesJuego.DUDO, None),
    ])
    partida.jugar_ronda(proveedor_r2)
    assert [j.total_de_dados_en_juego() for j in partida.jugadores] == [5, 3]  # vuelve a perder J1

    # ---------- RONDA 3 ----------
    # Secuencia: APUESTO(2×2) -> DUDO, ahora hacemos el DUDO INCORRECTO (efectivos de 2 >= 2) para que
    # pierda quien dudó.
    manos_r3 = [
        [2, 1, 4, 5, 6],
        [2, 3, 4],
    ]
    for j, mano in zip(partida.jugadores, manos_r3):
        _set_mano_respetando_cantidad(j, mano)

    proveedor_r3 = ProveedorScripted([
        (OpcionesJuego.APUESTO, (2, 2)),
        (OpcionesJuego.DUDO, None),
    ])
    partida.jugar_ronda(proveedor_r3)
    assert [j.total_de_dados_en_juego() for j in partida.jugadores] == [4, 3]


def test_eliminar_jugador_sin_dados():
    partida = GestorPartida(3)

    # Forzamos un jugador sin dados
    jugador_a_eliminar = partida.jugadores[0]
    for _ in range(5):
        jugador_a_eliminar.perder_dado()  # se queda sin dados

    # Ejecutamos limpieza
    partida._eliminar_jugadores_sin_dados()

    # Debe haber solo 2 jugadores ahora
    assert len(partida.jugadores) == 2
    assert jugador_a_eliminar not in partida.jugadores
@pytest.mark.parametrize(
    "cantidad_jugadores, jugadores_sin_dados, decision_final, esperado",
    [
        # Si al terminar la ronda queda 1 jugador, True (partida ganada)
        (2, [0], OpcionesJuego.DUDO, True),
        (3, [1, 2], OpcionesJuego.CALZO, True),

        # Si quedan >1 jugadores al terminar la ronda, False (partida no terminada)
        (3, [1], OpcionesJuego.DUDO, False),
        (6, [5], OpcionesJuego.CALZO, False),

        # Caso extremo: quedan 1 vs muchos eliminados -> True
        (6, [0,1,2,3,4], OpcionesJuego.DUDO, True),
    ],
    ids=[
        "2jug-1eliminado-termina",
        "3jug-2eliminados-termina",
        "3jug-1eliminado-no_termina",
        "6jug-1eliminado-no_termina",
        "6jug-5eliminados-termina"
    ]
)
def test_jugar_ronda_devuelve_true_si_partida_termina(cantidad_jugadores, jugadores_sin_dados,
                                                      decision_final, esperado, monkeypatch):
    """Test para verificar que juego devuelva si esta finalizada la partida o no"""
    partida = GestorPartida(cantidad_jugadores)

    partida.arbitro = ArbitroDummy()

    # Forzamos jugadores eliminados (sin dados)
    for j_id in jugadores_sin_dados:
        j = partida.jugadores[j_id]
        for _ in range(5):
            j.perder_dado()
    partida._eliminar_jugadores_sin_dados()

    proveedor = ProveedorScripted([
        (OpcionesJuego.APUESTO, (2, 5)),
        (decision_final, None),
    ])
    resultado = partida.jugar_ronda(proveedor)

    assert resultado == esperado
