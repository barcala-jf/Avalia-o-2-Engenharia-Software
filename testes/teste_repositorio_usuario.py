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

    def test_buscar_usuario_inexistente(self):
        repositorio = RepositorioUsuario()
        resultado = repositorio.buscar("123456")
        self.assertIsNone(resultado)
        
    def test_atualizar_usuario(self):
        repositorio = RepositorioUsuario()
        usuario = Usuario(nome="Lorenzo", user="2669587", senha="1234")
        repositorio.salvar(usuario)
        usuario_atualizado = Usuario(nome="Lorenzo Brugnolo", user="2669587", senha="nova")
        repositorio.atualizar(usuario_atualizado)
        resultado = repositorio.buscar("2669587")
        self.assertIs(resultado, usuario_atualizado)
