class RepositorioUsuario:
    def __init__(self):
        self.usuarios = {}

    def salvar(self, usuario):
        self.usuarios[usuario.get_user()] = usuario

    def buscar(self, login):
        return self.usuarios.get(login)
