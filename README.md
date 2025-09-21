# Agenda VTA - Sistema de Agendamento para Clínica Veterinária

## Sobre o Projeto

O **Agenda VTA** é um sistema de agendamento desenvolvido para otimizar a gestão de consultas e o uso das salas de atendimento na clínica veterinária **Vet Assistance**. O projeto nasceu da necessidade de substituir o controle manual por planilhas, que era suscetível a erros, agendamentos duplicados e não oferecia uma visão clara da disponibilidade dos recursos.

O foco da solução é fornecer uma ferramenta **estável, rápida e intuitiva** para a equipe interna, principalmente para a recepção, que realiza um alto volume de agendamentos diários e simultâneos.

**Importante:** Este sistema é de **uso exclusivo da equipe da clínica** e não possui portal de acesso para os clientes finais.

-----

## 🚀 Principais Funcionalidades (MVP)

O escopo inicial do projeto (MVP) foi definido para atender às necessidades mais críticas da clínica:

  * 🔐 **Autenticação de Usuários (UC01):** Sistema de login seguro com perfis de acesso (recepção, veterinário, administrador).
  * 👥 **Gestão de Clientes e Pets (UC02):** Cadastro, consulta, edição e exclusão de tutores e seus pets, centralizando as informações.
  * 🗓️ **Visualização da Agenda por Sala (UC03):** Grade de horários organizada por sala, com modos de visualização por dia e semana.
  * ✅ **Realizar Agendamento (UC04):** Fluxo simples para marcar novas consultas, validando conflitos de horário e disponibilidade de sala.
  * 🚫 **Bloqueio de Horários (UC05):** Funcionalidade administrativa para bloquear datas ou horários específicos, impedindo novos agendamentos.
  * 📢 **Notificação Interna de Alterações (UC06):** Alertas no painel da recepção sobre mudanças ou cancelamentos de agendamentos.
  * 📊 **Relatórios Gerenciais (UC07):** Geração de relatórios mensais para análise de atendimentos.
  * 🐾 **Histórico do Pet (UC08):** Acesso rápido ao histórico de agendamentos de cada animal.

-----

## 🏛️ Arquitetura e Princípios de Design

Este projeto foi guiado por premissas essenciais definidas junto ao cliente para garantir a aderência à realidade da clínica:

1.  **Estabilidade em Primeiro Lugar:** A prioridade máxima é um sistema que "não pode cair". As decisões técnicas favoreceram a estabilidade e a simplicidade para garantir a continuidade da operação.
2.  **Segurança Contra Erros:** Toda ação de exclusão exige uma **confirmação em duas etapas**, minimizando o risco de perda acidental de dados.
3.  **Comunicação Controlada e Humanizada:** O sistema **não envia mensagens automáticas** via WhatsApp. Em vez disso, gera um "ticket" de texto padronizado para que a recepção possa copiar, colar e enviar manualmente, mantendo um contato pessoal com o cliente.
4.  **Foco na Usabilidade da Recepção:** A interface foi pensada para a persona da recepcionista (25–32 anos), que precisa de máxima agilidade para realizar tarefas repetitivas em um ambiente com múltiplos atendimentos simultâneos.

-----

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia |
| :--- | :--- |
| **Front-End** | `HTML5`, `CSS3`, `JavaScript` |
| **Back-End** | `Java`, `Spring Boot` |
| **Banco de Dados** | `PostgreSQL` |
| **Versionamento** | `Git`, `GitHub` |
| **Gerenciamento** | `Trello` |

-----

## 🏁 Como Executar o Projeto (Guia Rápido)

Para configurar e rodar o ambiente de desenvolvimento localmente, siga estes passos:

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/trickGit/Agenda-Vet.git
    ```

2.  **Configuração do Back-end:**

      * Navegue até a pasta do projeto back-end.
      * Instale as dependências do Maven.
      * Configure as variáveis de ambiente no arquivo `application.properties`, incluindo as credenciais do banco de dados PostgreSQL.
      * Execute a aplicação Spring Boot.

3.  **Configuração do Front-end:**

      * Navegue até a pasta do projeto front-end.
      * Abra o arquivo `index.html` em seu navegador de preferência ou utilize um servidor local (como o Live Server do VSCode).

4.  **Acesso ao Sistema:**

      * Após iniciar ambos os ambientes, o sistema estará acessível. Utilize as credenciais padrão de administrador para o primeiro acesso.

-----

## 👥 Equipe do Projeto

| Integrante | Papel |
| :--- | :--- |
| **Augusto Azambuya M. da Silva** | Desenvolvedor Back-end |
| **Lucas Ramos Alves** | Communicator |
| **Mateus Franceschet Pereira** | Desenvolvedor Front-end |
| **Patrick Vargas Santos** | Desenvolvedor Full-Stack |
| **Roger Luiz do Nascimento Vesely** | Scrum Master |
