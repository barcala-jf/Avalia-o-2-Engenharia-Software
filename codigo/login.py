def autenticar(usuarios, user, senha):
    if user in usuarios:
        if senha == usuarios[user]["senha"]:
            return True
        else:
            return False
    else:
        return False
