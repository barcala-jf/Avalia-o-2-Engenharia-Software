import unittest

from codigo.login import realizar_login
from codigo.repositorio_usuario import RepositorioUsuario
from codigo.usuario_role_object import Usuario, Aluno, Professor, Monitor



class TestLoginIntegrado(unittest.TestCase):
    def test_login_valido_retorna_usuario_com_papel_aluno(self):
        repositorio = RepositorioUsuario()
        usuario = Usuario(
            nome="Lorenzo",
            user="2669587",
            senha="1234",
            role_inicial=Aluno()
        )
        repositorio.salvar(usuario)

        resultado = realizar_login(repositorio, "2669587", "1234")

        self.assertIs(resultado, usuario)
        self.assertTrue(resultado.have_role(Aluno))

    def test_login_com_senha_incorreta(self):
        repositorio = RepositorioUsuario()
        usuario = Usuario(
            nome="Lorenzo",
            user="2669587",
            senha="neymargoat",
            role_inicial=Aluno()
        )
        repositorio.salvar(usuario)

        with self.assertRaisesRegex(ValueError, "Credenciais inválidas"):
            realizar_login(repositorio, "2669587", "lionelmessigoat123")


    def test_login_com_usuario_inexistente(self):
        repositorio = RepositorioUsuario()

        with self.assertRaisesRegex(ValueError, "Credenciais inválidas"):
            realizar_login(repositorio, "barbeirosUtfpr", "67")

    def test_login_monitor_preserva_roles_e_disciplinas(self):
        repositorio = RepositorioUsuario()

        aluno = Usuario(
            nome="Lorenzo",
            user="2669587",
            senha="1234",
            role_inicial=Aluno()
        )
        professor = Usuario(
            nome="Luva de pedreiro",
            user="professor",
            senha="receba",
            role_inicial=Professor(["Calculo"])
        )

        professor.get_role(Professor).atribuir_monitor(aluno, "Calculo")
        repositorio.salvar(aluno)

        resultado = realizar_login(repositorio, "2669587", "1234")

        self.assertTrue(resultado.have_role(Aluno))
        self.assertTrue(resultado.have_role(Monitor))
        self.assertEqual(
            resultado.get_role(Monitor).get_disciplinas_monitorias(),
            ["Calculo"]
        ) 