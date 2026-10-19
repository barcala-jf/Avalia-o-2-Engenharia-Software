def identificar_perfil(usuarios, user):
    roles_validas = {"aluno", "professor", "monitor"}
    if user in usuarios:
        if usuarios[user]["role"] in roles_validas:
            return usuarios[user]["role"]
        raise ValueError("Role Inválida")
        