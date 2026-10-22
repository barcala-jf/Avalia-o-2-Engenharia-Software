import unittest
from unittest.mock import patch

from codigo.login import realizar_login
from codigo.repositorio_usuario import RepositorioUsuario
from codigo.sessao import Sessao
from codigo.usuario_role_object import Usuario, Aluno, Professor, Monitor


class TestIntegracaoPermissoes(unittest.TestCase):
    def test_promocao_persistida_apos_novo_login(self):
        repositorio = RepositorioUsuario()
        sessao = Sessao()

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
        repositorio.salvar(aluno)
        repositorio.salvar(professor)

        usuario_logado = realizar_login(repositorio, "2669587", "1234")
        sessao.iniciar_sessao(usuario_logado)
        self.assertFalse(usuario_logado.have_role(Monitor))

        professor_logado = realizar_login(repositorio, "professor", "5678")

        with patch.object(
            repositorio, "salvar", wraps=repositorio.salvar
        ) as salvar:
            professor_logado.get_role(Professor).atribuir_monitor(
                usuario_logado, "Calculo", repositorio
            )
            salvar.assert_called_once_with(usuario_logado)

        sessao.encerrar_sessao()
        self.assertIsNone(sessao.usuario_atual())

        novo_login = realizar_login(repositorio, "2669587", "1234")
        sessao.iniciar_sessao(novo_login)

        self.assertTrue(novo_login.have_role(Aluno))
        self.assertTrue(novo_login.have_role(Monitor))
        self.assertEqual(
            novo_login.get_role(Monitor).get_disciplinas_monitorias(),
            ["Calculo"]
        )