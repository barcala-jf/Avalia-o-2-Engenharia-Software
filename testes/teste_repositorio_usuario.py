import unittest

from codigo.repositorio_usuario import RepositorioUsuario
from codigo.usuario_role_object import Usuario, Aluno

class TestRepositorio(unittest.TestCase):
    def test_salvar_e_buscar_usuario(self):
        repositorio = RepositorioUsuario()
        usuario = Usuario(nome="Lorenzo", user="2669587", senha="1234")
        repositorio.salvar(usuario)
        resultado = repositorio.buscar("2669587")
        self.assertIs(resultado, usuario)
        