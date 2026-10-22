import unittest
from codigo.monitorias import Monitoria
from codigo.usuario_role_object import Monitor
from codigo.usuario_role_object import Usuario, Aluno, Monitor


class TestLimiteSemanal(unittest.TestCase):
    def test_terceira_reserva_na_mesma_disciplina_bloqueada(self):
        monitoria = Monitoria(
            monitor=Monitor(["Calculo"]),
            materia="Calculo",
            dia="Quarta-feira",
            hora_inicio="14:00",
            hora_fim="15:30",
            Vagas=2
        )
        aluno = Usuario("Lorenzo", "1", "1234", Aluno())
        papel = aluno.get_role(Aluno)
        atendimentos = monitoria.get_atendimentos()

        papel.marcar_monitoria(atendimentos[0])
        papel.marcar_monitoria(atendimentos[1])

        with self.assertRaisesRegex(ValueError, "Limite de reservas atingido"):
            papel.marcar_monitoria(atendimentos[2])

        self.assertEqual(len(papel.get_monitorias_marcadas()), 2)
        self.assertNotIn(aluno, atendimentos[2].alunos_cadastrados)
