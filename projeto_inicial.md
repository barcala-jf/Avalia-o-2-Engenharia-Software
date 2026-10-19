# Projeto Inicial: Reserva de Horários

**História de Usuário Escolhida (Prioridade Alta):**
Como aluno, eu gostaria de poder marcar os horários e matérias das monitorias que eu queira participar.

## 1\. Descrição das classes/funções

Para implementar esta história, o sistema utilizará as seguintes classes principais:

* **`Aluno` (herda de `Usuario`):** Representa o usuário autenticado que deseja realizar a reserva. É responsável por armazenar suas próprias informações de perfil e manter o histórico ou contador de reservas feitas na semana vigente, garantindo que a validação de limites por usuário seja possível.
* **`Monitoria`:** Entidade que armazena os dados do atendimento oferecido (disciplina, horário, monitor responsável, capacidade total e vagas disponíveis). Sua responsabilidade é gerenciar seu próprio estado de ocupação, permitindo ou negando a entrada de novos alunos com base na capacidade máxima (individual ou em grupo).
* **`ControladorReserva`:** Classe orquestradora (ou módulo de funções) responsável pela regra de negócio principal. Ela recebe a intenção de reserva do `Aluno` para uma determinada `Monitoria`, faz as validações necessárias (checa autenticação, verifica se há vagas e se o aluno não estourou o limite semanal) e, se tudo estiver correto, efetiva a reserva deduzindo uma vaga da sessão.

## 2\. Mapeamento de testes

Os critérios de aceitação da história acima serão verificados através do framework `unittest`, garantindo cenários de sucesso e exceção:

* **Critério de Aceitação 1:** O aluno só pode reservar uma monitoria se houver vagas disponíveis.

  * *Teste correspondente:* `test\_reserva\_com\_sucesso\_deduz\_vaga\_da\_monitoria` (Cenário de Sucesso)
* **Critério de Aceitação 2:** O sistema deve impedir a reserva caso a capacidade máxima (individual ou grupo) da monitoria já tenha sido atingida.

  * *Teste correspondente:* `test\_reserva\_em\_monitoria\_lotada\_levanta\_excecao` (Cenário de Falha/Exceção)
* **Critério de Aceitação 3:** O aluno não pode exceder o limite de reservas semanais estipulado pela coordenação (ex: 2 reservas por disciplina).

  * *Teste correspondente:* `test\_reserva\_acima\_do\_limite\_semanal\_bloqueada` (Cenário de Falha)
* **Critério de Aceitação 4:** Apenas usuários com a classe/perfil de aluno autenticado podem realizar a ação de reserva.

  * *Teste correspondente:* `test\_permissao\_apenas\_aluno\_pode\_efetivar\_reserva` (Cenário de Falha/Permissão)

