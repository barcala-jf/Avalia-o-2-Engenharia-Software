import unittest

from codigo.monitorias import Monitoria
from codigo.usuario_role_object import Usuario, Aluno, Monitor


class TestCancelamentoReserva(unittest.TestCase):
    def test_cancelamento_libera_vaga_para_outro_aluno(self):
        monitoria = Monitoria(
            monitor=Monitor(["Calculo"]),
            materia="Calculo",
            dia="Quarta-feira",
            hora_inicio="14:00",
            hora_fim="15:00",
            Vagas=1
        )
        atendimento = monitoria.get_atendimentos()[0]

        aluno1 = Usuario("Lorenzo", "1", "1234", Aluno())
        aluno2 = Usuario("Joao", "2", "1234", Aluno())

        papel1 = aluno1.get_role(Aluno)
        papel1.marcar_monitoria(atendimento)
        papel1.cancelar_monitoria(atendimento)

        self.assertNotIn(atendimento, papel1.get_monitorias_marcadas())
        self.assertNotIn(aluno1, atendimento.alunos_cadastrados)
        self.assertFalse(atendimento.lotado)

        aluno2.get_role(Aluno).marcar_monitoria(atendimento)

        self.assertIn(aluno2, atendimento.alunos_cadastrados)
        self.assertIn(atendimento,aluno2.get_role(Aluno).get_monitorias_marcadas())