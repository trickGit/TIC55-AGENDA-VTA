import pytest
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from unittest.mock import Mock, MagicMock, patch

# Importações
from backend.services.autenticacao_servico import AutenticacaoServico
from backend.models.usuario import Usuario
from backend.enums.perfil_usuario import PerfilUsuario
from backend.enums.status_usuario import StatusUsuario


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def servico():
    """Cria instância do serviço para testes."""
    return AutenticacaoServico()


@pytest.fixture
def mock_conn():
    """Cria mock de conexão do banco."""
    conn = MagicMock()
    cursor = MagicMock()
    
    conn.__enter__ = Mock(return_value=conn)
    conn.__exit__ = Mock(return_value=False)
    cursor.__enter__ = Mock(return_value=cursor)
    cursor.__exit__ = Mock(return_value=False)
    
    conn.cursor.return_value = cursor
    
    return conn, cursor


@pytest.fixture
def usuario_dict():
    """Retorna dicionário simulando linha do banco."""
    senha_hash = Usuario.hash_senha("senha123")
    return {
        "uuid": str(uuid4()),
        "idusuario": 1,
        "nome": "João Silva",
        "email": "joao@example.com",
        "senhahash": senha_hash,
        "perfil": PerfilUsuario.VETERINARIO.value,  # FIX: Usar .value
        "status": StatusUsuario.ATIVO.value,  # FIX: Usar .value
        "ultimo_login": None
    }


# ============================================================================
# TESTES DE LOGIN
# ============================================================================

class TestSessaoLogin:
    """Testes do método sessao_login."""
    
    def test_login_sucesso(self, servico, mock_conn, usuario_dict):
        """Deve fazer login com credenciais corretas."""
        conn, cursor = mock_conn
        cursor.fetchone.return_value = usuario_dict
        
        with patch.object(servico, '_get_conn', return_value=conn):
            usuario = servico.sessao_login("joao@example.com", "senha123")
        
        assert usuario is not None
        assert usuario.nome == "João Silva"
        assert usuario.email == "joao@example.com"
        assert usuario.perfil == PerfilUsuario.VETERINARIO
        assert cursor.execute.called
    
    def test_login_email_nao_encontrado(self, servico, mock_conn):
        """Deve retornar None para email não encontrado."""
        conn, cursor = mock_conn
        cursor.fetchone.return_value = None
        
        with patch.object(servico, '_get_conn', return_value=conn):
            usuario = servico.sessao_login("inexistente@example.com", "senha123")
        
        assert usuario is None
    
    def test_login_senha_incorreta(self, servico, mock_conn, usuario_dict):
        """Deve retornar None para senha incorreta."""
        conn, cursor = mock_conn
        cursor.fetchone.return_value = usuario_dict
        
        with patch.object(servico, '_get_conn', return_value=conn):
            usuario = servico.sessao_login("joao@example.com", "senha_errada")
        
        assert usuario is None
    
    def test_login_usuario_inativo(self, servico, mock_conn, usuario_dict):
        """Deve retornar None para usuário inativo."""
        conn, cursor = mock_conn
        usuario_dict["status"] = StatusUsuario.INATIVO.value  # FIX: Usar .value
        cursor.fetchone.return_value = usuario_dict
        
        with patch.object(servico, '_get_conn', return_value=conn):
            usuario = servico.sessao_login("joao@example.com", "senha123")
        
        assert usuario is None
    
    def test_login_atualiza_ultimo_login(self, servico, mock_conn, usuario_dict):
        """Deve tentar atualizar último login."""
        conn, cursor = mock_conn
        cursor.fetchone.return_value = usuario_dict
        
        with patch.object(servico, '_get_conn', return_value=conn):
            usuario = servico.sessao_login("joao@example.com", "senha123")
        
        execute_calls = cursor.execute.call_args_list
        assert len(execute_calls) >= 2
        
        update_call = execute_calls[1][0][0]
        assert "UPDATE" in update_call.upper()
    
    def test_login_email_vazio(self, servico):
        """Deve retornar None para email vazio."""
        usuario = servico.sessao_login("", "senha123")
        assert usuario is None
    
    def test_login_senha_vazia(self, servico):
        """Deve retornar None para senha vazia."""
        usuario = servico.sessao_login("joao@example.com", "")
        assert usuario is None


# ============================================================================
# TESTES DE CRIAÇÃO DE USUÁRIO
# ============================================================================

class TestCriarUsuario:
    """Testes do método criar_usuario."""
    
    def test_criar_usuario_sucesso(self, servico, mock_conn):
        """Deve criar usuário com sucesso."""
        conn, cursor = mock_conn
        cursor.fetchone.side_effect = [
            None,
            {"idusuario": 1}
        ]
        
        with patch.object(servico, '_get_conn', return_value=conn):
            usuario = servico.criar_usuario(
                nome="Novo Usuario",
                email="novo@example.com",
                senha="senha_segura_123"
            )
        
        assert usuario is not None
        assert usuario.nome == "Novo Usuario"
        assert usuario.email == "novo@example.com"
        assert usuario.perfil == PerfilUsuario.RECEPCIONISTA
        
        execute_calls = cursor.execute.call_args_list
        insert_call = [c for c in execute_calls if "INSERT" in c[0][0].upper()]
        assert len(insert_call) == 1
    
    def test_criar_usuario_email_duplicado(self, servico, mock_conn):
        """Deve retornar None se email já existe."""
        conn, cursor = mock_conn
        cursor.fetchone.return_value = {"idusuario": 999}
        
        with patch.object(servico, '_get_conn', return_value=conn):
            usuario = servico.criar_usuario(
                nome="Teste",
                email="duplicado@example.com",
                senha="senha123"
            )
        
        assert usuario is None
    
    def test_criar_usuario_senha_curta(self, servico):
        """Deve falhar com senha muito curta."""
        with pytest.raises(ValueError, match="Senha deve ter no mínimo 8 caracteres"):
            servico.criar_usuario(
                nome="Teste",
                email="teste@example.com",
                senha="123"
            )
    
    def test_criar_usuario_dados_vazios(self, servico):
        """Deve falhar com dados vazios."""
        with pytest.raises(ValueError, match="obrigatórios"):
            servico.criar_usuario(
                nome="",
                email="teste@example.com",
                senha="senha123"
            )
    
    def test_criar_usuario_com_perfil(self, servico, mock_conn):
        """Deve criar usuário com perfil específico."""
        conn, cursor = mock_conn
        cursor.fetchone.side_effect = [None, {"idusuario": 1}]
        
        with patch.object(servico, '_get_conn', return_value=conn):
            usuario = servico.criar_usuario(
                nome="Admin",
                email="admin@example.com",
                senha="senha123",
                perfil=PerfilUsuario.ADMIN
            )
        
        assert usuario.perfil == PerfilUsuario.ADMIN


# ============================================================================
# TESTES DE ALTERAÇÃO DE SENHA
# ============================================================================

class TestAlterarSenha:
    """Testes do método alterar_senha."""
    
    def test_alterar_senha_sucesso(self, servico, mock_conn):
        """Deve alterar senha com sucesso."""
        conn, cursor = mock_conn
        senha_atual_hash = Usuario.hash_senha("senha_antiga")
        
        cursor.fetchone.return_value = {
            "idusuario": 1,
            "senhahash": senha_atual_hash
        }
        
        with patch.object(servico, '_get_conn', return_value=conn):
            sucesso = servico.alterar_senha(
                email="joao@example.com",
                senha_atual="senha_antiga",
                senha_nova="senha_nova_123"
            )
        
        assert sucesso is True
        
        execute_calls = cursor.execute.call_args_list
        update_call = [c for c in execute_calls if "UPDATE" in c[0][0].upper()]
        assert len(update_call) == 1
    
    def test_alterar_senha_usuario_nao_encontrado(self, servico, mock_conn):
        """Deve falhar se usuário não existe."""
        conn, cursor = mock_conn
        cursor.fetchone.return_value = None
        
        with patch.object(servico, '_get_conn', return_value=conn):
            sucesso = servico.alterar_senha(
                email="inexistente@example.com",
                senha_atual="senha123",
                senha_nova="nova123"
            )
        
        assert sucesso is False
    
    def test_alterar_senha_senha_atual_incorreta(self, servico, mock_conn):
        """Deve falhar se senha atual incorreta."""
        conn, cursor = mock_conn
        cursor.fetchone.return_value = {
            "idusuario": 1,
            "senhahash": Usuario.hash_senha("senha_correta")
        }
        
        with patch.object(servico, '_get_conn', return_value=conn):
            sucesso = servico.alterar_senha(
                email="joao@example.com",
                senha_atual="senha_errada",
                senha_nova="nova123"
            )
        
        assert sucesso is False
    
    def test_alterar_senha_nova_muito_curta(self, servico, mock_conn):
        """Deve falhar se nova senha muito curta."""
        conn, cursor = mock_conn
        cursor.fetchone.return_value = {
            "idusuario": 1,
            "senhahash": Usuario.hash_senha("senha_antiga")
        }
        
        with patch.object(servico, '_get_conn', return_value=conn):
            sucesso = servico.alterar_senha(
                email="joao@example.com",
                senha_atual="senha_antiga",
                senha_nova="123"
            )
        
        assert sucesso is False


# ============================================================================
# TESTES DE RECUPERAÇÃO DE SENHA
# ============================================================================

class TestRecuperacaoSenha:
    """Testes dos métodos de recuperação de senha."""
    
    def test_solicitar_recuperacao_sucesso(self, servico, mock_conn):
        """Deve gerar token de recuperação."""
        conn, cursor = mock_conn
        cursor.fetchone.return_value = {"idusuario": 1}
        
        with patch.object(servico, '_get_conn', return_value=conn):
            token = servico.solicitar_recuperacao_senha("joao@example.com")
        
        assert token is not None
        assert len(token) == 64
        
        execute_calls = cursor.execute.call_args_list
        insert_call = [c for c in execute_calls if "INSERT" in c[0][0].upper()]
        assert len(insert_call) == 1
    
    def test_solicitar_recuperacao_email_nao_encontrado(self, servico, mock_conn):
        """Deve retornar None para email não encontrado."""
        conn, cursor = mock_conn
        cursor.fetchone.return_value = None
        
        with patch.object(servico, '_get_conn', return_value=conn):
            token = servico.solicitar_recuperacao_senha("inexistente@example.com")
        
        assert token is None
    
    def test_redefinir_senha_token_valido(self, servico, mock_conn):
        """Deve redefinir senha com token válido."""
        conn, cursor = mock_conn
        
        cursor.fetchone.return_value = {
            "idtoken": 1,
            "expiraem": datetime.now(timezone.utc) + timedelta(minutes=10),
            "utilizado": False,
            "idusuario": 1
        }
        
        with patch.object(servico, '_get_conn', return_value=conn):
            sucesso = servico.redefinir_senha(
                token="token_valido_123",
                nova_senha="nova_senha_segura_123"
            )
        
        assert sucesso is True
        
        execute_calls = cursor.execute.call_args_list
        update_calls = [c for c in execute_calls if "UPDATE" in c[0][0].upper()]
        assert len(update_calls) == 2
    
    def test_redefinir_senha_token_invalido(self, servico, mock_conn):
        """Deve falhar com token inválido."""
        conn, cursor = mock_conn
        cursor.fetchone.return_value = None
        
        with patch.object(servico, '_get_conn', return_value=conn):
            sucesso = servico.redefinir_senha(
                token="token_invalido",
                nova_senha="nova_senha_123"
            )
        
        assert sucesso is False
    
    def test_redefinir_senha_token_expirado(self, servico, mock_conn):
        """Deve falhar com token expirado."""
        conn, cursor = mock_conn
        
        cursor.fetchone.return_value = {
            "idtoken": 1,
            "expiraem": datetime.now(timezone.utc) - timedelta(minutes=10),
            "utilizado": False,
            "idusuario": 1
        }
        
        with patch.object(servico, '_get_conn', return_value=conn):
            sucesso = servico.redefinir_senha(
                token="token_expirado",
                nova_senha="nova_senha_123"
            )
        
        assert sucesso is False
    
    def test_redefinir_senha_token_ja_utilizado(self, servico, mock_conn):
        """Deve falhar com token já utilizado."""
        conn, cursor = mock_conn
        
        cursor.fetchone.return_value = {
            "idtoken": 1,
            "expiraem": datetime.now(timezone.utc) + timedelta(minutes=10),
            "utilizado": True,
            "idusuario": 1
        }
        
        with patch.object(servico, '_get_conn', return_value=conn):
            sucesso = servico.redefinir_senha(
                token="token_usado",
                nova_senha="nova_senha_123"
            )
        
        assert sucesso is False
    
    def test_redefinir_senha_muito_curta(self, servico, mock_conn):
        """Deve falhar com senha muito curta."""
        conn, cursor = mock_conn
        cursor.fetchone.return_value = {
            "idtoken": 1,
            "expiraem": datetime.now(timezone.utc) + timedelta(minutes=10),
            "utilizado": False,
            "idusuario": 1
        }
        
        with patch.object(servico, '_get_conn', return_value=conn):
            sucesso = servico.redefinir_senha(
                token="token_valido",
                nova_senha="123"
            )
        
        assert sucesso is False


# ============================================================================
# TESTES DE VERIFICAÇÃO DE EMAIL
# ============================================================================

class TestVerificarEmail:
    """Testes do método verificar_email_disponivel."""
    
    def test_email_disponivel(self, servico, mock_conn):
        """Deve retornar True para email disponível."""
        conn, cursor = mock_conn
        cursor.fetchone.return_value = None
        
        with patch.object(servico, '_get_conn', return_value=conn):
            disponivel = servico.verificar_email_disponivel("novo@example.com")
        
        assert disponivel is True
    
    def test_email_ja_cadastrado(self, servico, mock_conn):
        """Deve retornar False para email já cadastrado."""
        conn, cursor = mock_conn
        cursor.fetchone.return_value = {"idusuario": 1}
        
        with patch.object(servico, '_get_conn', return_value=conn):
            disponivel = servico.verificar_email_disponivel("existe@example.com")
        
        assert disponivel is False
    
    def test_email_vazio(self, servico):
        """Deve retornar False para email vazio."""
        disponivel = servico.verificar_email_disponivel("")
        assert disponivel is False


# ============================================================================
# TESTES DE GERENCIAMENTO DE USUÁRIOS
# ============================================================================

class TestGerenciamentoUsuarios:
    """Testes dos métodos de gerenciamento."""
    
    def test_listar_usuarios_ativos(self, servico, mock_conn):
        """Deve listar apenas usuários ativos."""
        conn, cursor = mock_conn
        
        senha_hash = Usuario.hash_senha("senha123")
        cursor.fetchall.return_value = [
            {
                "uuid": str(uuid4()),
                "nome": "Usuario 1",
                "email": "u1@example.com",
                "senhahash": senha_hash,
                "perfil": PerfilUsuario.ADMIN.value,  # FIX: Usar .value
                "status": StatusUsuario.ATIVO.value,  # FIX: Usar .value
                "ultimo_login": None
            },
            {
                "uuid": str(uuid4()),
                "nome": "Usuario 2",
                "email": "u2@example.com",
                "senhahash": senha_hash,
                "perfil": PerfilUsuario.VETERINARIO.value,  # FIX: Usar .value
                "status": StatusUsuario.ATIVO.value,  # FIX: Usar .value
                "ultimo_login": None
            }
        ]
        
        with patch.object(servico, '_get_conn', return_value=conn):
            usuarios = servico.listar_usuarios_ativos()
        
        assert len(usuarios) == 2
        assert all(isinstance(u, Usuario) for u in usuarios)
        assert all(u.status == StatusUsuario.ATIVO for u in usuarios)
    
    def test_atualizar_perfil_sucesso(self, servico, mock_conn):
        """Deve atualizar perfil do usuário."""
        conn, cursor = mock_conn
        cursor.rowcount = 1
        
        with patch.object(servico, '_get_conn', return_value=conn):
            sucesso = servico.atualizar_perfil_usuario(
                email="joao@example.com",
                novo_perfil=PerfilUsuario.ADMIN
            )
        
        assert sucesso is True
    
    def test_atualizar_perfil_usuario_nao_encontrado(self, servico, mock_conn):
        """Deve retornar False se usuário não existe."""
        conn, cursor = mock_conn
        cursor.rowcount = 0
        
        with patch.object(servico, '_get_conn', return_value=conn):
            sucesso = servico.atualizar_perfil_usuario(
                email="inexistente@example.com",
                novo_perfil=PerfilUsuario.ADMIN
            )
        
        assert sucesso is False
    
    def test_desativar_usuario_sucesso(self, servico, mock_conn):
        """Deve desativar usuário."""
        conn, cursor = mock_conn
        cursor.rowcount = 1
        
        with patch.object(servico, '_get_conn', return_value=conn):
            sucesso = servico.desativar_usuario("joao@example.com")
        
        assert sucesso is True
    
    def test_reativar_usuario_sucesso(self, servico, mock_conn):
        """Deve reativar usuário."""
        conn, cursor = mock_conn
        cursor.rowcount = 1
        
        with patch.object(servico, '_get_conn', return_value=conn):
            sucesso = servico.reativar_usuario("joao@example.com")
        
        assert sucesso is True


# ============================================================================
# TESTES DE INVALIDAÇÃO DE TOKENS
# ============================================================================

class TestInvalidarTokens:
    """Testes de invalidação de tokens."""
    
    def test_invalidar_tokens_usuario(self, servico, mock_conn):
        """Deve invalidar todos os tokens de um usuário."""
        conn, cursor = mock_conn
        cursor.rowcount = 3
        
        with patch.object(servico, '_get_conn', return_value=conn):
            tokens_invalidados = servico.invalidar_tokens_usuario(usuario_id=1)
        
        assert tokens_invalidados == 3
    
    def test_limpar_tokens_expirados(self, servico, mock_conn):
        """Deve remover tokens expirados."""
        conn, cursor = mock_conn
        cursor.rowcount = 5
        
        with patch.object(servico, '_get_conn', return_value=conn):
            tokens_removidos = servico.limpar_tokens_expirados()
        
        assert tokens_removidos == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])