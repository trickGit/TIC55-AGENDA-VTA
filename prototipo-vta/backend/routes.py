from flask import request, jsonify, session, render_template, redirect, url_for
import psycopg2.extras
from werkzeug.security import check_password_hash
from functools import wraps

# Importa a instância 'app' e a função 'get_db' do app.py
from app import app, get_db

# --- DECORADOR DE AUTENTICAÇÃO ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # Se for uma requisição AJAX, retorna erro 401
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(message="Sessão expirada. Faça login novamente."), 401
            # Se for uma navegação normal, redireciona para o login
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# --- ROTAS DE PÁGINAS E AUTENTICAÇÃO ---

@app.route('/')
def login_page():
    """Exibe a página de login."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('1. login_vta.html')

@app.route('/login', methods=['POST'])
def login():
    """Processa o formulário de login."""
    data = request.form
    email = data.get('email')
    senha = data.get('password')

    if not email or not senha:
        return jsonify(message="Email e senha são obrigatórios!"), 400

    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute("SELECT id, email, senha_hash, perfil FROM usuarios WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user['senha_hash'], senha):
            session['user_id'] = user['id']
            session['user_perfil'] = user['perfil']
            
            return jsonify(
                message="Login bem-sucedido! Redirecionando...",
                redirect_url=url_for('dashboard')
            ), 200
        else:
            return jsonify(message="Email ou senha incorretos."), 401

    except Exception as e:
        print(f"Erro no login: {e}")
        return jsonify(message="Erro interno no servidor."), 500

@app.route('/logout')
def logout():
    """Limpa a sessão do usuário."""
    session.clear()
    return redirect(url_for('login_page'))

# --- ROTAS PROTEGIDAS (EXIGEM LOGIN) ---

@app.route('/dashboard')
@login_required
def dashboard():
    """Exibe o dashboard principal."""
    return render_template('2. dashboard_vta.html')

@app.route('/agenda')
@login_required
def agenda_page():
    """Exibe a página da agenda."""
    return render_template('3. agenda_vta.html')

@app.route('/agendamentos')
@login_required
def agendamentos_page():
    """Exibe a página de gerenciamento de agendamentos."""
    return render_template('4. agendamento_vta.html')

# --- API ENDPOINTS ---

@app.route('/api/agendamentos', methods=['GET'])
@login_required
def get_agendamentos():
    """Retorna uma lista de agendamentos em formato JSON."""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Query mais completa para buscar dados relacionados
        query = """
            SELECT
                a.id,
                a.data,
                a.hora,
                a.status,
                a.observacoes,
                c.nome AS cliente_nome,
                c.telefone AS cliente_telefone,
                p.nome AS pet_nome,
                p.raca AS pet_raca,
                s.nome AS servico_nome,
                v.nome AS veterinario_nome,
                sa.nome AS sala_nome
            FROM agendamentos a
            JOIN clientes c ON a.cliente_id = c.id
            JOIN pets p ON a.pet_id = p.id
            JOIN servicos s ON a.servico_id = s.id
            JOIN veterinarios v ON a.veterinario_id = v.id
            JOIN salas sa ON a.sala_id = sa.id
            ORDER BY a.data DESC, a.hora DESC;
        """
        cur.execute(query)

        agendamentos = [dict(row) for row in cur.fetchall()]
        cur.close()

        return jsonify(agendamentos)

    except Exception as e:
        print(f"Erro ao buscar agendamentos: {e}")
        return jsonify(message="Erro ao buscar dados dos agendamentos."), 500