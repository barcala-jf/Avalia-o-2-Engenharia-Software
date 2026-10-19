import unittest
from codigo.login import autenticar

class TestLogin(unittest.TestCase):
    def test_credenciais_validas(self):
        usuarios = {
            "Lorenzo": {"senha": "1234"}
        }

        resultado = autenticar(usuarios, "Lorenzo", "1234")

        self.assertTrue(resultado)