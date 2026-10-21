class RepositorioMonitorias:
    def __init__(self):
        self.monitorias = {}
        self.proximo_id = 1

    def salvar(self, monitoria):
        identificador = self.proximo_id
        self.monitorias[identificador] = monitoria
        self.proximo_id +=1
        return identificador

    def buscar(self, identificador):
        return self.monitorias.get(identificador)

    def excluir(self, identificador):
        self.monitorias.pop(identificador, None)