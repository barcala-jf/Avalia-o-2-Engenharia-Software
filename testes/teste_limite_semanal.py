import unittest
from datetime import date

from codigo.monitorias import Monitoria
from codigo.usuario_role_object import Monitor


class TestLimiteSemanal(unittest.TestCase):
    def test_monitoria_guarda_data(self):
        monitoria = Monitoria(
            monitor=Monitor(["Calculo"]),
            materia="Calculo",
            dia="Quarta-feira",
            hora_inicio="14:00",
            hora_fim="15:00",
            Vagas=2,
            data=date(2026, 10, 21)
        )

        self.assertEqual(monitoria.data, date(2026, 10, 21))