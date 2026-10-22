import threading
from datetime import date, datetime, timedelta

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

    def desmarcar(self, aluno) -> bool:
        with self.lock: # Blqueia o acesso a recursos compartilhados para evitar condições de corrida
            if aluno not in self.alunos_cadastrados:
                return False

            self.alunos_cadastrados.remove(aluno)
            self.lotado = len(self.alunos_cadastrados) >= self.vagas
            self.monitoria.registrar_cancelamento_aluno(aluno)
            return True

class Monitoria:
    def __init__(self, monitor: 'Monitor', materia: str, dia: str, hora_inicio: str , hora_fim: str, Vagas: int) -> None:
        self.monitor = monitor
        self.materia = materia

        i, f = datetime.strptime(hora_inicio, "%H:%M"), datetime.strptime(hora_fim, "%H:%M")
        self.hora_inicio = i.strftime("%H:%M")
        self.hora_fim = f.strftime("%H:%M")

        i = datetime.strptime(hora_inicio, "%H:%M")
        f = datetime.strptime(hora_fim, "%H:%M")

        duracao_minutos = (f - i).total_seconds() / 60

        if duracao_minutos <= 0 or duracao_minutos % 30 != 0:
            raise ValueError("A duração deve ser positiva e múltipla de 30 minutos")

        self.atendimentos = []
        for hora in self._gerar_horarios(i, f):
            self.atendimentos.append(Atendimento(hora, Vagas, self))

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

    def editar_monitoria(self, dia: str = None, hora_inicio: str = None, hora_fim: str = None, vagas: int = None) -> None:
        if dia:
            self.dia = dia
            
        if hora_inicio or hora_fim:
            novo_inicio = hora_inicio or self.hora_inicio
            novo_fim = hora_fim or self.hora_fim
            
            i, f = datetime.strptime(novo_inicio, "%H:%M"), datetime.strptime(novo_fim, "%H:%M")
            self.hora_inicio = i.strftime("%H:%M")
            self.hora_fim = f.strftime("%H:%M")
            
            self.atendimentos = []
            for hora in self._gerar_horarios(i, f):

                vagas_atual = vagas if vagas is not None else 1
                self.atendimentos.append(Atendimento(hora, vagas_atual, self))
                
        elif vagas is not None:
            for atendimento in self.atendimentos:
                atendimento.vagas = vagas

    def cancelar_atendimento(self, atendimento: Atendimento) -> None:
        atendimento.cancelar()

    def cancelar_monitoria(self) -> None:
        for atendimento in self.atendimentos:
            atendimento.cancelar()

        self.cancelado = True

    def reativar_monitoria(self) -> None:
        for atendimento in self.atendimentos:
            atendimento.cancelado = False

        self.cancelado = False

    def registrar_cancelamento_aluno(self, aluno: str) -> None:
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
    