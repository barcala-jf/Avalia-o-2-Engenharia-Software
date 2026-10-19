def identificar_perfil(usuarios, user):
    if user in usuarios:
        return usuarios[user]["role"]