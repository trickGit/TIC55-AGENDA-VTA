# routes.py CORRIGIDO

from flask import request, jsonify, session, render_template, redirect, url_for
import psycopg2
import psycopg2.extras # Importante para o cursor como dicionário
from werkzeug.security import check_password_hash
import os

# Importa a instância 'app' do arquivo app.py
from app import app

# --- Configuração da Conexão com o Banco de Dados ---
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def get_db_connection():
    """Cria e retorna uma nova conexão com o banco de dados."""
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn

# --- ROTAS DE PÁGINAS E AUTENTICAÇÃO ---

# Rota para a página de Login (GET)
@app.route('/')
def login_page():
    return render_template('1. login_vta.html')

# Rota para processar o formulário de login (POST)
@app.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data.get('email')
    senha = data.get('password')

    if not email or not senha:
        return jsonify({"message": "Email e senha são obrigatórios!"}), 400

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute("SELECT id, email, senha_hash, perfil FROM usuarios WHERE email = %s", (email,))
        user = cur.fetchone()
        
        cur.close()

        if user and check_password_hash(user['senha_hash'], senha):
            session['user_id'] = user['id']
            session['user_perfil'] = user['perfil']
            
            # Responde ao front-end com a URL de redirecionamento
            return jsonify({
                "message": "Login bem-sucedido! Redirecionando...", 
                "redirect_url": url_for('dashboard')
            }), 200
        else:
            return jsonify({"message": "Email/usuário ou senha incorretos."}), 401

    except Exception as e:
        print(f"Erro no login: {e}")
        return jsonify({"message": "Erro interno no servidor."}), 500
    finally:
        if conn:
            conn.close()

# Rota de Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

# --- ROTAS PROTEGIDAS (EXIGEM LOGIN) ---

# Rota do Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    # Renderiza o arquivo HTML do dashboard
    return render_template('2. dashboard_vta.html')

# Rota da Agenda
@app.route('/agenda')
def agenda_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    # Renderiza o arquivo HTML da agenda
    return render_template('3. agenda_vta.html')

# Nova rota para Agendamento (Novo / Editar)
@app.route('/agendamento')
def agendamento_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('4. agendamento_vta.html')

# Rota dos Pets
@app.route('/pets')
def pets_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('6. pets_vta.html')

# Nova rota para Clientes
@app.route('/clientes')
def clientes_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('5. clientes_vta.html')

# Nova rota para Salas
@app.route('/salas')
def salas_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('8. salas_vta.html')

# Rota para Relatórios ADM
@app.route('/relatorios')
def relatorios_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('9. relatorios_dashboard.html')

# Nova rota para Relatórios Pets
@app.route('/relatorios/pets')
def relatorios_pets():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('10. relatorios_pets.html')
# Adicione aqui outras rotas para as demais páginas (clientes, pets, etc.)
# seguindo o mesmo modelo.