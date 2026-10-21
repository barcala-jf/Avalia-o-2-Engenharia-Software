import unittest

from codigo.monitorias import Monitoria
from codigo.repositorio_monitorias import RepositorioMonitorias


class TestRepositorioMonitorias(unittest.TestCase):
    def test_salvar_e_buscar_monitoria(self):
        repositorio = RepositorioMonitorias()

        monitoria = Monitoria(
            materia="Calculo",
            dia="Quarta-feira",
            hora_inicio="14:00",
            hora_fim="15:00",
            Vagas=2
        )

        identificador = repositorio.salvar(monitoria)
        resultado = repositorio.buscar(identificador)

        self.assertIs(resultado, monitoria)

    def test_excluir_monitoria(self):
        repositorio = RepositorioMonitorias()

        monitoria = Monitoria(
            materia="Calculo",
            dia="Quarta-feira",
            hora_inicio="14:00",
            hora_fim="15:00",
            Vagas=2
        )

        identificador = repositorio.salvar(monitoria)
        repositorio.excluir(identificador)
        self.assertIsNone(repositorio.buscar(identificador))