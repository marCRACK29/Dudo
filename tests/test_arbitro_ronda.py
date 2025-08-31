import pytest

from src.juego.arbitro_ronda import ArbitroRonda, Rotacion, OpcionesJuego
from src.juego.jugador import Jugador
from src.juego.validador_apuesta import ValidadorApuesta

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


class FakeCacho:
    def __init__(self, mano):
        self._mano = list(mano)
    @property
    def resultados_numericos(self):
        return list(self._mano)

def _set_mano(monkeypatch, jugador: Jugador, mano: list[int]):
    """
    Sombrea la property `resultados_numericos` SOLO en la instancia jugador.cacho
    para no depender de `agitar()`. Permite manos distintas por jugador.
    """
    monkeypatch.setattr(jugador, "cacho", FakeCacho(mano))

#Para la estructura de la tupla es (cantidad_a_adivinar, tipo de dado adivinado)
@pytest.mark.parametrize(
    "manos, adivinanza, esperado",
    [
        # Apuesta normal: ases como comodines
        (
            [[3, 3, 2, 6, 1], [4, 1, 3, 2, 5]],  # total trenes efectivos: 5
            (4, 3),
            5
        ),
        # Apuesta a ases: no hay comodín (cuentan solo los 1)
        (
            [[1, 3, 1, 6, 2], [4, 1, 3, 2, 5]],  # total ases: 3
            (3, 1),
            3
        ),
        # Insuficiente: incluso contando comodines no alcanza
        (
            [[5, 2, 3, 6, 2], [4, 1, 3, 2, 5]],  # quinas reales 2 + ases 1 = 3
            (6, 5),
            3
        ),
        # Varios jugadores, mezcla de reales y ases
        (
            [[4, 4, 1, 2, 6], [2, 4, 3, 1, 1], [6, 6, 6, 2, 4]],  # cuatros efectivos: (2+1)+(1+2)+(1)=7
            (5, 4),
            7
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
    # Se simula un resultado de una mano y se le asocia a cada jugador para verificar respuesta correcta de manera determinista
    for j, mano in zip(jugadores, manos):
        j.cacho.agitar()
        _set_mano(monkeypatch, j, mano)

    arbitro = ArbitroRonda(0, jugadores)
    assert arbitro.definir_ganador(adivinanza) == esperado

def test_arbitro_valida_apuesta(mocker):
    jugadores_prueba = [Jugador(), Jugador(), Jugador()]
    arbitro = ArbitroRonda(0, jugadores_prueba)

    # Parcheamos ValidadorApuesta en el módulo donde ArbitroRonda lo usa
    mock_validador_cls = mocker.patch(
        "src.juego.arbitro_ronda.ValidadorApuesta"
    )
    # Creamos un mock para la instancia de esa clase
    mock_validador_inst = mock_validador_cls.return_value
    mock_validador_inst.es_apuesta_valida.return_value = (True, "Apuesta válida")

    # Apuesta simulada
    apuesta_simulada = (2, 5)  # Dos quinas

    # Ejecutamos el método
    arbitro.procesar_jugada(OpcionesJuego.APUESTO, apuesta_simulada)

    # Verificamos que es_apuesta_valida se llamó correctamente
    mock_validador_inst.es_apuesta_valida.assert_called_once_with(
        apuesta_simulada, None, 15
    )


def test_arbitro_cuando_jugador_hace_dudo_y_se_llama_a_definir_ganador(mocker):
    jugadores_prueba = [Jugador(), Jugador(), Jugador()]
    arbitro = ArbitroRonda(0, jugadores_prueba)
    
    mock_definir_ganador = mocker.patch.object(arbitro, 'definir_ganador', return_value=3)

    
    
    apuesta_anterior = (4, 4)
    arbitro.apuesta_anterior = apuesta_anterior
    
    # Aquí se corrige el problema. El método procesar_jugada recibe el jugador actual del arbitro.
    arbitro.procesar_jugada(OpcionesJuego.DUDO, None)

    mock_definir_ganador.assert_called_once()
    mock_definir_ganador.assert_called_once_with(apuesta_anterior)


@pytest.mark.parametrize(
    "dados_reales, apuesta_duda, pierde_actual",
    [
        (3, (4, 5), False), # Dudo correcto -> pierde el anterior
        (5, (4, 5), True) # Dudo incorrecto -> pierde el actual
    ]
)
def test_arbitro_aplica_regla_dudo_correctamente(dados_reales, apuesta_duda, pierde_actual, mocker):
    jugadores = [Jugador(), Jugador()]
    arbitro = ArbitroRonda(0, jugadores)
    
    arbitro.apuesta_anterior = apuesta_duda
    
    mocker.patch.object(arbitro, 'definir_ganador', return_value=dados_reales)
    
    jugador_actual = arbitro.jugadores[arbitro.jugador_actual_id]
    jugador_anterior = arbitro.jugadores[(arbitro.jugador_actual_id - arbitro.rotacion.value) % len(arbitro.jugadores)]
    
    mock_perder_actual = mocker.patch.object(jugador_actual, 'perder_dado')
    mock_perder_anterior = mocker.patch.object(jugador_anterior, 'perder_dado')

    arbitro.procesar_jugada(OpcionesJuego.DUDO, None)
    
    if pierde_actual:
        mock_perder_actual.assert_called_once()
        mock_perder_anterior.assert_not_called()
    else:
        mock_perder_anterior.assert_called_once()
        mock_perder_actual.assert_not_called()


   
@pytest.mark.parametrize(
    "dados_reales, apuesta_calzo, metodo_esperado",
    [
        # Escenario 1: Calzo correcto (hay 4 dados, se apostó 4)
        # El jugador que calzó gana un dado
        (4, (4, 5), 'ganar_dado'),
        
        # Escenario 2: Calzo incorrecto (hay 5 dados, se apostó 4)
        # El jugador que calzó pierde un dado
        (5, (4, 5), 'perder_dado')
    ]
)
def test_arbitro_aplica_regla_calzo_correctamente(
    dados_reales, apuesta_calzo, metodo_esperado, mocker
):
    # Creamos un árbitro con un jugador de prueba
    jugador_calzador = Jugador()
    arbitro = ArbitroRonda(0, [jugador_calzador])
    
    # Configuramos la apuesta anterior
    arbitro.apuesta_anterior = apuesta_calzo
    
    # Mockeamos el resultado real de los dados para que sea predecible
    mocker.patch.object(arbitro, 'definir_ganador', return_value=dados_reales)
    
    jugador_actual = arbitro.jugadores[arbitro.jugador_actual_id]
    
    
    mock_ganar_dado = mocker.patch.object(jugador_actual, 'ganar_dado')
    mock_perder_dado = mocker.patch.object(jugador_actual, 'perder_dado')

    arbitro.procesar_jugada(OpcionesJuego.CALZO, None)
    
   
    if metodo_esperado == 'ganar_dado':
        mock_ganar_dado.assert_called_once()
        mock_perder_dado.assert_not_called()
    else:
        mock_perder_dado.assert_called_once()
        mock_ganar_dado.assert_not_called()

def test_setear_jugador_prox_ronda():
    jugadores = [Jugador() for _ in range(4)] 
    arbitro = ArbitroRonda(0, jugadores) # comenzamos con el primer jugador de la lista

    jugador_objetivo = jugadores[2] #tomamos el tercero y comenzamos la siguiente ronda desde aquí 
    arbitro._setear_inicio_ronda(jugador_objetivo)

    assert arbitro.jugador_actual_id == 2
