import unittest
from codigo.role import identificar_perfil

class TestRole(unittest.TestCase):
    def test_identifica_perfil(self):
        usuarios = {
            "Lorenzo": {"role": "aluno"},
            "Joao": {"role": "monitor"},
            "Luiz": {"role": "professor"}
        }

        resultado = identificar_perfil(usuarios, "Lorenzo")
        self.assertEqual(resultado, "aluno")