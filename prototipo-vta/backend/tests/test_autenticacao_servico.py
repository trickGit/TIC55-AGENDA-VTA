import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from datetime import datetime, timedelta
from backend.models.usuario import Usuario, PerfilUsuario, StatusUsuario
from services.autenticacao_servico import AutenticacaoServico

@pytest.fixture
def usuario_ativo():
    senha_hash = Usuario.hash_senha("senha123")
    return Usuario(None, "Augusto", "augusto@email.com", senha_hash, PerfilUsuario.ADMIN)


@pytest.fixture
def usuario_inativo():
    senha_hash = Usuario.hash_senha("senha123")
    return Usuario(None, "Inativo", "inativo@email.com", senha_hash, PerfilUsuario.RECEPCIONISTA, StatusUsuario.INATIVO)


@pytest.fixture
def servico(usuario_ativo, usuario_inativo):
    return AutenticacaoServico([usuario_ativo, usuario_inativo])


# ---------------------------------------------------------------------------
# LOGIN
# ---------------------------------------------------------------------------
def test_login_sucesso(servico, usuario_ativo):
    usuario = servico.sessao_login(usuario_ativo.email, "senha123")
    assert usuario is not None
    assert usuario.ultimo_login is not None


def test_login_falha_email_incorreto(servico):
    assert servico.sessao_login("naoexiste@email.com", "senha123") is None


def test_login_falha_senha_errada(servico, usuario_ativo):
    assert servico.sessao_login(usuario_ativo.email, "senhaErrada") is None


def test_login_usuario_inativo(servico, usuario_inativo):
    assert servico.sessao_login(usuario_inativo.email, "senha123") is None


# ---------------------------------------------------------------------------
# RECUPERAÇÃO E REDEFINIÇÃO
# ---------------------------------------------------------------------------
def test_recuperacao_token_gerado(servico, usuario_ativo):
    token = servico.solicitar_recuperacao_senha(usuario_ativo.email)
    assert token in servico.tokens_recuperacao
    meta = servico.tokens_recuperacao[token]
    assert meta["uuid"] == usuario_ativo.uuid


def test_recuperacao_email_inexistente(servico):
    assert servico.solicitar_recuperacao_senha("fake@email.com") is None


def test_redefinir_senha_sucesso(servico, usuario_ativo):
    token = servico.solicitar_recuperacao_senha(usuario_ativo.email)
    assert servico.redefinir_senha(token, "novaSenha123") is True


def test_redefinir_senha_token_invalido(servico):
    assert servico.redefinir_senha("tokenfake", "nova") is False


def test_redefinir_senha_token_expirado(servico, usuario_ativo):
    token = servico.solicitar_recuperacao_senha(usuario_ativo.email)
    servico.tokens_recuperacao[token]["expira"] = datetime.utcnow() - timedelta(minutes=1)
    assert servico.redefinir_senha(token, "nova") is False


def test_redefinir_senha_token_ja_usado(servico, usuario_ativo):
    token = servico.solicitar_recuperacao_senha(usuario_ativo.email)
    servico.redefinir_senha(token, "nova1")
    assert servico.redefinir_senha(token, "nova2") is False