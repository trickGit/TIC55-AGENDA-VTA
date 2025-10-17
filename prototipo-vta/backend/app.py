from flask import Flask, g, jsonify
import os
import psycopg2
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Cria a instância principal da aplicação
app = Flask(__name__)

# Configura uma chave secreta para a sessão. Essencial para segurança!
# Puxa do arquivo .env ou usa um valor padrão se não encontrar
app.secret_key = os.getenv("SECRET_KEY", "uma-chave-secreta-padrao-para-testes")

# --- Configuração da Conexão com o Banco de Dados ---
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def get_db():
    """
    Abre uma nova conexão com o banco de dados se não houver uma na requisição atual.
    """
    if 'db' not in g:
        g.db = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    """
    Fecha a conexão com o banco de dados ao final da requisição.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

# --- Rotas da Aplicação ---

# Adiciona um endpoint de health check para verificar a conexão com o DB
@app.route('/health')
def health_check():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close()
        return jsonify({"status": "ok", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "error", "database": "disconnected", "error": str(e)}), 500

# Importa as rotas DEPOIS de criar o 'app' para evitar importação circular
from routes import *

# --- Ponto de entrada para rodar o servidor ---
if __name__ == '__main__':
    # O modo debug reinicia o servidor automaticamente a cada alteração
    app.run(debug=True, port=5000)