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

    def test_perfil_inexistente(self):
        usuarios = {
            "Lorenzo": {"role": "aluno"}
        }

        resultado = identificar_perfil(usuarios, "Neymar")
        self.assertIsNone(resultado, "aluno")

    def test_perfil_monitor(self):
        usuarios = {
            "Lorenzo": {"role": "monitor"}
        }
        resultado = identificar_perfil(usuarios, "Lorenzo")
        self.assertEqual(resultado, "monitor")

    def test_perfil_professor(self):
        usuarios = {
            "Lorenzo": {"role": "professor"}
        }
        resultado = identificar_perfil(usuarios, "Lorenzo")
        self.assertEqual(resultado, "professor")
    
    def test_sem_role(self):
        usuarios = {
            "Lorenzo": {"senha": "1234"}
        }

        with self.assertRaises(KeyError):
            identificar_perfil(usuarios, "Lorenzo")
