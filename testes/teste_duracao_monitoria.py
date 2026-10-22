import unittest

from codigo.monitorias import Monitoria
from codigo.usuario_role_object import Monitor


class TestDuracaoMonitoria(unittest.TestCase):
    def test_rejeita_intervalo_maior_que_30(self):
        with self.assertRaisesRegex(ValueError, "30 minutos"):
            Monitoria(
                monitor=Monitor(["Calculo"]),
                materia="Calculo",
                dia="Quarta-feira",
                hora_inicio="14:00",
                hora_fim="14:45",
                Vagas=2
            )

    def test_intervalo_de_uma_hora_gera_dois_atendimentos(self):
        monitoria = Monitoria(
            monitor=Monitor(["Calculo"]),
            materia="Calculo",
            dia="Quarta-feira",
            hora_inicio="14:00",
            hora_fim="15:00",
            Vagas=2
        )

        horarios = [atendimento.hora for atendimento in monitoria.get_atendimentos()]
        self.assertEqual(horarios, ["14:00", "14:30"])