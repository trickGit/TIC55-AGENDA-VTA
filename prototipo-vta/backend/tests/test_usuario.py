"""
Testes para a classe Usuario
pytest test_usuario.py -v
"""

import pytest
from datetime import datetime, timezone, timedelta
from uuid import UUID
import hashlib

# Importações (ajuste os paths conforme sua estrutura)
import sys
sys.path.insert(0, '/mnt/user-data/outputs')

from backend.models.usuario import Usuario
from backend.enums.perfil_usuario import PerfilUsuario
from backend.enums.status_usuario import StatusUsuario


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def usuario_valido():
    """Cria um usuário válido para testes."""
    senha_hash = Usuario.hash_senha("senha123")
    return Usuario(
        nome="João Silva",
        email="joao@example.com",
        senha_hash=senha_hash,
        perfil=PerfilUsuario.VETERINARIO,
        status=StatusUsuario.ATIVO
    )


@pytest.fixture
def usuario_admin():
    """Cria um usuário admin para testes."""
    senha_hash = Usuario.hash_senha("admin123")
    return Usuario(
        nome="Admin Sistema",
        email="admin@example.com",
        senha_hash=senha_hash,
        perfil=PerfilUsuario.ADMIN,
        status=StatusUsuario.ATIVO
    )


@pytest.fixture
def usuario_inativo():
    """Cria um usuário inativo para testes."""
    senha_hash = Usuario.hash_senha("senha123")
    return Usuario(
        nome="Usuario Inativo",
        email="inativo@example.com",
        senha_hash=senha_hash,
        perfil=PerfilUsuario.RECEPCIONISTA,
        status=StatusUsuario.INATIVO
    )


# ============================================================================
# TESTES DO CONSTRUTOR
# ============================================================================

class TestUsuarioConstructor:
    """Testes do construtor da classe Usuario."""
    
    def test_criar_usuario_valido(self):
        """Deve criar usuário com dados válidos."""
        senha_hash = Usuario.hash_senha("senha123")
        usuario = Usuario(
            nome="Maria Santos",
            email="maria@example.com",
            senha_hash=senha_hash
        )
        
        assert usuario.nome == "Maria Santos"
        assert usuario.email == "maria@example.com"
        assert usuario.senha_hash == senha_hash
        assert usuario.perfil == PerfilUsuario.RECEPCIONISTA  # padrão
        assert usuario.status == StatusUsuario.ATIVO  # padrão
        assert usuario.uuid is not None
        assert usuario.ultimo_login is None
    
    def test_email_normalizado_lowercase(self):
        """Deve converter email para lowercase."""
        senha_hash = Usuario.hash_senha("senha123")
        usuario = Usuario(
            nome="Teste",
            email="TESTE@EXAMPLE.COM",
            senha_hash=senha_hash
        )
        
        assert usuario.email == "teste@example.com"
    
    def test_nome_com_espacos_extras(self):
        """Deve remover espaços extras do nome."""
        senha_hash = Usuario.hash_senha("senha123")
        usuario = Usuario(
            nome="  João  Silva  ",
            email="joao@example.com",
            senha_hash=senha_hash
        )
        
        assert usuario.nome == "João Silva"
    
    def test_uuid_customizado(self):
        """Deve aceitar UUID customizado."""
        senha_hash = Usuario.hash_senha("senha123")
        uuid_custom = "123e4567-e89b-12d3-a456-426614174000"
        
        usuario = Usuario(
            nome="Teste",
            email="teste@example.com",
            senha_hash=senha_hash,
            uuid=uuid_custom
        )
        
        assert usuario.uuid == uuid_custom
    
    def test_uuid_objeto_uuid(self):
        """Deve aceitar objeto UUID."""
        senha_hash = Usuario.hash_senha("senha123")
        uuid_obj = UUID("123e4567-e89b-12d3-a456-426614174000")
        
        usuario = Usuario(
            nome="Teste",
            email="teste@example.com",
            senha_hash=senha_hash,
            uuid=uuid_obj
        )
        
        assert usuario.uuid == str(uuid_obj)
    
    def test_erro_nome_vazio(self):
        """Deve falhar com nome vazio."""
        senha_hash = Usuario.hash_senha("senha123")
        
        with pytest.raises(ValueError, match="Nome não pode ser vazio"):
            Usuario(
                nome="",
                email="teste@example.com",
                senha_hash=senha_hash
            )
    
    def test_erro_nome_apenas_espacos(self):
        """Deve falhar com nome apenas espaços."""
        senha_hash = Usuario.hash_senha("senha123")
        
        with pytest.raises(ValueError, match="Nome não pode ser vazio"):
            Usuario(
                nome="   ",
                email="teste@example.com",
                senha_hash=senha_hash
            )
    
    def test_erro_email_invalido(self):
        """Deve falhar com email inválido."""
        senha_hash = Usuario.hash_senha("senha123")
        
        with pytest.raises(ValueError, match="Email inválido"):
            Usuario(
                nome="Teste",
                email="email_invalido",
                senha_hash=senha_hash
            )
    
    def test_erro_email_vazio(self):
        """Deve falhar com email vazio."""
        senha_hash = Usuario.hash_senha("senha123")
        
        with pytest.raises(ValueError, match="Email inválido"):
            Usuario(
                nome="Teste",
                email="",
                senha_hash=senha_hash
            )
    
    def test_erro_senha_hash_vazia(self):
        """Deve falhar com senha_hash vazia."""
        with pytest.raises(ValueError, match="Hash de senha não pode ser vazio"):
            Usuario(
                nome="Teste",
                email="teste@example.com",
                senha_hash=""
            )
    
    def test_erro_perfil_invalido(self):
        """Deve falhar com perfil inválido."""
        senha_hash = Usuario.hash_senha("senha123")
        
        with pytest.raises(ValueError, match="Perfil deve ser uma instância"):
            Usuario(
                nome="Teste",
                email="teste@example.com",
                senha_hash=senha_hash,
                perfil="ADMIN"  # string em vez de enum
            )
    
    def test_erro_status_invalido(self):
        """Deve falhar com status inválido."""
        senha_hash = Usuario.hash_senha("senha123")
        
        with pytest.raises(ValueError, match="Status deve ser uma instância"):
            Usuario(
                nome="Teste",
                email="teste@example.com",
                senha_hash=senha_hash,
                status="ATIVO"  # string em vez de enum
            )
    
    def test_erro_ultimo_login_invalido(self):
        """Deve falhar com ultimo_login inválido."""
        senha_hash = Usuario.hash_senha("senha123")
        
        with pytest.raises(ValueError, match="ultimo_login deve ser datetime"):
            Usuario(
                nome="Teste",
                email="teste@example.com",
                senha_hash=senha_hash,
                ultimo_login="2025-01-01"  # string em vez de datetime
            )


# ============================================================================
# TESTES DE HASH DE SENHA
# ============================================================================

class TestHashSenha:
    """Testes do método hash_senha."""
    
    def test_hash_senha_gera_string(self):
        """Deve gerar string de hash."""
        hash_result = Usuario.hash_senha("senha123")
        
        assert isinstance(hash_result, str)
        assert len(hash_result) > 0
    
    def test_hash_senha_formato_correto(self):
        """Deve gerar hash no formato iterations$salt$hash."""
        hash_result = Usuario.hash_senha("senha123")
        
        partes = hash_result.split("$")
        assert len(partes) == 3
        assert partes[0] == "600000"  # iterations
        assert len(partes[1]) == 32  # salt (16 bytes = 32 hex)
        assert len(partes[2]) == 64  # hash (32 bytes = 64 hex)
    
    def test_hash_senha_deterministico_com_salt(self):
        """Deve gerar hashes diferentes para mesma senha (salt aleatório)."""
        hash1 = Usuario.hash_senha("senha123")
        hash2 = Usuario.hash_senha("senha123")
        
        assert hash1 != hash2  # Salts diferentes
    
    def test_hash_senha_iterations_customizado(self):
        """Deve aceitar número de iterações customizado."""
        hash_result = Usuario.hash_senha("senha123", iterations=100_000)
        
        partes = hash_result.split("$")
        assert partes[0] == "100000"
    
    def test_erro_senha_vazia(self):
        """Deve falhar com senha vazia."""
        with pytest.raises(ValueError, match="Senha não pode ser vazia"):
            Usuario.hash_senha("")
    
    def test_erro_senha_apenas_espacos(self):
        """Deve falhar com senha apenas espaços."""
        with pytest.raises(ValueError, match="Senha não pode ser vazia"):
            Usuario.hash_senha("   ")
    
    def test_erro_iterations_muito_baixo(self):
        """Deve falhar com iterações muito baixas."""
        with pytest.raises(ValueError, match="Número de iterações muito baixo"):
            Usuario.hash_senha("senha123", iterations=50_000)


# ============================================================================
# TESTES DE VALIDAÇÃO DE SENHA
# ============================================================================

class TestValidarSenha:
    """Testes do método validar_senha."""
    
    def test_validar_senha_correta(self):
        """Deve validar senha correta."""
        senha = "minha_senha_123"
        hash_senha = Usuario.hash_senha(senha)
        
        assert Usuario.validar_senha(hash_senha, senha) is True
    
    def test_validar_senha_incorreta(self):
        """Deve rejeitar senha incorreta."""
        hash_senha = Usuario.hash_senha("senha_correta")
        
        assert Usuario.validar_senha(hash_senha, "senha_errada") is False
    
    def test_validar_senha_case_sensitive(self):
        """Deve ser case-sensitive."""
        hash_senha = Usuario.hash_senha("Senha123")
        
        assert Usuario.validar_senha(hash_senha, "senha123") is False
        assert Usuario.validar_senha(hash_senha, "SENHA123") is False
    
    def test_validar_senha_hash_invalido(self):
        """Deve retornar False para hash inválido."""
        assert Usuario.validar_senha("hash_invalido", "senha") is False
    
    def test_validar_senha_hash_vazio(self):
        """Deve retornar False para hash vazio."""
        assert Usuario.validar_senha("", "senha") is False
    
    def test_validar_senha_senha_vazia(self):
        """Deve retornar False para senha vazia."""
        hash_senha = Usuario.hash_senha("senha")
        assert Usuario.validar_senha(hash_senha, "") is False
    
    def test_validar_senha_tipos_invalidos(self):
        """Deve retornar False para tipos inválidos."""
        assert Usuario.validar_senha(None, "senha") is False
        assert Usuario.validar_senha("hash", None) is False
        assert Usuario.validar_senha(123, "senha") is False


# ============================================================================
# TESTES DE STATUS
# ============================================================================

class TestStatusMethods:
    """Testes dos métodos relacionados a status."""
    
    def test_is_ativo_retorna_true_para_ativo(self, usuario_valido):
        """Deve retornar True para usuário ativo."""
        assert usuario_valido.is_ativo() is True
    
    def test_is_ativo_retorna_false_para_inativo(self, usuario_inativo):
        """Deve retornar False para usuário inativo."""
        assert usuario_inativo.is_ativo() is False
    
    def test_ativar_usuario(self, usuario_inativo):
        """Deve ativar usuário."""
        usuario_inativo.ativar()
        assert usuario_inativo.status == StatusUsuario.ATIVO
        assert usuario_inativo.is_ativo() is True
    
    def test_desativar_usuario(self, usuario_valido):
        """Deve desativar usuário."""
        usuario_valido.desativar()
        assert usuario_valido.status == StatusUsuario.INATIVO
        assert usuario_valido.is_ativo() is False
    
    def test_set_status_valido(self, usuario_valido):
        """Deve definir status válido."""
        usuario_valido.set_status(StatusUsuario.INATIVO)
        assert usuario_valido.status == StatusUsuario.INATIVO
    
    def test_set_status_invalido(self, usuario_valido):
        """Deve falhar com status inválido."""
        with pytest.raises(ValueError, match="status deve ser uma instância"):
            usuario_valido.set_status("ATIVO")


# ============================================================================
# TESTES DE ÚLTIMO LOGIN
# ============================================================================

class TestUltimoLogin:
    """Testes dos métodos de último login."""
    
    def test_registrar_ultimo_login_sem_parametro(self, usuario_valido):
        """Deve registrar login com hora atual."""
        antes = datetime.now(timezone.utc)
        usuario_valido.registrar_ultimo_login()
        depois = datetime.now(timezone.utc)
        
        assert usuario_valido.ultimo_login is not None
        assert antes <= usuario_valido.ultimo_login <= depois
        assert usuario_valido.ultimo_login.tzinfo is not None  # Tem timezone
    
    def test_registrar_ultimo_login_com_parametro(self, usuario_valido):
        """Deve registrar login com data específica."""
        data_especifica = datetime(2025, 1, 15, 10, 30, tzinfo=timezone.utc)
        usuario_valido.registrar_ultimo_login(data_especifica)
        
        assert usuario_valido.ultimo_login == data_especifica
    
    def test_registrar_ultimo_login_adiciona_timezone(self, usuario_valido):
        """Deve adicionar timezone UTC se ausente."""
        data_sem_tz = datetime(2025, 1, 15, 10, 30)
        usuario_valido.registrar_ultimo_login(data_sem_tz)
        
        assert usuario_valido.ultimo_login.tzinfo is not None
    
    def test_get_ultimo_login(self, usuario_valido):
        """Deve retornar último login."""
        data = datetime(2025, 1, 15, 10, 30, tzinfo=timezone.utc)
        usuario_valido.registrar_ultimo_login(data)
        
        assert usuario_valido.get_ultimo_login() == data
    
    def test_get_ultimo_login_none(self, usuario_valido):
        """Deve retornar None se nunca logou."""
        assert usuario_valido.get_ultimo_login() is None
    
    def test_erro_registrar_login_tipo_invalido(self, usuario_valido):
        """Deve falhar com tipo inválido."""
        with pytest.raises(ValueError, match="data_hora deve ser datetime"):
            usuario_valido.registrar_ultimo_login("2025-01-15")


# ============================================================================
# TESTES DE PERMISSÕES
# ============================================================================

class TestPermissoes:
    """Testes do sistema de permissões."""
    
    def test_admin_pode_tudo(self, usuario_admin):
        """Admin deve ter todas as permissões."""
        assert usuario_admin.pode("visualizar") is True
        assert usuario_admin.pode("criar") is True
        assert usuario_admin.pode("editar") is True
        assert usuario_admin.pode("excluir") is True
        assert usuario_admin.pode("qualquer_coisa") is True
    
    def test_veterinario_pode_visualizar(self, usuario_valido):
        """Veterinário deve poder visualizar."""
        assert usuario_valido.pode("visualizar") is True
    
    def test_veterinario_nao_pode_editar(self, usuario_valido):
        """Veterinário não deve poder editar."""
        assert usuario_valido.pode("editar") is False
        assert usuario_valido.pode("criar") is False
        assert usuario_valido.pode("excluir") is False
    
    def test_recepcionista_permissoes(self):
        """Recepcionista deve ter permissões corretas."""
        senha_hash = Usuario.hash_senha("senha123")
        recep = Usuario(
            nome="Recepcionista",
            email="recep@example.com",
            senha_hash=senha_hash,
            perfil=PerfilUsuario.RECEPCIONISTA
        )
        
        assert recep.pode("visualizar") is True
        assert recep.pode("criar") is True
        assert recep.pode("editar") is False
        assert recep.pode("excluir") is False
    
    def test_usuario_inativo_nao_tem_permissao(self, usuario_inativo):
        """Usuário inativo não deve ter nenhuma permissão."""
        assert usuario_inativo.pode("visualizar") is False
        assert usuario_inativo.pode("criar") is False
    
    def test_pode_normaliza_acao(self, usuario_admin):
        """Deve normalizar ação (lowercase, sem espaços)."""
        assert usuario_admin.pode("  VISUALIZAR  ") is True
        assert usuario_admin.pode("ViSuAlIzAr") is True
    
    def test_pode_rejeita_acao_invalida(self, usuario_admin):
        """Deve rejeitar ação inválida."""
        assert usuario_admin.pode("") is False
        assert usuario_admin.pode("   ") is False
        assert usuario_admin.pode(None) is False
        assert usuario_admin.pode(123) is False
    
    def test_get_permissoes_admin(self, usuario_admin):
        """Deve retornar todas permissões para admin."""
        permissoes = usuario_admin.get_permissoes()
        
        assert isinstance(permissoes, frozenset)
        assert "visualizar" in permissoes
        assert "criar" in permissoes
        assert "editar" in permissoes
        assert "excluir" in permissoes
    
    def test_get_permissoes_veterinario(self, usuario_valido):
        """Deve retornar permissões do veterinário."""
        permissoes = usuario_valido.get_permissoes()
        
        assert isinstance(permissoes, frozenset)
        assert "visualizar" in permissoes
        assert "criar" not in permissoes
    
    def test_get_permissoes_inativo(self, usuario_inativo):
        """Deve retornar set vazio para inativo."""
        permissoes = usuario_inativo.get_permissoes()
        
        assert isinstance(permissoes, frozenset)
        assert len(permissoes) == 0


# ============================================================================
# TESTES DE SERIALIZAÇÃO
# ============================================================================

class TestSerializacao:
    """Testes de to_dict e from_dict."""
    
    def test_to_dict_completo(self, usuario_valido):
        """Deve converter para dicionário completo."""
        usuario_valido.registrar_ultimo_login()
        dados = usuario_valido.to_dict()
        
        assert isinstance(dados, dict)
        assert dados["uuid"] == usuario_valido.uuid
        assert dados["nome"] == usuario_valido.nome
        assert dados["email"] == usuario_valido.email
        assert dados["perfil"] == usuario_valido.perfil.value
        assert dados["status"] == usuario_valido.status.value
        assert dados["ultimo_login"] is not None
        assert "permissoes" in dados
        assert "senha_hash" not in dados  # Não deve incluir senha
    
    def test_to_dict_sem_ultimo_login(self, usuario_valido):
        """Deve funcionar sem último login."""
        dados = usuario_valido.to_dict()
        
        assert dados["ultimo_login"] is None
    
    def test_from_dict_completo(self):
        """Deve criar usuário de dicionário."""
        senha_hash = Usuario.hash_senha("senha123")
        dados = {
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "nome": "Teste Usuario",
            "email": "teste@example.com",
            "perfil": "VETERINARIO",
            "status": "ATIVO",
            "ultimo_login": "2025-01-15T10:30:00+00:00"
        }
        
        usuario = Usuario.from_dict(dados, senha_hash)
        
        assert usuario.uuid == dados["uuid"]
        assert usuario.nome == dados["nome"]
        assert usuario.email == dados["email"]
        assert usuario.perfil == PerfilUsuario.VETERINARIO
        assert usuario.status == StatusUsuario.ATIVO
        assert usuario.ultimo_login is not None


# ============================================================================
# TESTES DE MÉTODOS MÁGICOS
# ============================================================================

class TestMetodosMagicos:
    """Testes de __repr__, __eq__, __hash__."""
    
    def test_repr_legivel(self, usuario_valido):
        """Deve ter repr legível."""
        repr_str = repr(usuario_valido)
        
        assert "Usuario" in repr_str
        assert usuario_valido.uuid in repr_str
        assert usuario_valido.nome in repr_str
        assert usuario_valido.email in repr_str
    
    def test_eq_uuids_iguais(self):
        """Usuários com mesmo UUID devem ser iguais."""
        senha_hash = Usuario.hash_senha("senha123")
        uuid_comum = "123e4567-e89b-12d3-a456-426614174000"
        
        u1 = Usuario("User 1", "u1@test.com", senha_hash, uuid=uuid_comum)
        u2 = Usuario("User 2", "u2@test.com", senha_hash, uuid=uuid_comum)
        
        assert u1 == u2
    
    def test_eq_uuids_diferentes(self, usuario_valido, usuario_admin):
        """Usuários com UUIDs diferentes devem ser diferentes."""
        assert usuario_valido != usuario_admin
    
    def test_eq_tipo_diferente(self, usuario_valido):
        """Não deve ser igual a outro tipo."""
        assert usuario_valido != "string"
        assert usuario_valido != 123
        assert usuario_valido != None
    
    def test_hash_consistente(self, usuario_valido):
        """Hash deve ser consistente."""
        hash1 = hash(usuario_valido)
        hash2 = hash(usuario_valido)
        
        assert hash1 == hash2
    
    def test_hash_diferente_uuids_diferentes(self, usuario_valido, usuario_admin):
        """Usuários diferentes devem ter hashes diferentes."""
        assert hash(usuario_valido) != hash(usuario_admin)


# ============================================================================
# TESTES DE INTEGRAÇÃO
# ============================================================================

class TestIntegracao:
    """Testes de integração de múltiplas funcionalidades."""
    
    def test_fluxo_completo_usuario(self):
        """Testa fluxo completo de criação e uso de usuário."""
        # Criar usuário
        senha = "senha_super_segura_123"
        hash_senha = Usuario.hash_senha(senha)
        
        usuario = Usuario(
            nome="Teste Completo",
            email="TESTE@EXAMPLE.COM",
            senha_hash=hash_senha,
            perfil=PerfilUsuario.ADMIN
        )
        
        # Verificar criação
        assert usuario.nome == "Teste Completo"
        assert usuario.email == "teste@example.com"  # normalizado
        assert usuario.is_ativo() is True
        
        # Validar senha
        assert Usuario.validar_senha(usuario.senha_hash, senha) is True
        assert Usuario.validar_senha(usuario.senha_hash, "senha_errada") is False
        
        # Registrar login
        usuario.registrar_ultimo_login()
        assert usuario.ultimo_login is not None
        
        # Verificar permissões
        assert usuario.pode("visualizar") is True
        assert usuario.pode("excluir") is True
        
        # Desativar
        usuario.desativar()
        assert usuario.is_ativo() is False
        assert usuario.pode("visualizar") is False  # Inativo não tem permissão
        
        # Reativar
        usuario.ativar()
        assert usuario.is_ativo() is True
        assert usuario.pode("visualizar") is True
        
        # Serializar
        dados = usuario.to_dict()
        assert dados["email"] == "teste@example.com"
        assert "senha_hash" not in dados


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])