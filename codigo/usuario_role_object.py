from abc import ABC
from typing import Dict, Type, TypeVar, Optional
from datetime import datetime

from codigo.monitorias import Monitoria, Atendimento


U = TypeVar("U", bound="RoleUsuario")


class RoleUsuario(ABC):
    ''' Classe base para as roles. (ComponentRole)'''

    def __init__(self) -> None:
        self.usuario: Optional['Usuario'] = None


# Classes Role (ConcreteRoles)
class Aluno(RoleUsuario):
    def __init__(self, materias: Optional[list[str]] = None) -> None:
        super().__init__()
        self.materias: list[str] = list(materias) if materias is not None else []
        self.monitorias_marcadas: list['Atendimento'] = []

    def list_monitorias(self, repositorio):
        ''' Deve listar as monitorias disponíveis na semana'''
        disponiveis = []

        for monitoria in repositorio.listar():
            if monitoria.cancelado:
                continue

            for atendimento in monitoria.get_atendimentos():
                vagas_livres = (
                    atendimento.vagas - len(atendimento.alunos_cadastrados)
                )

                if atendimento.cancelado or vagas_livres <= 0:
                    continue

                disponiveis.append({
                    "materia": monitoria.materia,
                    "monitor": monitoria.monitor.usuario.get_nome(),
                    "dia": monitoria.dia,
                    "hora": atendimento.hora,
                    "vagas_disponiveis": vagas_livres
                })

        return disponiveis

    def marcar_monitoria(self, atendimento: Atendimento):
        if atendimento.cancelado:
            raise ValueError("Atendimento cancelado")

        if atendimento in self.monitorias_marcadas:
            raise ValueError("Reserva já realizada")

        monitoria = atendimento.monitoria

        reservas_da_disciplina = sum(
            1
            for reserva in self.monitorias_marcadas
            if not reserva.cancelado
            and reserva.monitoria.materia == monitoria.materia
        )

        if reservas_da_disciplina >= 2:
            raise ValueError("Limite de reservas atingido para esta disciplina"
        )

        if not atendimento.marcar(self.usuario):
            raise ValueError("Horário Lotado")

        self.monitorias_marcadas.append(atendimento)

    def cancelar_monitoria(self, atendimento: Atendimento):
        ''' Deve cancelar uma monitoria já marcada'''
        if atendimento not in self.monitorias_marcadas:
            raise ValueError("Reserva não encontrada")

        if not atendimento.desmarcar(self.usuario):
            raise ValueError("Aluno não cadastrado no atendimento")

        self.monitorias_marcadas.remove(atendimento)

    def get_monitorias_participadas(self):
        ''' Deve listar as monitorias já participadas'''
        return self.monitorias_marcadas     

    def get_monitorias_marcadas(self):
        ''' Deve listar as monitorias marcadas da semana'''
        return self.monitorias_marcadas

    def get_materias(self) -> list[str]:
        return self.materias


class Monitor(RoleUsuario):
    def __init__(self, disciplinas_monitorias: Optional[list[str]] = None) -> None:
        super().__init__()
        self.disciplinas_monitorias: list[str] = (
            list(disciplinas_monitorias) if disciplinas_monitorias is not None else []
        )
        self.monitorias: list[Monitoria] = []
        self.monitorias_canceladas: list[Monitoria] = []

    def criar_monitoria(self, materia: str, dia: str,hora_inicio: str, hora_fim: str,Vagas: int):
        ''' Deve criar uma monitoria com hora de uma materia que ele seja monitor'''
        if materia not in self.disciplinas_monitorias:
            raise PermissionError(
                f"O monitor não pode criar monitoria para a matéria {materia}."
            )

        self.monitoria = Monitoria(monitor=self, materia=materia, dia=dia, hora_inicio=hora_inicio, hora_fim=hora_fim, Vagas=Vagas)
        self.monitorias.append(self.monitoria)

    def editar_monitoria(self, monitoria: 'Monitoria', dia: str = None, hora_inicio: str = None, hora_fim: str = None, vagas: int = None):
        ''' Edita os detalhes de uma monitoria existente '''
        monitoria_encontrada = self.get_monitoria(monitoria)
        
        if monitoria_encontrada is None:
            raise ValueError("A monitoria solicitada não foi encontrada como Monitoria deste Monitor.")
            
        monitoria_encontrada.editar_monitoria(dia, hora_inicio, hora_fim, vagas)

    def cancelar_monitoria(self, monitoria: Monitoria):
        ''' Cancela uma monitoria já marcada para aquela semana'''
        monitoria_encontrada = self.get_monitoria(monitoria)
        
        if monitoria_encontrada is None:
            raise ValueError("A monitoria solicitada não foi encontrada no sistema.")
            
        self.monitorias_canceladas.append(monitoria_encontrada)
        monitoria_encontrada.cancelar_monitoria()

    def reativar_monitoria(self, monitoria: Monitoria):
        ''' Reativa uma monitoria cancelada para aquela semana'''
        self.monitorias_canceladas.remove(self.get_monitoria(monitoria))
        self.get_monitoria(monitoria).reativar_monitoria()

    def get_monitoria(self, monitoria: Monitoria):
        ''' Deve selecionar uma monitoria especifica da lista de monitorias do monitor'''
        return self.monitorias[self.monitorias.index(monitoria)]

    def get_monitorias(self):
        ''' Deve listar as monitorias criadas'''
        return self.monitorias

    def get_monitorias_canceladas(self):
        ''' Deve listar as monitorias canceladas'''
        return self.monitorias_canceladas

    def get_disciplinas_monitorias(self) -> list[str]:
        ''' Deve listar as matérias em que ele é monitor'''
        return self.disciplinas_monitorias


class Professor(RoleUsuario):
    def __init__(self, disciplinas_ministradas: Optional[list[str]] = None) -> None:
        super().__init__()
        self.disciplinas_ministradas: list[str] = (
            list(disciplinas_ministradas) if disciplinas_ministradas is not None else []
        )

    def atribuir_monitor(self, alvo: "Usuario", disciplina: str, repositorio=None) -> None:
        # 1. O atribuído deve obrigatoriamente ser um Aluno
        if not alvo.have_role(Aluno):
            raise PermissionError(
                f"O usuário '{alvo.nome}' não é um aluno e não pode ser monitor."
            )

        # 2. A atribuição deve ser dada a uma matéria ministrada por este professor
        if disciplina not in self.disciplinas_ministradas:
            raise PermissionError(
                f"O professor não leciona a disciplina '{disciplina}'."
            )

        # 3. Se o aluno JÁ tem a role Monitor, apenas adiciona a nova disciplina na lista dele
        if alvo.have_role(Monitor):
            role_monitor = alvo.get_role(Monitor)
            if role_monitor and disciplina not in role_monitor.disciplinas_monitorias:
                role_monitor.disciplinas_monitorias.append(disciplina)
        else:
            # Caso ainda não seja Monitor, cria a role Monitor com a primeira disciplina
            novo_monitor = Monitor(disciplinas_monitorias=[disciplina])
            alvo._definir_role_interno(novo_monitor)

        if repositorio is not None:
            repositorio.salvar(alvo)

    def retirar_monitoria(self, alvo: "Usuario", disciplina: str) -> None:
        # 1. Verifica se o professor leciona a disciplina que ele quer retirar
        if disciplina not in self.disciplinas_ministradas:
            raise PermissionError(
                f"O professor não leciona a disciplina '{disciplina}' e não pode removê-la."
            )

        # 2. Verifica se o alvo realmente tem a role de Monitor
        role_monitor = alvo.get_role(Monitor)
        if not role_monitor:
            raise ValueError(f"O usuário '{alvo.nome}' não possui o papel de monitor.")

        # 3. Verifica se o aluno é monitor especificamente dessa disciplina
        if disciplina not in role_monitor.disciplinas_monitorias:
            raise ValueError(
                f"O usuário '{alvo.nome}' não é monitor da disciplina '{disciplina}'."
            )

        # 4. Remove apenas a disciplina da lista
        role_monitor.disciplinas_monitorias.remove(disciplina)

        # 5. Se não sobrou nenhuma disciplina de monitoria, retira a role Monitor do usuário
        if len(role_monitor.disciplinas_monitorias) == 0:
            alvo._remover_role_interno(Monitor)

    def contar_horas_trabalhadas(self, monitor: 'Monitor') -> float:
        materias_em_comum = set(self.disciplinas_ministradas).intersection(monitor.get_disciplinas_monitorias())
        if not materias_em_comum:
            raise PermissionError("O monitor não leciona nenhuma matéria deste professor.")
        
        horas_trabalhadas = 0.0
        
        for monitoria in monitor.get_monitorias():
            if monitoria.materia in self.disciplinas_ministradas:
                # Converte as strings de volta para datetime para fazer a conta
                inicio = datetime.strptime(monitoria.hora_inicio, "%H:%M")
                fim = datetime.strptime(monitoria.hora_fim, "%H:%M")
                
                # Calcula a duração (fim - inicio) e extrai o valor em horas
                diferenca = fim - inicio
                horas_trabalhadas += diferenca.total_seconds() / 3600
        
        return horas_trabalhadas

class Usuario:
    ''' Usuário Core, cuja role inicial (Aluno ou Professor) vem do login. (ComponentCore)'''

    def __init__(
        self,
        nome: str,
        user: str,
        senha: str,
        role_inicial: Optional[RoleUsuario] = None
    ) -> None:
        self.nome = nome
        self.user = user
        self.senha = senha

        # Dic que mapeia os papéis do usuário
        self._roles: Dict[Type[RoleUsuario], RoleUsuario] = {}

        # O sistema de login/cadastro já define se ele entra como Aluno ou Professor
        if role_inicial is not None:
            if not isinstance(role_inicial, (Aluno, Professor)):
                raise PermissionError(
                    "A role inicial de login deve ser apenas Aluno ou Professor."
                )
            self._definir_role_interno(role_inicial)

    # Métodos internos (protegidos por convenção com "_") usados pelo Professor e pelo Login
    def _definir_role_interno(self, role: RoleUsuario) -> None:
        role.usuario = self
        self._roles[type(role)] = role

    def _remover_role_interno(self, tipo_role: Type[RoleUsuario]) -> None:
        role_removido = self._roles.pop(tipo_role, None)
        if role_removido:
            role_removido.usuario = None

    def have_role(self, tipo_role: Type[RoleUsuario]) -> bool:
        return tipo_role in self._roles

    def get_role(self, tipo_role: Type[U]) -> U | None:
        role = self._roles.get(tipo_role)
        return role if isinstance(role, tipo_role) else None

    def get_nome(self) -> str:
        return self.nome

    def get_user(self) -> str:
        return self.user