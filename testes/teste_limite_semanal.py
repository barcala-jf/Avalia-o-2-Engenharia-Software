import unittest
from datetime import date

from codigo.monitorias import Monitoria
from codigo.usuario_role_object import Monitor
from codigo.usuario_role_object import Usuario, Aluno, Monitor


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

    def test_terceira_reserva_na_mesma_semana_e_disciplina_bloqueada(self):
        monitoria = Monitoria(
            monitor=Monitor(["Calculo"]),
            materia="Calculo",
            dia="Quarta-feira",
            hora_inicio="14:00",
            hora_fim="15:30",
            Vagas=2,
            data=date(2026, 10, 21)
        )
        aluno = Usuario("Lorenzo", "1", "1234", Aluno())
        papel = aluno.get_role(Aluno)
        atendimentos = monitoria.get_atendimentos()

        papel.marcar_monitoria(atendimentos[0])
        papel.marcar_monitoria(atendimentos[1])

        with self.assertRaisesRegex(ValueError, "Limite semanal"):
            papel.marcar_monitoria(atendimentos[2])

        self.assertEqual(len(papel.get_monitorias_marcadas()), 2)
        self.assertNotIn(aluno, atendimentos[2].alunos_cadastrados)

    def test_permite_reserva_em_outra_semana(self):
        monitor = Monitor(["Calculo"])
        aluno = Usuario("Lorenzo", "1", "1234", Aluno())
        papel = aluno.get_role(Aluno)

        semana1 = Monitoria(
            monitor=monitor,
            materia="Calculo",
            dia="Quarta-feira",
            hora_inicio="14:00",
            hora_fim="15:00",
            Vagas=2,
            data=date(2026, 10, 21)
        )
        semana2 = Monitoria(
            monitor=monitor,
            materia="Calculo",
            dia="Quarta-feira",
            hora_inicio="14:00",
            hora_fim="14:30",
            Vagas=2,
            data=date(2026, 10, 28)
        )

        for atendimento in semana1.get_atendimentos():
            papel.marcar_monitoria(atendimento)

        novo_atendimento = semana2.get_atendimentos()[0]
        papel.marcar_monitoria(novo_atendimento)

        self.assertEqual(len(papel.get_monitorias_marcadas()), 3)
        self.assertIn(aluno, novo_atendimento.alunos_cadastrados)