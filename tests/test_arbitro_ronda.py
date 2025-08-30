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
    # Se simula un resultado de una mano y se le asocia a cada jugador para verificar respuesta correcta de manera determinista
    for j, mano in zip(jugadores, manos):
        j.cacho.agitar()
        _set_mano(monkeypatch, j, mano)

    arbitro = ArbitroRonda(0, jugadores)
    assert arbitro.definir_ganador(adivinanza) == 5

def test_arbitro_valida_apuesta(mocker):
    
    jugadores_prueba = [Jugador(), Jugador(), Jugador()]
    arbitro = ArbitroRonda(0, jugadores_prueba)
    
    
    mock_validador = mocker.Mock(spec = ValidadorApuesta)
    mock_validador.es_apuesta_valida.return_value = (True, "Apuesta valida")
    
    # Aquí simulamos la apuesta del jugador
    apuesta_simulada = (2, 5) # Dos quinas
    
    # Llamamos al método que vamos a crear en ArbitroRonda
    arbitro.procesar_jugada(OpcionesJuego.APUESTO, mock_validador, apuesta_simulada)

    # Verificamos que el método de validación fue llamado una vez
    mock_validador.es_apuesta_valida.assert_called_once()
    
    # Opcional pero recomendado: Verificamos que fue llamado con los argumentos correctos
    mock_validador.es_apuesta_valida.assert_called_once_with(
        apuesta_simulada, None, 15  
    )


def test_arbitro_cuando_jugador_hace_dudo_y_se_llama_a_definir_ganador(mocker):
    
    jugadores_prueba = [Jugador(), Jugador(), Jugador()]
    arbitro = ArbitroRonda(0, jugadores_prueba)
    
    # Mockeamos el método definir_ganador para poder verificar su llamada
    mock_definir_ganador = mocker.patch.object(arbitro, 'definir_ganador')
    
    # El árbitro necesita una apuesta anterior para poder dudar y procesar la jugada
    apuesta_anterior = (3, 4) 
    arbitro.apuesta_anterior = apuesta_anterior
    
    # Llamamos al método procesar_jugada con la opción DUDO
    arbitro.procesar_jugada(OpcionesJuego.DUDO, None, None)

    # Verificamos que el método definir_ganador fue llamado una vez
    mock_definir_ganador.assert_called_once()
    
    # Verificamos que fue llamado con la apuesta anterior
    mock_definir_ganador.assert_called_once_with(apuesta_anterior)

def test_arbitro_cuando_jugador_hace_calzo_y_la_apuesta_es_correcta(mocker):
    # Creamos un jugador con un cacho que tiene 4 cuatros
    jugador_con_dados_fijos = Jugador()
    jugador_con_dados_fijos.cacho._dados = [mocker.Mock(ultimo_resultado =4 ) for _ in range(4)]
    
    # El resto de los jugadores tienen cachos con dados que no son 4
    jugadores_prueba = [
        jugador_con_dados_fijos, 
        Jugador(), 
        Jugador()
    ]
    
    arbitro = ArbitroRonda(0, jugadores_prueba)
    
    # La apuesta anterior es de 4 cuatros
    apuesta_anterior = (4, 4)
    arbitro.apuesta_anterior = apuesta_anterior
    
    # Mockeamos el metodo definir_ganador para devolver el conteo real de dados
    mocker.patch.object(arbitro, 'definir_ganador', return_value=4)
    
    # Llamamos al método procesar_jugada con CALZO
    resultado_calzo = arbitro.procesar_jugada(OpcionesJuego.CALZO, None, None)

    # Verificamos que el resultado es True, porque el calzo fue exacto
    assert resultado_calzo is True