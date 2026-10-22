import unittest

from codigo.monitorias import Monitoria
from codigo.usuario_role_object import Usuario, Aluno, Monitor


class TestReservas(unittest.TestCase):
    def test_reserva_lotada_nao_entra_na_agenda_do_aluno(self):
        monitor = Monitor(["Calculo"])
        monitoria = Monitoria(
            monitor=monitor,
            materia="Calculo",
            dia="Quarta-feira",
            hora_inicio="14:00",
            hora_fim="15:00",
            Vagas=1
        )
        atendimento = monitoria.get_atendimentos()[0]

        aluno1 = Usuario("Lorenzo", "1", "1234", Aluno())
        aluno2 = Usuario("Joao", "2", "1234", Aluno())

        aluno1.get_role(Aluno).marcar_monitoria(atendimento)

        with self.assertRaisesRegex(ValueError, "Horário Lotado"):
            aluno2.get_role(Aluno).marcar_monitoria(atendimento)

        self.assertNotIn(
            atendimento,
            aluno2.get_role(Aluno).get_monitorias_marcadas()
        )
        self.assertNotIn(aluno2, atendimento.alunos_cadastrados)
        self.assertIn(aluno1, atendimento.alunos_cadastrados)