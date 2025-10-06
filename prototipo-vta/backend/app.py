from flask import Flask
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Cria a instância principal da aplicação
app = Flask(__name__)

# Configura uma chave secreta para a sessão. Essencial para segurança!
# Puxa do arquivo .env ou usa um valor padrão se não encontrar
app.secret_key = os.getenv("SECRET_KEY", "uma-chave-secreta-padrao-para-testes")

# --- Importa as rotas DEPOIS de criar o 'app' ---
# Isso evita problemas de importação circular.
from routes import *

# --- Ponto de entrada para rodar o servidor ---
if __name__ == '__main__':
    # O modo debug reinicia o servidor automaticamente a cada alteração
    app.run(debug=True, port=5000)