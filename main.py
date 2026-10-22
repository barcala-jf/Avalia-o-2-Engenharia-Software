from codigo.login import realizar_login
from getpass import getpass
from codigo.repositorio_usuario import RepositorioUsuario
from codigo.sessao import Sessao
from codigo.usuario_role_object import Usuario, Aluno, Monitor, Professor
from codigo.repositorio_monitorias import RepositorioMonitorias

def criar_usuarios_exemplo(repositorio):
    aluno = Usuario(
        nome="Lorenzo",
        user="aluno",
        senha="1234",
        role_inicial=Aluno(["Calculo"]),
    )

    monitor = Usuario(
        nome="Joao",
        user="monitor",
        senha="1234",
        role_inicial=Aluno(["Calculo"]),
    )

    professor = Usuario(
        nome="Luiz",
        user="professor",
        senha="1234",
        role_inicial=Professor(["Calculo"]),
    )

    professor.get_role(Professor).atribuir_monitor(monitor, "Calculo")
    for usuario in (aluno, monitor, professor):
        repositorio.salvar(usuario)

def criar_monitoria(usuario, repositorio):
    monitor = usuario.get_role(Monitor)
    print("Disciplinas:", ", ".join(monitor.get_disciplinas_monitorias()))
    materia = input("Matéria: ").strip()
    dia = input("Dia da semana: ").strip()
    inicio = input("Horário inicial (HH:MM): ").strip()
    fim = input("Horário final (HH:MM): ").strip()
    vagas = int(input("Vagas por atendimento: "))

    if vagas <= 0:
        raise ValueError("Não pode vagas negativas")

    monitor.criar_monitoria(materia,dia,inicio,fim,vagas)
    monitoria = monitor.get_monitorias()[-1]
    identificador = repositorio.salvar(monitoria)

    print(f"Monitoria criada! id: {identificador}")

def consultar_monitorias(usuario, repositorio):
    aluno = usuario.get_role(Aluno)
    atendimentos = aluno.list_monitorias(repositorio)

    if not atendimentos:
        print("Nenhum atendimento encontrado")
        return

    for atendimento in atendimentos:
        print(
            f"{atendimento['materia']} | "
            f"Monitor: {atendimento['monitor']} | "
            f"Dia {atendimento['dia']} as {atendimento['hora']} | "
            f"Vagas: {atendimento['vagas_disponiveis']}"
        )

def escolher_atendimento(atendimentos):
    if not atendimentos:
        print("Nenhum atendimento encontrado")
        return None
    
    for numero, atendimento in enumerate(atendimentos, start=1):
        monitoria = atendimento.monitoria
        status = "Cancelado" if atendimento.cancelado else "Ativo"

        print(
            f"{numero} - {monitoria.materia} | "
            f"{monitoria.dia} às {atendimento.hora} | "
            f"Monitor: {monitoria.monitor.usuario.get_nome()} | "
            f"{status}"
        )

    escolha = int(input("Escolha o atendimento (0 para voltar): "))

    if escolha == 0:
        return None
    if escolha < 1 or escolha > len(atendimentos):
        raise ValueError("Opção Inválida")

    return atendimentos[escolha - 1]

def reservar_atendimento(usuario, repositorio):
    aluno = usuario.get_role(Aluno)
    disponiveis = []

    for monitoria in repositorio.listar():
        if monitoria.cancelado:
            continue

        for atendimento in monitoria.get_atendimentos():
            if not atendimento.cancelado and (len(atendimento.alunos_cadastrados) < atendimento.vagas):
                disponiveis.append(atendimento)
    atendimento = escolher_atendimento(disponiveis)

    if atendimento is not None:
        aluno.marcar_monitoria(atendimento)
        print("Reserva Realizada!")

def cancelar_reserva(usuario):
    aluno = usuario.get_role(Aluno)
    atendimento = escolher_atendimento(aluno.get_monitorias_marcadas())

    if atendimento is not None:
        aluno.cancelar_monitoria(atendimento)
        print("Reserva Cancelada")

def cancelar_monitoria(usuario):
    monitor = usuario.get_role(Monitor)
    monitorias = [monitoria for monitoria in monitor.get_monitorias() if not monitoria.cancelado
    ]

    if not monitorias:
        print("Nenhuma monitoria ativa para cancelar.")
        return

    for numero, monitoria in enumerate(monitorias, start=1):
        print(
            f"{numero} - {monitoria.materia} | "
            f"{monitoria.dia} | "
            f"{monitoria.hora_inicio} às {monitoria.hora_fim}"
        )

    escolha = int(input("Escolha a monitoria (0 para voltar): "))

    if escolha == 0:
        return

    if escolha < 1 or escolha > len(monitorias):
        raise ValueError("Monitoria inválida")

    monitor.cancelar_monitoria(monitorias[escolha - 1])
    print("Monitoria e seus atendimentos cancelados!")


def atribuir_monitor(usuario, repositorio_usuarios):
    professor = usuario.get_role(Professor)

    login = input("Login do aluno: ").strip()
    alvo = repositorio_usuarios.buscar(login)

    if alvo is None:
        raise ValueError("Usuário não encontrado")

    print("Disciplinas do professor:",", ".join(professor.disciplinas_ministradas),)
    disciplina = input("Disciplina: ").strip()

    professor.atribuir_monitor(alvo, disciplina, repositorio_usuarios)
    print(f"{alvo.get_nome()} agora é monitor de {disciplina}!")


def menu_usuario(sessao, repositorio_monitorias, repositorio_usuarios):
    usuario = sessao.usuario_atual()

    while True:
        print(f"\nOlá, {usuario.get_nome()}!")
        
        if usuario.have_role(Aluno):
            print("1 - Consultar Atendimentos")
            print("3 - Reservar atendimento")
            print("4 - Cancelar reserva")

        if usuario.have_role(Monitor):
            print("2 - Criar Monitoria")
            print("5 - Cancelar Monitoria")

        if usuario.have_role(Professor):
            print("6 - Atribuir monitor")

        print("0 - exit")
        opcao = input("").strip()
    
        try:
            if opcao == "0":
                sessao.encerrar_sessao()
                print("Sessão Encerrada")
                return
            elif opcao == "1" and usuario.have_role(Aluno):
                consultar_monitorias(usuario, repositorio_monitorias)
            elif opcao == "2" and usuario.have_role(Monitor):
                criar_monitoria(usuario, repositorio_monitorias)
            elif opcao == "3" and usuario.have_role(Aluno):
                reservar_atendimento(usuario, repositorio_monitorias)
            elif opcao == "4" and usuario.have_role(Aluno):
                cancelar_reserva(usuario)
            elif opcao == "5" and usuario.have_role(Monitor):
                cancelar_monitoria(usuario)
            elif opcao == "6" and usuario.have_role(Professor):
                atribuir_monitor(usuario, repositorio_usuarios)
            else:
                print("Opção Inválida")
        
        except (ValueError, PermissionError) as erro:
            print(f"Não foi possivel realizar a operação: {erro}")
        
def main():
    repositorio_usuarios = RepositorioUsuario()
    repositorio_monitorias = RepositorioMonitorias()
    sessao = Sessao()
    criar_usuarios_exemplo(repositorio_usuarios)

    while True:
        print("\n=== Monitorias ===")
        print("1 - Entrar")
        print("0 - Sair")

        opcao = input("").strip()
        
        if opcao == "0":
            print("Sistema Encerrado")
            return
        if opcao !="1":
            print("Opção Invalida")
            continue
        login = input("Usuário: ").strip()
        senha = getpass("Senha: ")

        try:
            usuario = realizar_login(repositorio_usuarios, login, senha)
        except ValueError as erro:
            print(erro)
            continue

        sessao.iniciar_sessao(usuario)
        menu_usuario(sessao, repositorio_monitorias, repositorio_usuarios)

if __name__ == "__main__":
    main()