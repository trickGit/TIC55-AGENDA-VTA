
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
4.  **Foco na Usabilidade da Recepção:** A interface foi pensada para a persona da recepcionista, que precisa de máxima agilidade para realizar tarefas repetitivas em um ambiente com múltiplos atendimentos simultâneos.

-----

## 🛠️ Tecnologias Utilizadas

| Categoria      | Tecnologia                               |
| :------------- | :--------------------------------------- |
| **Front-End** | `HTML5`, `CSS3`, `JavaScript`            |
| **Back-End** | `Python`, `Flask`                        |
| **Banco de Dados** | `PostgreSQL`                             |
| **Versionamento** | `Git`, `GitHub`                          |
| **Gerenciamento** | `Trello`                                 |

-----

## 🚀 Como Executar o Protótipo (Ambiente Local)

Para configurar e rodar o ambiente de desenvolvimento localmente, siga estes passos:

### Pré-requisitos

* **Git** instalado para clonar o repositório.
* **Visual Studio Code** (ou outro editor de código).
* Extensão **Live Server** no VS Code (recomendado para o front-end).

### 1. Clonar o repositório

```bash
git clone [https://github.com/trickGit/tic55-agenda-vta.git](https://github.com/trickGit/tic55-agenda-vta.git)
cd tic55-agenda-vta
````

### 2\. Executando o Front-end (Protótipo HTML)

O front-end é composto por arquivos HTML estáticos que podem ser abertos diretamente no navegador, mas o uso de um servidor local é recomendado para evitar problemas de CORS no futuro.

1.  Abra a pasta do projeto (`tic55-agenda-vta`) no Visual Studio Code.
2.  Caso não tenha, instale a extensão **Live Server** de Ritwick Dey.
3.  Navegue até a pasta `prototipo-vta`.
4.  Clique com o botão direito no arquivo `1. login_vta.html`.
5.  Selecione a opção **"Open with Live Server"**.
6.  O seu navegador abrirá automaticamente com a tela de login do protótipo funcional.

### 3\. Executando o Back-end (Python/Flask)

As instruções abaixo servem como guia para quando a implementação do back-end estiver disponível no repositório.

1.  **Navegue até a pasta do back-end:**
    ```bash
    # Exemplo de como seria
    cd backend-agenda-vta
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure as variáveis de ambiente** (crie um arquivo `.env` com as credenciais do banco de dados).
5.  **Execute a aplicação Flask:**
    ```bash
    flask run
    ```

-----

## 👥 Equipe do Projeto

| Integrante                      | Papel                  |
| :------------------------------ | :--------------------- |
| **Augusto Azambuya M. da Silva** | Desenvolvedor Back-end |
| **Lucas Ramos Alves** | Communicator           |
| **Mateus Franceschet Pereira** | Desenvolvedor Front-end |
| **Patrick Vargas Santos** | Desenvolvedor Full-Stack |
| **Roger Luiz do Nascimento Vesely**| Scrum Master           |

```
```
