import unittest

from codigo.login import realizar_login
from codigo.repositorio_usuario import RepositorioUsuario
from codigo.repositorio_monitorias import RepositorioMonitorias
from codigo.usuario_role_object import Usuario, Aluno, Professor, Monitor


class TestIntegracaoMonitoria(unittest.TestCase):
    def test_login_criacao_e_busca_de_monitoria(self):
        usuarios = RepositorioUsuario()
        monitorias = RepositorioMonitorias()

        aluno = Usuario(
            nome="Lorenzo",
            user="2669587",
            senha="1234",
            role_inicial=Aluno()
        )
        professor = Usuario(
            nome="Professor",
            user="professor",
            senha="5678",
            role_inicial=Professor(["Calculo"])
        )

        professor.get_role(Professor).atribuir_monitor(aluno, "Calculo")
        usuarios.salvar(aluno)

        usuario_logado = realizar_login(usuarios, "2669587", "1234")
        monitor = usuario_logado.get_role(Monitor)
        self.assertIsNotNone(monitor)

        monitor.criar_monitoria(
            materia="Calculo",
            dia="Quarta-feira",
            hora_inicio="14:00",
            hora_fim="15:00",
            Vagas=2
        )
        criada = monitor.get_monitorias()[-1]

        identificador = monitorias.salvar(criada)
        recuperada = monitorias.buscar(identificador)

        self.assertIs(recuperada, criada)
        self.assertIs(recuperada.monitor, monitor)
        self.assertEqual(recuperada.get_materia(), "Calculo")
        self.assertEqual(recuperada.get_dia(), "Quarta-feira")
        self.assertEqual(recuperada.get_hora_inicio(), "14:00")
        self.assertEqual(recuperada.get_hora_fim(), "15:00")
        self.assertEqual(len(recuperada.get_atendimentos()), 2)
        self.assertEqual(recuperada.get_atendimentos()[0].vagas, 2)