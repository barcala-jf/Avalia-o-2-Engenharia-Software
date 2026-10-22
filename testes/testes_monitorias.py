import unittest
from codigo.monitorias import Monitoria
from codigo.usuario_role_object import Aluno, Monitor, Professor, Usuario
from datetime import date
from codigo.repositorio_monitorias import RepositorioMonitorias

class TestMonitorias(unittest.TestCase):

    def setUp(self) -> None:
        """ Cria ambiente de testes """
        monitor1 = Monitor(["Teste1"])
        self.monitoria1 = Monitoria(monitor1,"Teste1", "Quarta-feira", "14:00", "15:00", 1, date(2026,10,21))
        self.monitoria2 = Monitoria(monitor1,"Teste1", "Sexta-feira", "16:00", "18:00", 2, date(2026,10,23))

    def teste_atendimentos_monitoria(self) -> None:
        """ Testa se os atendimentos são gerados corretamente para cada monitoria """
        self.assertEqual(len(self.monitoria1.get_atendimentos()), 2)
        self.assertEqual(len(self.monitoria2.get_atendimentos()), 4)

        self.assertEqual(self.monitoria2.get_atendimentos()[0].hora, "16:00")
        self.assertEqual(self.monitoria2.get_atendimentos()[1].hora, "16:30")
        self.assertEqual(self.monitoria2.get_atendimentos()[2].hora, "17:00")
        self.assertEqual(self.monitoria2.get_atendimentos()[3].hora, "17:30")

    def teste_cancelamento_monitoria(self) -> None:
        """ Testa se o cancelamento de uma monitoria funciona corretamente """
        self.monitoria1.cancelar_monitoria()
        self.assertTrue(self.monitoria1.cancelado)
        for atendimento in self.monitoria1.get_atendimentos():
            self.assertTrue(atendimento.cancelado)

    def teste_cancelamento_atendimento(self) -> None:
        """ Testa se o cancelamento de um atendimento funciona corretamente """
        atendimento = self.monitoria2.get_atendimentos()[0]
        self.monitoria2.cancelar_atendimento(atendimento)
        self.assertTrue(atendimento.cancelado)

    def teste_registrar_aluno_em_monitoria(self) -> None:
        """ Testa se o registro de um aluno em uma monitoria funciona corretamente """
        atendimento = self.monitoria2.get_atendimentos()[0]
        sucesso = atendimento.marcar("Aluno1")
        self.assertTrue(sucesso)
    
    def teste_registrar_cancelamento_aluno(self) -> None:
        """ Testa se o registro de cancelamento de um aluno funciona corretamente """
        self.monitoria1.get_atendimentos()[0].marcar("Aluno1")
        sucesso = self.monitoria1.get_atendimentos()[0].desmarcar("Aluno1")
        self.assertTrue(sucesso)
        self.assertIn("Aluno1", self.monitoria1.alunos_cancelados)
        self.assertNotIn("Aluno1", self.monitoria1.get_atendimentos()[0].alunos_cadastrados)

    def teste_segundo_aluno_nao_reserva_atendimento_lotado(self) -> None:
        """ Testa se dois alunos podem marcar o mesmo atendimento ao mesmo tempo """
        atendimento = self.monitoria1.get_atendimentos()[0]
        sucesso1 = atendimento.marcar("Aluno1")
        sucesso2 = atendimento.marcar("Aluno2")
        self.assertTrue(sucesso1)
        self.assertFalse(sucesso2)
        self.assertIn("Aluno1", atendimento.alunos_cadastrados)
        self.assertNotIn("Aluno2", atendimento.alunos_cadastrados)

class TesteMonitoriasAlunos(unittest.TestCase):

    def setUp(self) -> None:
        """ Cria ambiente de testes """
        self.aluno_test = Usuario(
            nome = 'teste',
            user= '5555',
            senha='777',
            role_inicial=Aluno(['Teste1', 'Teste2']),

        )

        self.aluno_test2 = Usuario(
            nome = 'teste2',
            user= '5556',
            senha='777',
            role_inicial=Aluno(['Teste1', 'Teste2']),
        )

        self.professor_test1 = Usuario(
            nome='teste_professor',
            user='professor.teste',
            senha='777',
            role_inicial=Professor(['Teste1'])
        )

    def test_adicionar_monitoria(self) -> None:
        """" Um aluno deve ser capaz de criar uma monitor para uma matéria que ele seja monitor"""
        role_professor = self.professor_test1.get_role(Professor)
        if role_professor is not None:
            role_professor.atribuir_monitor(self.aluno_test2, 'Teste1')
            self.assertTrue(self.aluno_test2.have_role(Monitor))

        role_monitor = self.aluno_test2.get_role(Monitor) 
        role_monitor.criar_monitoria("Teste1", "Quarta-feira", "14:00", "15:00", 1,data=date(2026, 10, 21))

        self.assertIsNotNone(role_monitor.get_monitorias())

    def teste_monitor_cria_monitoria_para_materia_que_nao_e_monitor(self) -> None:
        """ Um aluno não deve ser capaz de criar uma monitoria para uma matéria que ele não seja monitor"""
        role_professor = self.professor_test1.get_role(Professor)
        if role_professor is not None:
            role_professor.atribuir_monitor(self.aluno_test2, 'Teste1')
            self.assertTrue(self.aluno_test2.have_role(Monitor))

        role_monitor = self.aluno_test2.get_role(Monitor) 
        with self.assertRaises(PermissionError):
            role_monitor.criar_monitoria("Teste3", "Quarta-feira", "14:00", "15:00", 1,data=date(2026, 10, 21))

    def teste_monitor_cancelar_monitoria(self) -> None:
        """ Um monitor deve ser capaz de cancelar uma monitoria que ele tenha criado """
        role_professor = self.professor_test1.get_role(Professor)
        if role_professor is not None:
            role_professor.atribuir_monitor(self.aluno_test2, 'Teste1')
            self.assertTrue(self.aluno_test2.have_role(Monitor))

        role_monitor = self.aluno_test2.get_role(Monitor) 
        role_monitor.criar_monitoria("Teste1", "Quarta-feira", "14:00", "15:00", 1,data=date(2026, 10, 21))
        monitorias = role_monitor.get_monitorias()
        self.assertIsNotNone(monitorias)

        # Cancelar a monitoria
        monitoria_para_cancelar = monitorias[0]
        role_monitor.cancelar_monitoria(monitoria_para_cancelar)
        monitorias_canceladas = role_monitor.get_monitorias_canceladas()
        self.assertIn(monitoria_para_cancelar, monitorias_canceladas)

    def teste_monitor_cancelar_monitoria_que_nao_existe(self) -> None:
        """ Um monitor não deve ser capaz de cancelar uma monitoria que ele não tenha criado """
        role_professor = self.professor_test1.get_role(Professor)
        if role_professor is not None:
            role_professor.atribuir_monitor(self.aluno_test2, 'Teste1')
            self.assertTrue(self.aluno_test2.have_role(Monitor))

        role_monitor = self.aluno_test2.get_role(Monitor) 
        with self.assertRaises(ValueError):
            role_monitor.cancelar_monitoria("Monitoria Inexistente")

        """ Um aluno deve ser capaz de ver as monitorias da matéria que ele participa"""

    def teste_aluno_ver_monitorias(self) -> None:
        repositorio = RepositorioMonitorias()

        professor = self.professor_test1.get_role(Professor)
        professor.atribuir_monitor(self.aluno_test2, "Teste1")

        monitor = self.aluno_test2.get_role(Monitor)
        monitor.criar_monitoria("Teste1", "Quarta-feira", "14:00", "15:00", 1,data=date(2026, 10, 21))
        repositorio.salvar(monitor.get_monitorias()[0])

        aluno = self.aluno_test.get_role(Aluno)
        resultado = aluno.list_monitorias(repositorio)

        esperado = [
            {
                "materia": "Teste1",
                "monitor": "teste2",
                "data": date(2026, 10, 21),
                "dia": "Quarta-feira",
                "hora": hora,
                "vagas_disponiveis": 1
            }
            for hora in ["14:00", "14:30"]
        ]

        self.assertEqual(resultado, esperado)

    def teste_aluno_marcar_monitoria(self) -> None:
        """ Um aluno deve ser capaz de marcar uma monitoria que ele queira participar """
        role_professor = self.professor_test1.get_role(Professor)
        if role_professor is not None:
            role_professor.atribuir_monitor(self.aluno_test2, 'Teste1')
            self.assertTrue(self.aluno_test2.have_role(Monitor))

        role_monitor = self.aluno_test2.get_role(Monitor)
        role_monitor.criar_monitoria("Teste1", "Quarta-feira", "14:00", "15:00", 1,data=date(2026, 10, 21))
        monitorias = role_monitor.get_monitorias()
        self.assertIsNotNone(monitorias)

        # Aluno marca a monitoria
        role_aluno = self.aluno_test.get_role(Aluno)
        monitoria_para_marcar = monitorias[0].get_atendimentos()[0]
        role_aluno.marcar_monitoria(monitoria_para_marcar)
        monitorias_marcadas = role_aluno.get_monitorias_marcadas()
        self.assertIn(monitoria_para_marcar, monitorias_marcadas)

    def teste_aluno_cancelar_monitoria(self) -> None:
        """ Um aluno deve ser capaz de cancelar uma monitoria que ele tenha marcado """
        role_professor = self.professor_test1.get_role(Professor)
        if role_professor is not None:
            role_professor.atribuir_monitor(self.aluno_test2, 'Teste1')
            self.assertTrue(self.aluno_test2.have_role(Monitor))

        role_monitor = self.aluno_test2.get_role(Monitor)
        role_monitor.criar_monitoria("Teste1", "Quarta-feira", "14:00", "15:00", 1,data=date(2026, 10, 21))
        monitorias = role_monitor.get_monitorias()
        self.assertIsNotNone(monitorias)

        # Aluno marca a monitoria
        role_aluno = self.aluno_test.get_role(Aluno)
        monitoria_para_marcar = monitorias[0].get_atendimentos()[0]
        role_aluno.marcar_monitoria(monitoria_para_marcar)
        monitorias_marcadas = role_aluno.get_monitorias_marcadas()
        self.assertIn(monitoria_para_marcar, monitorias_marcadas)

        # Aluno cancela a monitoria
        role_aluno.cancelar_monitoria(monitoria_para_marcar)
        monitorias_marcadas = role_aluno.get_monitorias_marcadas()
        self.assertNotIn(monitoria_para_marcar, monitorias_marcadas)

if __name__ == '__main__':
    unittest.main()