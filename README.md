
# Agenda VTA - Sistema de Agendamento para Clínica Veterinária

## Sobre o Projeto

[cite\_start]O **Agenda VTA** é um sistema de agendamento desenvolvido para otimizar a gestão de consultas e o uso das salas de atendimento na clínica veterinária **Vet Assistance**[cite: 9, 12]. [cite\_start]O projeto nasceu da necessidade de substituir o controle manual por planilhas de Excel, que era suscetível a erros, agendamentos duplicados e não oferecia uma visão clara da disponibilidade dos recursos[cite: 13, 14, 263].

[cite\_start]O foco da solução é fornecer uma ferramenta **estável, rápida e intuitiva** para a equipe interna, principalmente para a recepção, que realiza um alto volume de agendamentos diários e simultâneos[cite: 265].

[cite\_start]**Importante:** Este sistema é de **uso exclusivo da equipe da clínica** (recepcionistas, veterinários e gestores) e não possui portal de acesso para os clientes finais[cite: 18, 68].

-----

## 🚀 Principais Funcionalidades (MVP)

O escopo inicial do projeto (MVP) foi definido para atender às necessidades mais críticas da clínica:

  * [cite\_start]🔐 **Autenticação de Usuários (UC01):** Sistema de login seguro com perfis de acesso (recepcionista, veterinário, administrador)[cite: 27, 91].
  * [cite\_start]👥 **Gestão de Clientes e Pets (UC02):** Cadastro, consulta, edição e exclusão de tutores e seus animais de estimação, centralizando as informações[cite: 92].
  * [cite\_start]🗓️ **Visualização da Agenda por Sala (UC03):** O grande diferencial do sistema, uma grade de horários organizada por salas, com modos de visualização por dia e semana, permitindo ver em tempo real a ocupação[cite: 30, 43, 93].
  * [cite\_start]✅ **Realizar Agendamento (UC04):** Fluxo simples para marcar novas consultas, validando conflitos de horário e disponibilidade de sala para evitar sobreposições[cite: 29, 94, 97].
  * [cite\_start]🚫 **Bloqueio de Horários (UC05):** Funcionalidade para bloquear datas, horários ou salas inteiras, impedindo novos agendamentos em casos de manutenção ou indisponibilidade[cite: 48, 94].
  * [cite\_start]📢 **Geração de Texto para Notificação:** O sistema gera um texto-ticket padronizado para que a equipe envie manualmente a confirmação via WhatsApp, mantendo um contato pessoal com o cliente[cite: 95, 268].
  * [cite\_start]📊 **Relatórios Gerenciais (UC07):** Geração de relatórios para análise de atendimentos e ocupação das salas[cite: 32, 33, 34].
  * [cite\_start]🐾 **Histórico do Pet (UC08):** Acesso rápido ao histórico de agendamentos de cada animal[cite: 34].

-----

## 🏛️ Arquitetura e Princípios de Design

Este projeto foi guiado por premissas essenciais definidas junto ao cliente para garantir a aderência à realidade da clínica:

1.  **Estabilidade em Primeiro Lugar:** A prioridade máxima é um sistema que "não pode cair". [cite\_start]As decisões técnicas favoreceram a estabilidade e a simplicidade para garantir a continuidade da operação[cite: 265].
2.  [cite\_start]**Segurança Contra Erros:** Toda ação de exclusão exige uma **confirmação em duas etapas**, minimizando o risco de perda acidental de dados[cite: 266].
3.  **Comunicação Controlada e Humanizada:** O sistema **não envia mensagens automáticas** via WhatsApp. [cite\_start]Em vez disso, gera um "ticket" de texto padronizado para que a recepção possa copiar, colar e enviar manualmente, mantendo um contato pessoal com o cliente[cite: 268].
4.  [cite\_start]**Foco na Usabilidade da Recepção:** A interface foi pensada para a persona da recepcionista, que precisa de máxima agilidade para realizar tarefas repetitivas em um ambiente com múltiplos atendimentos simultâneos[cite: 26, 265].

-----

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia |
| :--- | :--- |
| **Front-End** | [cite\_start]`HTML5`, `CSS3`, `JavaScript` [cite: 131] |
| **Back-End** | [cite\_start]`Python`, `Flask` [cite: 126] |
| **Banco de Dados** | [cite\_start]`PostgreSQL` [cite: 121] |
| **Versionamento** | [cite\_start]`Git`, `GitHub` [cite: 124] |
| **Gerenciamento** | `Trello` |
| **Prototipagem** | [cite\_start]`Figma` [cite: 117] |

-----

## 🏁 Como Executar o Projeto (Guia Rápido)

Para configurar e rodar o ambiente de desenvolvimento localmente, siga estes passos:

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/trickGit/Agenda-Vet.git
    ```

2.  **Configuração do Back-end (Python/Flask):**

      * Navegue até a pasta do projeto back-end.
      * Crie e ative um ambiente virtual (`venv`).
      * Instale as dependências: `pip install -r requirements.txt`.
      * Configure as variáveis de ambiente (ex: em um arquivo `.env`), incluindo as credenciais do banco de dados PostgreSQL.
      * Execute a aplicação Flask.

3.  **Configuração do Front-end:**

      * Navegue até a pasta `prototipo-vta`.
      * Abra o arquivo `1. login_vta.html` em seu navegador de preferência ou utilize um servidor local (como o Live Server do VSCode).

4.  **Acesso ao Sistema:**

      * Após iniciar ambos os ambientes, o sistema estará acessível. Utilize as credenciais de teste para o primeiro acesso.

-----

## 👥 Equipe do Projeto

| Integrante | Papel |
| :--- | :--- |
| **Augusto Azambuya M. da Silva** | [cite\_start]Desenvolvedor Back-end [cite: 4] |
| **Lucas Ramos Alves** | [cite\_start]Communicator [cite: 5] |
| **Mateus Franceschet Pereira** | [cite\_start]Desenvolvedor Front-end [cite: 6] |
| **Patrick Vargas Santos** | [cite\_start]Desenvolvedor Full-Stack [cite: 7] |
| **Roger Luiz do Nascimento Vesely** | [cite\_start]Scrum Master [cite: 8] |
