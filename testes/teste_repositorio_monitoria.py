import unittest

from codigo.monitorias import Monitoria
from codigo.repositorio_monitorias import RepositorioMonitorias
from codigo.usuario_role_object import Monitor


class TestRepositorioMonitorias(unittest.TestCase):
    def setUp(self):
        self.monitor = Monitor(["Calculo"])

    def test_salvar_e_buscar_monitoria(self):
        repositorio = RepositorioMonitorias()
        

        monitoria = Monitoria(
            monitor=self.monitor,
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
            monitor=self.monitor,
            materia="Calculo",
            dia="Quarta-feira",
            hora_inicio="14:00",
            hora_fim="15:00",
            Vagas=2
        )

        identificador = repositorio.salvar(monitoria)
        repositorio.excluir(identificador)
        self.assertIsNone(repositorio.buscar(identificador))
    
    def test_atualizar_monitoria(self):
        repositorio = RepositorioMonitorias()

        monitoria = Monitoria(
            monitor=self.monitor,
            materia="Calculo",
            dia="Quarta-feira",
            hora_inicio="14:00",
            hora_fim="15:00",
            Vagas=2
        )

        identificador = repositorio.salvar(monitoria)

        atualizada = Monitoria(
            monitor=self.monitor,
            materia="Calculo",
            dia="Sexta-feira",
            hora_inicio="16:00",
            hora_fim="17:00",
            Vagas=3
        )

        repositorio.atualizar(identificador, atualizada)

        resultado = repositorio.buscar(identificador)
        self.assertIs(resultado, atualizada)

    def test_atualizar_monitoria_inexistente(self):
        repositorio = RepositorioMonitorias()
        monitoria = Monitoria(
            monitor=self.monitor,
            materia="Calculo",
            dia="Quarta-feira",
            hora_inicio="14:00",
            hora_fim="15:00",
            Vagas=2
        )

        with self.assertRaises(KeyError):
            repositorio.atualizar(999, monitoria)