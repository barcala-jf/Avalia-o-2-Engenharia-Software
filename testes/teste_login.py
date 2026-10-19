import unittest
from codigo.login import autenticar

class TestLogin(unittest.TestCase):
    def test_credenciais_validas(self):
        usuarios = {
            "Lorenzo": {"senha": "1234"}
        }

        resultado = autenticar(usuarios, "Lorenzo", "1234")

        self.assertTrue(resultado)

    def test_senha_incorreta(self):
        usuarios = {
            "Lorenzo": {"senha": "1234"}
        }

        resultado = autenticar(usuarios, "Lorenzo", "123")
        self.assertFalse(resultado)

    def test_usuario_incorreto(self):
        usuarios = {
            "Lorenzo": {"senha": "1234"}
        }

        resultado = autenticar(usuarios, "joao", "1234")
        self.assertFalse(resultado)