class Sessao():
    def __init__(self):
        self.usuario = None

    def iniciar_sessao(self, user):
        self.usuario = user

    def encerrar_sessao(self):
        self.usuario = None
    
    def usuario_atual(self):
        return self.usuario