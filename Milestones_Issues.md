# Resumo do Projeto: Sistema de Agendamento de Monitorias

## Visão Geral

O projeto visa construir um protótipo de sistema em Python para gerenciar horários de monitorias. O objetivo é facilitar a conexão entre alunos e monitores, resolvendo problemas de choque de horários, cancelamentos de última hora e coleta de dados para a coordenação, operando sob diferentes níveis de permissão.

## Arquitetura e Tecnologias

* **Linguagem:** Python
* **Testes Automatizados:** `unittest`
* **Persistência:** Banco de Dados Simulado (Mock database)
* **Padrões de Projeto Base:** Role-Object Pattern (para evolução de Aluno para Monitor) e Singleton (para configuração de monitorias).

---

## Roadmap de Desenvolvimento (Milestones e Issues)

### Milestone 0: Sistema de Login e Autenticação

Estabelece a entrada segura no sistema, simulando o banco de dados da instituição e identificando corretamente o tipo de usuário no momento do acesso.

* **Issue #1: [Feature] Implementar mock de banco de dados e validação de credenciais**
  * *Descrição:* Criar a base de dados simulada contendo os cadastros de alunos, monitores e professores, e implementar a função principal de login verificando login e senha.
  * *Critérios de Aceitação:* 
    * Criar estrutura de dados simulada com usuários de teste.
    * Criar a função de realizar login.
    * Retornar sucesso para credenciais corretas.
    * Levantar exceção/erro claro para credenciais inválidas.
    * Testes no `unittest` para sucesso e falha.

* **Issue #2: [Feature] Implementar identificação de Perfil do Usuário (Role)**
  * *Descrição:* Após a validação, o sistema deve identificar o nível de acesso do usuário e retornar a classe correta (Professor, Aluno ou Monitor).
  * *Critérios de Aceitação:*
    * Adicionar atributo de perfil/role no banco simulado.
    * Instanciar e retornar o usuário na classe correta após o login.
    * Testes no `unittest` garantindo o retorno das permissões adequadas para cada perfil.

* **Issue #3: [Feature] Implementar funcionalidade "Relembre-me" (Sessão)**
  * *Descrição:* Criar simulação de geração de token ou sessão persistente para login automático nas próximas execuções.
  * *Critérios de Aceitação:*
    * Modificar função de login para aceitar `relembre_me=True`.
    * Gerar token simulado associado ao usuário.
    * Criar função de login direto pelo token.
    * Testes no `unittest` validando o acesso via token.

---

### Milestone 1: Classes e suas Permissões

Define a estrutura de dados orientada a objetos das entidades do sistema e blinda o acesso a funções específicas de acordo com o cargo do usuário.

* **Issue #1: [Estrutura] Implementar o padrão Role-Object para Alunos e Monitores**
  * *Descrição:* Criar a estrutura base de classes. Um aluno deve poder receber a "role" de Monitor, herdando novas permissões.
  * *Critérios de Aceitação:*
    * Criar classes `Usuario`, `Aluno` e `Professor`.
    * Implementar o padrão Role-Object para o `Monitor`.
    * Implementar método `promover_para_monitor(aluno)` no Professor.
    * Testes no `unittest` para sucesso e falha de permissão.

* **Issue #2: [Feature] Criação e Configuração de Monitorias (Acesso: Monitor)**
  * *Descrição:* Criar a entidade Monitoria e dar poder aos monitores para criar e editar suas próprias sessões.
  * *Critérios de Aceitação:*
    * Criar a classe `Monitoria` (disciplina, horários, capacidade, status).
    * Implementar métodos de criação e edição apenas para Monitores.
    * Garantir que um monitor não edite a sessão de outro.
    * Testes no `unittest` validando criação e bloqueando acesso de Alunos.

* **Issue #3: [Feature] Visualização e Consulta de Monitorias (Acesso: Aluno)**
  * *Descrição:* Alunos devem poder verificar as monitorias disponíveis.
  * *Critérios de Aceitação:*
    * Criar método para listar monitorias ativas.
    * Ocultar dados sensíveis dos monitores na visualização.
    * Testes no `unittest` validando o retorno seguro dos dados.

* **Issue #4: [Feature] Gestão e Acesso a Relatórios (Acesso: Professor)**
  * *Descrição:* Professores precisam visualizar informações privadas dos monitores (horas trabalhadas).
  * *Critérios de Aceitação:*
    * Adicionar atributo de horas trabalhadas no perfil de Monitor.
    * Implementar visualização de relatório para o Professor.
    * Testes no `unittest` garantindo acesso ao Professor e bloqueando Alunos.

---

### Milestone 2: Integração e Banco de Dados

Conecta o sistema de autenticação com as classes de permissão, garantindo que as ações dos usuários modifiquem permanentemente o estado do banco de dados em memória.

* **Issue #1: [Infraestrutura] Implementar e Estruturar o Banco de Dados Simulado (Mock Database)**
  * *Descrição:* Expandir a base temporária para suportar entidades e relacionamentos através de repositórios em memória.
  * *Critérios de Aceitação:*
    * Criar `RepositorioUsuarios` e `RepositorioMonitorias`.
    * Garantir persistência em memória durante a execução.
    * Testes no `unittest` para inserção e busca de dados.

* **Issue #2: [Integração] Acoplar Sistema de Login com a Injeção de Perfis (Roles)**
  * *Descrição:* O login deve buscar o usuário no repositório e injetar a classe correta com os dados do banco.
  * *Critérios de Aceitação:*
    * Atualizar login para usar o `RepositorioUsuarios`.
    * Instanciar dinamicamente o perfil baseado nos dados do banco.
    * Testes no `unittest` simulando login completo de um monitor.

* **Issue #3: [Integração] Fluxo Completo: Login e Criação de Monitoria**
  * *Descrição:* Validar o MVP garantindo que um monitor logado consegue criar e salvar uma monitoria no banco.
  * *Critérios de Aceitação:*
    * Logar como Monitor e chamar a criação de monitoria.
    * Salvar a monitoria no `RepositorioMonitorias`.
    * Teste de integração no `unittest` validando todo o fluxo ponta a ponta.

* **Issue #4: [Integração] Atualização Dinâmica de Permissões no Banco**
  * *Descrição:* Refletir a promoção de um aluno a monitor no banco de dados para os próximos logins.
  * *Critérios de Aceitação:*
    * Atualizar o repositório quando um professor promover um aluno.
    * Teste no `unittest` validando promoção, novo login e aplicação da nova role.

---

### Milestone 3: Implementação do sistema de marcação de horário

O núcleo de valor do projeto, onde as regras de negócio de agendamento são aplicadas para resolver o problema central dos alunos e monitores.

* **Issue #1: [Feature] Fluxo de Reserva de Horário (Acesso: Aluno)**
  * *Descrição:* O aluno deve conseguir selecionar uma monitoria disponível e ocupar uma vaga nela.
  * *Critérios de Aceitação:*
    * Criar método de reserva acessível apenas ao Aluno.
    * Deduzir vaga da capacidade total da monitoria.
    * Impedir reserva em horários lotados.
    * Testes no `unittest` para sucesso e lotação.

* **Issue #2: [Regra de Negócio] Capacidade (Grupo vs Individual) e Limites Semanais**
  * *Descrição:* Diferenciar atendimentos e limitar agendamentos por aluno na semana.
  * *Critérios de Aceitação:*
    * Monitor define a capacidade na criação da sessão.
    * Validar quantidade de reservas do aluno por disciplina.
    * Bloquear caso exceda o limite.
    * Testes no `unittest` validando bloqueio na terceira tentativa (se limite for 2).

* **Issue #3: [Feature] Cancelamento de Horário pelo Monitor**
  * *Descrição:* Permitir que o monitor cancele a sessão, liberando os alunos.
  * *Critérios de Aceitação:*
    * Criar método de cancelamento exclusivo para o monitor dono do horário.
    * Mudar status para "Cancelada" no banco.
    * Remover horário das listas de disponibilidade.
    * Testes no `unittest` validando a mudança de status e sumiço da lista.

* **Issue #4: [Feature] Cancelamento de Reserva pelo Aluno**
  * *Descrição:* O aluno deve poder cancelar sua reserva, devolvendo a vaga.
  * *Critérios de Aceitação:*
    * Criar método de cancelamento de reserva acessível ao Aluno.
    * Restaurar +1 vaga na monitoria.
    * Testes no `unittest` validando a devolução da vaga.