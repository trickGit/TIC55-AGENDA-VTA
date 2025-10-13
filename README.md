

# Agenda VTA - Sistema de Agendamento para Clínica Veterinária

## Sobre o Projeto

O **Agenda VTA** é uma plataforma web desenvolvida para otimizar a gestão de agendamentos e o uso das salas de atendimento na clínica veterinária **Vet Assistance**. O projeto nasceu da necessidade de substituir o controle manual por planilhas de Excel, um processo suscetível a erros como duplicidade de horários e dificuldades para visualizar espaços ocupados.

O foco da solução é fornecer uma ferramenta **estável, rápida e intuitiva** para a equipe interna da clínica (recepcionistas, veterinários e gestores), que realiza um alto volume de agendamentos diários.

**Importante:** Este sistema é de **uso exclusivo da equipe da clínica** e não possui um portal de acesso para os clientes finais.

-----

## 🚀 Principais Funcionalidades (MVP)

O escopo do projeto foi definido para atender às necessidades mais críticas da clínica, incluindo:

  * 🔐 **Autenticação de Usuários (UC01):** Sistema de login seguro com perfis de acesso e permissões (administrador, recepcionista, veterinário).
  * 👥 **Gestão de Clientes e Pets (UC02):** Cadastro, consulta, edição e exclusão de tutores e seus animais de estimação, centralizando as informações.
  * 🗓️ **Visualização da Agenda por Sala (UC03):** O grande diferencial do sistema. Uma grade de horários organizada por salas, permitindo visualizar em tempo real a ocupação com modos de visualização por dia e semana.
  * ✅ **Realizar Agendamento (UC04):** Fluxo simplificado para marcar novas consultas, validando conflitos de horário para evitar sobreposições.
  * 🚫 **Bloqueio de Horários e Salas (UC05):** Funcionalidade para bloquear datas, horários ou salas inteiras em casos de manutenção ou indisponibilidade.
  * 📊 **Dashboard e Relatórios (UC07):** Painel com estatísticas rápidas e geração de relatórios gerenciais para análise de atendimentos e ocupação.
  * 🐾 **Histórico do Pet (UC08):** Acesso rápido ao histórico de agendamentos e atendimentos de cada animal.

-----

## 🏛️ Arquitetura e Princípios de Design

O projeto foi guiado por premissas essenciais para garantir a aderência à realidade da clínica:

1.  **Estabilidade em Primeiro Lugar:** A prioridade máxima é um sistema confiável. As decisões técnicas favoreceram a estabilidade e a simplicidade para garantir a continuidade da operação.
2.  **Segurança Contra Erros:** Ações críticas, como a exclusão de dados, exigem confirmação para minimizar o risco de perda acidental de informações.
3.  **Comunicação Controlada:** O sistema gera um "ticket" de texto padronizado para que a recepção possa copiar e enviar manualmente as confirmações via WhatsApp, mantendo um contato pessoal com o cliente.
4.  **Foco na Usabilidade da Recepção:** A interface foi desenhada para ser ágil e intuitiva, otimizando a rotina da equipe que lida com múltiplos atendimentos simultâneos.

-----

## 🛠️ Tecnologias Utilizadas

| Categoria      | Tecnologia                   |
| :------------- | :--------------------------- |
| **Front-End** | `HTML5`, `CSS3`, `JavaScript`|
| **Back-End** | `Python`, `Flask`            |
| **Banco de Dados**| `PostgreSQL`                 |
| **Versionamento**| `Git`, `GitHub`              |
| **Prototipagem** | `Figma`                      |

-----

## 🏁 Como Executar o Projeto (Guia Rápido)

Para configurar e rodar o ambiente de desenvolvimento localmente, siga estes passos:

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/trickGit/tic55-agenda-vta.git
    cd tic55-agenda-vta
    ```

2.  **Configuração do Back-end (Python/Flask):**

      * Navegue até a pasta do back-end:
        ```bash
        cd prototipo-vta/backend
        ```
      * Crie e ative um ambiente virtual.
          * No Windows:
            ```bash
            python -m venv venv
            .\venv\Scripts\activate
            ```
          * No macOS/Linux:
            ```bash
            python3 -m venv venv
            source venv/bin/activate
            ```
      * Instale as dependências do projeto:
        ```bash
        pip install -r requirements.txt
        ```
      * Configure as variáveis de ambiente. Crie um arquivo chamado `.env` na pasta `backend` e adicione as credenciais do seu banco de dados PostgreSQL, seguindo o exemplo:
        ```env
        SECRET_KEY="sua-chave-secreta-aqui"
        DB_HOST="localhost"
        DB_NAME="vta_agenda"
        DB_USER="vta_user"
        DB_PASS="sua-senha-do-banco"
        ```
      * Execute a aplicação Flask:
        ```bash
        flask run
        ```
      * O back-end estará rodando em `http://127.0.0.1:5000`.

3.  **Acesso ao Sistema:**

      * Após iniciar o back-end, abra seu navegador e acesse `http://127.0.0.1:5000`.
      * Você será direcionado para a página de login. Utilize as credenciais de teste para o primeiro acesso.

-----

## 👥 Equipe do Projeto

| Integrante                      | Papel                  |
| :------------------------------ | :--------------------- |
| **Augusto Azambuya M. da Silva**| Desenvolvedor Back-end |
| **Lucas Ramos Alves** | Communicator           |
| **Mateus Franceschet Pereira** | Desenvolvedor Front-end|
| **Patrick Vargas Santos** | Desenvolvedor Full-Stack|
| **Roger Luiz do Nascimento Vesely**| Scrum Master           |