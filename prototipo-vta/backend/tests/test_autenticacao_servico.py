import os
import sys
import pytest
from datetime import datetime, timedelta, timezone
import psycopg2
import psycopg2.extras

# Adiciona o caminho para importar módulos corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.models.usuario import Usuario
from backend.enums.status_usuario import StatusUsuario
from backend.enums.perfil_usuario import PerfilUsuario
from backend.services.autenticacao_servico import AutenticacaoServico

# ---------------------------------------------------------------------------
# FIXTURES DE BANCO E SERVIÇO
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def conn_str():
    # Banco de teste separado para não interferir em produção
    return "dbname='agendavta' user='postgres' password='Amcmta2007!' host='localhost' port='5432'"

@pytest.fixture(scope="module")
def conn(conn_str):
    conn = psycopg2.connect(conn_str, cursor_factory=psycopg2.extras.RealDictCursor)
    conn.set_client_encoding('UTF8')  # 🔥 força encoding correto
    yield conn
    conn.close()

@pytest.fixture(scope="function", autouse=True)
def limpar_banco(conn):
    """Limpa as tabelas relevantes antes de cada teste."""
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE TokenRecuperacao, Usuario RESTART IDENTITY CASCADE;")
        conn.commit()


@pytest.fixture
def servico(conn_str):
    return AutenticacaoServico(conn_str)


@pytest.fixture
def usuario_ativo(conn):
    senha_hash = Usuario.hash_senha("senha123")
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Usuario (nome, email, perfil, status, senhaHash)
            VALUES (%s, %s, %s, TRUE, %s)
            RETURNING idUsuario, email;
        """, ("Augusto", "augusto@email.com", "ADMIN", senha_hash))
        usuario = cur.fetchone()
        conn.commit()
        return usuario


@pytest.fixture
def usuario_inativo(conn):
    senha_hash = Usuario.hash_senha("senha123")
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Usuario (nome, email, perfil, status, senhaHash)
            VALUES (%s, %s, %s, FALSE, %s)
            RETURNING idUsuario, email;
        """, ("Inativo", "inativo@email.com", "RECEPCIONISTA", senha_hash))
        usuario = cur.fetchone()
        conn.commit()
        return usuario


# ---------------------------------------------------------------------------
# TESTES DE LOGIN
# ---------------------------------------------------------------------------
def test_login_sucesso(servico, usuario_ativo):
    usuario = servico.sessao_login(usuario_ativo["email"], "senha123")
    assert usuario is not None
    assert usuario.email == usuario_ativo["email"]


def test_login_falha_email_incorreto(servico):
    assert servico.sessao_login("naoexiste@email.com", "senha123") is None


def test_login_falha_senha_errada(servico, usuario_ativo):
    assert servico.sessao_login(usuario_ativo["email"], "senhaErrada") is None


def test_login_usuario_inativo(servico, usuario_inativo):
    assert servico.sessao_login(usuario_inativo["email"], "senha123") is None


# ---------------------------------------------------------------------------
# TESTES DE RECUPERAÇÃO E REDEFINIÇÃO
# ---------------------------------------------------------------------------
def test_recuperacao_token_gerado(servico, usuario_ativo, conn):
    token = servico.solicitar_recuperacao_senha(usuario_ativo["email"])
    assert token is not None

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM TokenRecuperacao WHERE token = %s;", (token,))
        meta = cur.fetchone()
        assert meta is not None
        assert meta["fk_usuario_idusuario"] == usuario_ativo["idusuario"]


def test_recuperacao_email_inexistente(servico):
    assert servico.solicitar_recuperacao_senha("fake@email.com") is None


def test_redefinir_senha_sucesso(servico, usuario_ativo, conn):
    token = servico.solicitar_recuperacao_senha(usuario_ativo["email"])
    sucesso = servico.redefinir_senha(token, "novaSenha123")
    assert sucesso is True

    # Verifica se senha foi atualizada
    with conn.cursor() as cur:
        cur.execute("SELECT senhaHash FROM Usuario WHERE email = %s;", (usuario_ativo["email"],))
        hash_novo = cur.fetchone()["senhahash"]
        assert Usuario.validar_senha(hash_novo, "novaSenha123")


def test_redefinir_senha_token_invalido(servico):
    assert servico.redefinir_senha("tokenfake", "nova") is False


def test_redefinir_senha_token_expirado(servico, usuario_ativo, conn):
    token = servico.solicitar_recuperacao_senha(usuario_ativo["email"])

    # Expira o token manualmente
    with conn.cursor() as cur:
        cur.execute("UPDATE TokenRecuperacao SET expiraEm = %s WHERE token = %s;",
                    (datetime.now(timezone.utc) - timedelta(minutes=1), token))
        conn.commit()

    assert servico.redefinir_senha(token, "nova") is False


def test_redefinir_senha_token_ja_usado(servico, usuario_ativo):
    token = servico.solicitar_recuperacao_senha(usuario_ativo["email"])
    assert servico.redefinir_senha(token, "nova1")
    assert servico.redefinir_senha(token, "nova2") is False