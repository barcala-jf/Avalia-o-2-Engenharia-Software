def autenticar(usuarios, user, senha):
    if user in usuarios:
        if senha == usuarios[user]["senha"]:
            return True
    else:
        return False

def realizar_login(repositorio, login, senha):
    pass
