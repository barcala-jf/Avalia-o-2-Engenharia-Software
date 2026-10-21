import threading
from datetime import datetime, timedelta

class Atendimento:
    def __init__(self, hora: str, vagas: int, monitoria: 'Monitoria') -> None:
        self.hora = datetime.strptime(hora, "%H:%M").strftime("%H:%M")
        self.monitoria = monitoria

        self.vagas = vagas
        self.cancelado = False
        self.lotado = False
        self.alunos_cadastrados = []
        
        self.lock = threading.Lock() # Mutex para controlar o acesso a recursos compartilhados

    def cancelar(self):
        self.cancelado = True

    def marcar(self, aluno: str) -> bool:
        with self.lock: # Blqueia o acesso a recursos compartilhados para evitar condições de corrida
            if not self.cancelado and len(self.alunos_cadastrados) < self.vagas:
                self.alunos_cadastrados.append(aluno)
                if len(self.alunos_cadastrados) == self.vagas:
                    self.lotado = True
                return True
            return False

    def desmarcar(self, aluno: str) -> bool:
        with self.lock: # Blqueia o acesso a recursos compartilhados para evitar condições de corrida
            if aluno in self.alunos_cadastrados:
                self.alunos_cadastrados.remove(aluno)
                self.monitoria.registrar_cancelamento(aluno) 
                return True
            return False

class Monitoria:
    def __init__(self, materia: str, dia: str, hora_inicio: str , hora_fim: str, Vagas: int) -> None:

        i, f = datetime.strptime(hora_inicio, "%H:%M"), datetime.strptime(hora_fim, "%H:%M")
        self.hora_inicio = i.strftime("%H:%M")
        self.hora_fim = f.strftime("%H:%M")

        self.atendimentos = []
        for hora in self._gerar_horarios(i, f):
            self.atendimentos.append(Atendimento(hora, Vagas, self))

        self.materia = materia
        self.dia = dia

        self.alunos_cadastrados = []
        self.alunos_cancelados = []
        self.cancelado = False

    def _gerar_horarios(self, hora_inicio: datetime, hora_fim: datetime) -> list[str]:
        horarios = []
        hora_atual = hora_inicio
        while hora_atual < hora_fim:
            horarios.append(hora_atual.strftime("%H:%M"))
            hora_atual += timedelta(minutes=30)
        return horarios

    def cancelar_atendimento(self, atendimento: Atendimento) -> None:
        atendimento.cancelar()

    def cancelar_monitoria(self) -> None:
        for atendimento in self.atendimentos:
            atendimento.cancelar()

        self.cancelado = True

    def registrar_cancelamento(self, aluno: str) -> None:
        self.alunos_cancelados.append(aluno)

    def get_atendimentos(self) -> list[Atendimento]:
        return self.atendimentos

    def get_materia(self) -> str:
        return self.materia

    def get_dia(self) -> str:
        return self.dia

    def get_alunos_cadastrados(self) -> list:
        todos_alunos = set()
        for atendimento in self.atendimentos:
            for aluno in atendimento.alunos_cadastrados:
                todos_alunos.add(aluno)
        
        return list(todos_alunos)

    def get_alunos_cancelados(self) -> list:
        return self.alunos_cancelados

    def get_hora_inicio(self) -> str:
        return self.hora_inicio 

    def get_hora_fim(self) -> str:
        return self.hora_fim
    