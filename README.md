# Seção 2 - Relatório de Execução (README)

**Como executar.** **Python:** 3.10 ou superior (testado no 3.13). **Bibliotecas:** nenhuma externa, só a biblioteca padrão (`unittest`, `datetime`, `threading`, `abc`, `typing`, `getpass`). **Arquivo principal:** `main.py`, na raiz do projeto (código em `codigo/`, testes em `testes/`). Todos os comandos devem ser rodados na raiz:

- Sistema: `python main.py`. Usuários de exemplo: `aluno`, `monitor` e `professor`, todos com senha `1234`.
- Testes: `python -m unittest discover testes -v` (62 testes, todos passando).

**Plano x realizado.**

| Data | Etapa planejada | Resp. no plano | O que foi feito, quando e por quem |
|---|---|---|---|
| 16/10 | Documentação inicial e cronograma (PT1) | João | Feito em dia, por João. |
| 17/10 | Criação do GitHub e milestones | Lorenzo | Passou para 18/10, por escolha da equipe (o dia de descanso era 18 e foi trocado para 17). Feito por João. |
| 17/10 | Histórias de usuário | João | Passou para 18/10, pelo mesmo motivo. Feito por Lorenzo. |
| 19/10 | Milestone 0: Sistema de login | Lorenzo | Feito em dia, por Lorenzo. |
| 19/10 | Milestone 1: Classes e suas permissões | João | **Transbordou** para 20 e 21/10, João. Ficou 50% (2 de 4 issues). |
| 20/10 | Milestone 2: Integração do login e classes | Lorenzo e João | Feito em dia, só por Lorenzo. |
| 21/10 | Milestone 3: Sistema de marcação de horário | João e Lorenzo | Feita em 21/10, finalizada e commitada em 22/10, por João e Lorenzo. |
| 22/10 | Revisão geral | Lorenzo e João | Feito em dia, por João e Lorenzo, junto com este relatório. |

**Atrasos e mudanças no cronograma.**

- **Milestone 1 transbordou para 20 e 21/10.** Foi mais complexa do que esperávamos e acabou sendo a milestone mais importante do projeto. Nela montamos o Role-Object (`Usuario` com os papéis `Aluno`, `Monitor` e `Professor`) e as classes de monitoria; a partir dela, com poucas linhas, completamos toda a Milestone 3.
- **Milestone 3 passou para 21/10 e foi finalizada e commitada em 22/10**, por causa do transbordo da Milestone 1, da qual ela dependia.
- **Milestone 2 ficou só com o Lorenzo.** Ela foi feita em dia, mas o João continuou responsável pela Milestone 1, que ainda não tinha terminado.

**Issues que não foram concluídas** (por isso a Milestone 1 ficou em 50%):

- **Criação e Configuração de Monitorias (Acesso: Monitor)**, nos itens *criar_monitoria() e editar_regras() só para Monitor* e *monitor não edita a monitoria de outro*. A criação foi feita e testada, mas a lógica de edição ficou mais complexa do que o esperado: ao editar, os atendimentos são recriados, e queríamos uma forma leve de guardar a monitoria antes e depois da edição. Com o tempo limitado, o `editar_monitoria` ficou numa versão básica, sem testes.
- **Gestão (Acesso: Professor)**, nos itens *visualizar_relatorio_monitor(monitor)* e o teste do professor lendo esses dados. Por falta de tempo não fizemos a geração de relatórios. Pensando no futuro, deixamos lugares específicos para guardar as monitorias criadas e canceladas (`monitorias`, `monitorias_canceladas` e `alunos_cancelados`), que serviriam para montar o relatório e contar as horas trabalhadas.

**Mudanças em relação ao projeto inicial.**

- **`ControladorReserva` não foi criado.** Com o Role-Object, só quem tem o papel `Aluno` tem o método de reserva, então a validação ficou em `Aluno.marcar_monitoria` (cancelado, duplicado, limite) e o controle de vagas em `Atendimento.marcar`.
- **Nova classe `Atendimento`.** O e-mail diz que cada atendimento dura 30 minutos, então a `Monitoria` é dividida em atendimentos de 30 min, cada um com suas vagas. O `marcar` usa um `Lock` para que dois alunos não peguem a mesma vaga ao mesmo tempo.
- **Nomes dos testes mudaram** em relação aos previstos no projeto inicial; as Seções 1 e 3 citam os testes que existem no código.

**Método de trabalho.** Usamos TDD: primeiro escrevíamos os testes (fase red) e depois o código até passar (fase green). Cada módulo foi feito para funcionar separado nos seus testes, e depois fizemos os testes que integram as partes (`teste_login_integrado.py`, `teste_integracao_monitoria.py` e `teste_integracao_permissoes.py`).
