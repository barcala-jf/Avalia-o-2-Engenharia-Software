import unittest
from datetime import date
from codigo.monitorias import Monitoria
from codigo.repositorio_monitorias import RepositorioMonitorias
from codigo.usuario_role_object import Usuario, Aluno, Professor, Monitor

class TestConsultaMonitorias(unittest.TestCase):
    def test_lista_atendimentos_disponiveis(self):
        repositorio = RepositorioMonitorias()
        user_monitor = Usuario("Neymar", "1", "1234", Aluno())
        professor = Usuario("Luiz", "2", "1234", Professor(["Calculo"]))
        professor.get_role(Professor).atribuir_monitor(user_monitor, "Calculo")
        monitor = user_monitor.get_role(Monitor)

        monitoria = Monitoria(
            monitor=monitor,
            materia="Calculo",
            dia="Quarta-feira",
            hora_inicio="14:00",
            hora_fim="15:30",
            Vagas=1,
            data=date(2026, 10, 28)
        )
        repositorio.salvar(monitoria)

        atendimentos = monitoria.get_atendimentos()

        aluno_inscrito = Usuario("João", "3", "1234", Aluno())
        aluno_inscrito.get_role(Aluno).marcar_monitoria(atendimentos[0])
        atendimentos[1].cancelar()

        aluno = Usuario("Lorenzo", "4", "1234", Aluno())
        resultado = aluno.get_role(Aluno).list_monitorias(repositorio)

        self.assertEqual(resultado, [{
            "materia": "Calculo",
            "monitor": "Joao",
            "data": date(2026, 10, 28),
            "dia": "Quarta-feira",
            "hora": "15:00",
            "vagas_disponiveis": 1
        }])