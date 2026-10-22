from codigo.login import realizar_login
from getpass import getpass
from codigo.repositorio_usuario import RepositorioUsuario
from codigo.sessao import Sessao
from codigo.usuario_role_object import Usuario, Aluno, Monitor, Professor

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

def menu_usuario(sessao):
    usuario = sessao.usuario_atual()

    while True:
        print(f"\nOlá, {usuario.get_nome()}!")
        papeis = [papel.__name__ for papel in (Aluno, Monitor, Professor) if usuario.have_role(papel)]
        print("Papéis:",", ".join(papeis))
        print("0 - exit")
        opcao = input("").strip()
        if opcao == "0":
            sessao.encerrar_sessao()
            print("Sessão Encerrada")
            return
        print("Opção Inválida")
    
def main():
    repositorio_usuarios = RepositorioUsuario()
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
        menu_usuario(sessao)

if __name__ == "__main__":
    main()