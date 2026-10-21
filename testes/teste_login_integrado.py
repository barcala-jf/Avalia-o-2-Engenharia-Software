import unittest

from codigo.login import realizar_login
from codigo.repositorio_usuario import RepositorioUsuario
from codigo.usuario_role_object import Usuario, Aluno


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