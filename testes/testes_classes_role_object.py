import unittest
from codigo.usuario_role_object import(
    Usuario,
    RoleUsuario,
    Aluno,
    Monitor,
    Professor
)

class TestRoleObject(unittest.TestCase):

    def setUp(self) -> None:
        ''' Cria ambiente de testes'''
        self.aluno_test = Usuario(
            nome = 'teste',
            user= '5555',
            senha= '777',
            role_inicial=Aluno(['Teste1', 'Teste2']),
        )

        self.professor_test1 = Usuario(
            nome='teste_professor',
            user='professor.teste',
            senha='777',
            role_inicial=Professor(['Teste1'])
        )

        self.professor_test2 = Usuario(
            nome='teste_professor2',
            user='professor2.teste',
            senha='777',
            role_inicial=Professor(['Teste2'])
        )

        self.professor_test3 = Usuario(
            nome='teste_professor3',
            user='professor3.test',
            senha='777',
            role_inicial=Professor(['Teste1', 'Teste2'])
        )

    def test_roles_concreta_herda_role_usuario(self) -> None:
        ''' Garante herança da role concreta com base na classe base Usuario'''
        roles = (
            Aluno(['Teste1']),
            Monitor(['Teste1']),
            Professor(['Teste1'])
        )

        for role in roles:
            with self.subTest(role=type(role).__name__):
                self.assertIsInstance(role, RoleUsuario)


    def test_usuario_inicia_role_definida(self) -> None:
        ''' Aluno e professor devem nascer com suas respectivas roles, nunca deve nascer um monitor'''
        # Aluno deve ser Aluno
        self.assertTrue(self.aluno_test.have_role(Aluno))
        # Aluno não deve ser Professor
        self.assertFalse(self.aluno_test.have_role(Professor))
        # Aluno não deve ser Monitor
        self.assertFalse(self.aluno_test.have_role(Monitor))

        self.assertTrue(self.professor_test1.have_role(Professor))
        self.assertFalse(self.professor_test1.have_role(Aluno))

    def test_referencia_bidirecional_entre_usuario_e_role(self) -> None:
        """A role deve apontar para a instância correta de Usuario."""
        role_aluno = self.aluno_test.get_role(Aluno)
        self.assertIsNotNone(role_aluno)
        self.assertIs(role_aluno.usuario, self.aluno_test)
        self.assertEqual(role_aluno.get_materias(), ["Teste1", "Teste2"])

    def test_professor_atribui_monitoria1_aluno(self) -> None:
        """ O professor deve atribuir corretamente a primeira monitoria a um aluno tornando ele monitor"""
        role_prof = self.professor_test1.get_role(Professor)
        role_prof.atribuir_monitor(self.aluno_test, 'Teste1')

        # O aluno agora deve ter a role Monitor
        self.assertTrue(self.aluno_test.have_role(Monitor))
        # O aluno deve continuar sendo aluno
        self.assertTrue(self.aluno_test.have_role(Aluno))

        role_monitor = self.aluno_test.get_role(Monitor)
        # Deve adicionar a disciplina na lista de disciplinas monitoradas
        self.assertEqual(role_monitor.get_disciplinas_monitorias(), ['Teste1'])

    def test_professor_atribui_monitoria2_aluno(self) -> None:
        ''' O professor deve atribuir corretamente a segunda disciplina monitorada por um aluno que já é monitor'''
        role_prof1 = self.professor_test1.get_role(Professor)
        role_prof2 = self.professor_test2.get_role(Professor)
        
        
        role_prof1.atribuir_monitor(self.aluno_test, 'Teste1')
        role_prof2.atribuir_monitor(self.aluno_test, 'Teste2')

        role_monitor = self.aluno_test.get_role(Monitor)
        self.assertEqual(
            role_monitor.get_disciplinas_monitorias(),
            ['Teste1', 'Teste2'],
        )

    def test_retirar_uma_monitoria_mantem_role_monitor_se_sobrar_disciplina(self) -> None:
        """ Ao tirar a monitoria de algum aluno deve se verificar se o professor ministra tal disciplina e somente retirar a
            Role de monitor se for a última disciplina que ele dá monitoria """

        role_prof1 = self.professor_test1.get_role(Professor)
        role_prof2 = self.professor_test2.get_role(Professor)

        role_prof1.atribuir_monitor(self.aluno_test, 'Teste1')
        role_prof2.atribuir_monitor(self.aluno_test, 'Teste2')

        # Retira a primeira disciplina monitorada
        role_prof1.retirar_monitoria(self.aluno_test, 'Teste1')

        # Deve continuar sendo monitor da primeira monitoria
        self.assertTrue(self.aluno_test.have_role(Monitor))
        role_monitor = self.aluno_test.get_role(Monitor)
        self.assertEqual(role_monitor.get_disciplinas_monitorias(), ['Teste2'])

        # Retira a segunda disciplina monitorada
        role_prof2.retirar_monitoria(self.aluno_test, 'Teste2')

        # Não deve mais ser monitor
        self.assertFalse(self.aluno_test.have_role(Monitor))

    def test_erro_atribuir_disciplina_nao_lecionada(self) -> None:
        """Um professor não pode transformar um aluno em um monitor de uma disciplina que não é sua"""
        role_prof1 = self.professor_test1.get_role(Professor)

        with self.assertRaises(PermissionError):
            role_prof1.atribuir_monitor(self.aluno_test, 'Teste2')

    def test_erro_atribuir_disciplina_outro_professor(self) -> None:
        role_prof1 = self.professor_test1.get_role(Professor)

        with self.assertRaises(PermissionError):
            role_prof1.atribuir_monitor(self.professor_test2, 'Teste1')

    def test_erro_retirar_disciplina_nao_lecionada(self) -> None:
        role_prof1 = self.professor_test1.get_role(Professor)
        role_prof2 = self.professor_test2.get_role(Professor)

        role_prof1.atribuir_monitor(self.aluno_test, 'Teste1')
        role_prof2.atribuir_monitor(self.aluno_test, 'Teste2')

        with self.assertRaises(PermissionError):
            role_prof1.retirar_monitoria(self.aluno_test, 'Teste2')

    def test_erro_retirar_disciplina_nao_monitor_e_nao_monitora(self) -> None:
        ''' Um professor não pode retirar monitoria de um aluno que não é monitor e nem retirar uma monitoria de um monitor
            que não a monitora, mesmo que esse professor lecione essa disciplina'''
        role_prof3 = self.professor_test3.get_role(Professor)

        # Tenta tirar a disciplina de monitoria de um aluno que não é monitor
        with self.assertRaises(ValueError):
            role_prof3.retirar_monitoria(self.aluno_test, 'Teste1')

        role_prof3.atribuir_monitor(self.aluno_test, 'Teste1')

        # Tenta tirar uma disciplina que o monitor não monitora mesmo que esse professor a lecione
        with self.assertRaises(ValueError):
            role_prof3.retirar_monitoria(self.aluno_test, 'Teste2')

if __name__ == '__main__':
    unittest.main()