from flask import request, jsonify, session
import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash
import os

# Importa o objeto 'app' que foi criado no arquivo app.py
from app import app

# Configurações de conexão com o banco de dados a partir das variáveis de ambiente
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def get_db_connection():
    """Cria e retorna uma nova conexão com o banco de dados."""
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# --- Rota de Login ---
@app.route('/login', methods=['POST'])
def login():
    """Processa a tentativa de login do usuário."""
    # Usamos request.form porque o front-end está enviando como 'FormData'
    data = request.form
    email = data.get('email')
    senha = data.get('password')

    if not email or not senha:
        return jsonify({"message": "Email e senha são obrigatórios!"}), 400

    conn = None
    try:
        conn = get_db_connection()
        # Usamos um cursor como dicionário para facilitar o acesso às colunas pelo nome
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute("SELECT id, email, senha_hash, perfil FROM usuarios WHERE email = %s", (email,))
        user = cur.fetchone()
        
        cur.close()

        # user[2] ou user['senha_hash']
        if user and check_password_hash(user['senha_hash'], senha):
            session['user_id'] = user['id']
            session['user_perfil'] = user['perfil']
            
            return jsonify({"message": "Login bem-sucedido!", "redirect_url": "/dashboard"}), 200
        else:
            return jsonify({"message": "Credenciais inválidas!"}), 401

    except Exception as e:
        print(f"Erro no login: {e}")
        return jsonify({"message": "Erro interno no servidor."}), 500
    finally:
        if conn:
            conn.close()

# --- Rota de Logout ---
@app.route('/logout', methods=['POST'])
def logout():
    session.clear() # Limpa toda a sessão
    return jsonify({"message": "Logout bem-sucedido!"}), 200

# --- Rota Protegida de Exemplo ---
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return f"<h1>Bem-vindo ao Dashboard!</h1><p>Seu ID: {session['user_id']}, Perfil: {session['user_perfil']}</p>"
    else:
        # No futuro, aqui você faria um redirect para a tela de login
        return jsonify({"message": "Acesso não autorizado! Faça login."}), 401