class Sessao():
    def __init__(self):
        self.usuario = None

    def iniciar_sessao(self, user):
        self.usuario = user
    
    def usuario_atual(self):
        return self.usuario