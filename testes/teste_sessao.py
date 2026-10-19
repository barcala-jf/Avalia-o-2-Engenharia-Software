import unittest
from codigo.sessao import Sessao

class TestSessao(unittest.TestCase):
    def test_iniciar_sessao(self):
        sessao = Sessao()
        sessao.iniciar_sessao("Lorenzo")
        self.assertEqual(sessao.usuario_atual(), "Lorenzo")

    def test_sessao_vazia(self):
        sessao = Sessao()
        self.assertIsNone(sessao.usuario_atual())
