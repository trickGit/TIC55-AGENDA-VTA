# Testes para a classe Usuario.
# Execute com: pytest test_usuario.py -v

import pytest
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from backend.models.usuario import Usuario
from backend.enums.perfil_usuario import PerfilUsuario
from backend.enums.status_usuario import StatusUsuario


class TestUsuarioInstanciacao:
    # Testes de criação e inicialização de usuários.
    
    def test_criar_usuario_completo(self):
        # Testa criação de usuário com todos os parâmetros.
        uuid = str(uuid4())
        senha_hash = Usuario.hash_senha("senha123")
        ultimo_login = datetime.now(timezone.utc)
        
        usuario = Usuario(
            uuid=uuid,
            nome="João Silva",
            email="joao@example.com",
            senha_hash=senha_hash,
            perfil=PerfilUsuario.ADMIN,
            status=StatusUsuario.ATIVO,
            ultimo_login=ultimo_login
        )
        
        assert usuario.uuid == uuid
        assert usuario.nome == "João Silva"
        assert usuario.email == "joao@example.com"
        assert usuario.senha_hash == senha_hash
        assert usuario.perfil == PerfilUsuario.ADMIN
        assert usuario.status == StatusUsuario.ATIVO
        assert usuario.ultimo_login == ultimo_login
    
    def test_criar_usuario_minimo(self):
        # Testa criação com parâmetros mínimos (valores padrão).
        senha_hash = Usuario.hash_senha("senha123")
        
        usuario = Usuario(
            uuid=None,
            nome="Maria",
            email="maria@example.com",
            senha_hash=senha_hash
        )
        
        assert usuario.uuid is not None
        assert len(usuario.uuid) == 36  # UUID formato padrão
        assert usuario.perfil == PerfilUsuario.RECEPCIONISTA
        assert usuario.status == StatusUsuario.ATIVO
        assert usuario.ultimo_login is None
    
    def test_nome_normalizado(self):
        # Testa que nome é normalizado (strip).
        senha_hash = Usuario.hash_senha("senha123")
        
        usuario = Usuario(
            uuid=None,
            nome="  João Silva  ",
            email="joao@example.com",
            senha_hash=senha_hash
        )
        
        assert usuario.nome == "João Silva"
    
    def test_email_normalizado(self):
        # Testa que email é convertido para lowercase.
        senha_hash = Usuario.hash_senha("senha123")
        
        usuario = Usuario(
            uuid=None,
            nome="João",
            email="JOAO@EXAMPLE.COM",
            senha_hash=senha_hash
        )
        
        assert usuario.email == "joao@example.com"
    
    def test_erro_nome_vazio(self):
        # Testa que nome vazio gera erro.
        senha_hash = Usuario.hash_senha("senha123")
        
        with pytest.raises(ValueError, match="Nome não pode ser vazio"):
            Usuario(
                uuid=None,
                nome="   ",
                email="joao@example.com",
                senha_hash=senha_hash
            )
    
    def test_erro_email_invalido(self):
        # Testa que email sem @ gera erro.
        senha_hash = Usuario.hash_senha("senha123")
        
        with pytest.raises(ValueError, match="Email inválido"):
            Usuario(
                uuid=None,
                nome="João",
                email="emailinvalido",
                senha_hash=senha_hash
            )
    
    def test_erro_senha_hash_vazio(self):
        # Testa que senha_hash vazio gera erro.
        with pytest.raises(ValueError, match="Hash de senha não pode ser vazio"):
            Usuario(
                uuid=None,
                nome="João",
                email="joao@example.com",
                senha_hash=""
            )
    
    def test_conversao_ultimo_login_string(self):
        # Testa conversão de string ISO para datetime.
        senha_hash = Usuario.hash_senha("senha123")
        data_str = "2024-11-10T10:30:00"
        
        usuario = Usuario(
            uuid=None,
            nome="João",
            email="joao@example.com",
            senha_hash=senha_hash,
            ultimo_login=data_str
        )
        
        assert isinstance(usuario.ultimo_login, datetime)
        assert usuario.ultimo_login.year == 2024
        assert usuario.ultimo_login.month == 11
        assert usuario.ultimo_login.day == 10
    
    def test_conversao_ultimo_login_string_invalida(self):
        # Testa que string inválida resulta em None.
        senha_hash = Usuario.hash_senha("senha123")
        
        usuario = Usuario(
            uuid=None,
            nome="João",
            email="joao@example.com",
            senha_hash=senha_hash,
            ultimo_login="data-invalida"
        )
        
        assert usuario.ultimo_login is None


class TestHashSenha:
    # Testes de hash e validação de senhas.
    
    def test_hash_senha_gera_string(self):
        # Testa que hash_senha retorna string no formato correto.
        hash_result = Usuario.hash_senha("minha_senha")
        
        assert isinstance(hash_result, str)
        assert "$" in hash_result
        
        # Formato: iterations$salt$hash
        partes = hash_result.split("$")
        assert len(partes) == 3
        assert partes[0].isdigit()  # iterations
        assert len(partes[1]) == 32  # salt hex (16 bytes = 32 chars)
        assert len(partes[2]) == 64  # hash hex (32 bytes = 64 chars)
    
    def test_hash_senha_usa_iterations_customizado(self):
        # Testa que aceita número customizado de iterações.
        hash_result = Usuario.hash_senha("senha", iterations=100_000)
        iterations = int(hash_result.split("$")[0])
        
        assert iterations == 100_000
    
    def test_hash_senha_diferente_para_mesma_senha(self):
        # Testa que mesmo senha gera hashes diferentes (salt aleatório).
        hash1 = Usuario.hash_senha("senha123")
        hash2 = Usuario.hash_senha("senha123")
        
        assert hash1 != hash2
    
    def test_hash_senha_vazia_gera_erro(self):
        # Testa que senha vazia gera erro.
        with pytest.raises(ValueError, match="Senha não pode ser vazia"):
            Usuario.hash_senha("")
    
    def test_validar_senha_correta(self):
        # Testa validação de senha correta.
        senha = "senha_secreta_123"
        hash_stored = Usuario.hash_senha(senha)
        
        assert Usuario.validar_senha(hash_stored, senha) is True
    
    def test_validar_senha_incorreta(self):
        # Testa validação de senha incorreta.
        hash_stored = Usuario.hash_senha("senha_correta")
        
        assert Usuario.validar_senha(hash_stored, "senha_errada") is False
    
    def test_validar_senha_formato_legado_sha256(self):
        # Testa suporte a formato SHA256 antigo.
        import hashlib
        senha = "senha123"
        hash_legado = hashlib.sha256(senha.encode()).hexdigest()
        
        assert Usuario.validar_senha(hash_legado, senha) is True
        assert Usuario.validar_senha(hash_legado, "outra") is False
    
    def test_validar_senha_hash_invalido(self):
        # Testa que hash inválido retorna False.
        assert Usuario.validar_senha("hash_invalido", "senha") is False
        assert Usuario.validar_senha("", "senha") is False
        assert Usuario.validar_senha(None, "senha") is False
    
    def test_validar_senha_formato_incorreto(self):
        # Testa hash com formato incorreto.
        # Formato com apenas 2 partes ao invés de 3
        hash_invalido = "100000$abc123"
        assert Usuario.validar_senha(hash_invalido, "senha") is False


class TestAutenticacao:
    # Testes de autenticação de usuários.
    
    def test_autenticar_usuario_ativo_senha_correta(self):
        # Testa autenticação bem-sucedida.
        senha = "senha_secreta"
        usuario = Usuario(
            uuid=None,
            nome="João",
            email="joao@example.com",
            senha_hash=Usuario.hash_senha(senha),
            status=StatusUsuario.ATIVO
        )
        
        assert usuario.autenticar(senha) is True
    
    def test_autenticar_usuario_ativo_senha_incorreta(self):
        # Testa autenticação com senha errada.
        usuario = Usuario(
            uuid=None,
            nome="João",
            email="joao@example.com",
            senha_hash=Usuario.hash_senha("senha_correta"),
            status=StatusUsuario.ATIVO
        )
        
        assert usuario.autenticar("senha_errada") is False
    
    def test_autenticar_usuario_inativo(self):
        # Testa que usuário inativo não autentica.
        senha = "senha123"
        usuario = Usuario(
            uuid=None,
            nome="João",
            email="joao@example.com",
            senha_hash=Usuario.hash_senha(senha),
            status=StatusUsuario.INATIVO
        )
        
        assert usuario.autenticar(senha) is False


class TestStatusUsuario:
    # Testes de gerenciamento de status.
    
    def test_is_ativo_usuario_ativo(self):
        # Testa verificação de usuário ativo.
        usuario = Usuario(
            uuid=None,
            nome="João",
            email="joao@example.com",
            senha_hash=Usuario.hash_senha("senha"),
            status=StatusUsuario.ATIVO
        )
        
        assert usuario.is_ativo() is True
    
    def test_is_ativo_usuario_inativo(self):
        # Testa verificação de usuário inativo.
        usuario = Usuario(
            uuid=None,
            nome="João",
            email="joao@example.com",
            senha_hash=Usuario.hash_senha("senha"),
            status=StatusUsuario.INATIVO
        )
        
        assert usuario.is_ativo() is False
    
    def test_ativar_usuario(self):
        # Testa ativação de usuário.
        usuario = Usuario(
            uuid=None,
            nome="João",
            email="joao@example.com",
            senha_hash=Usuario.hash_senha("senha"),
            status=StatusUsuario.INATIVO
        )
        
        usuario.ativar()
        assert usuario.status == StatusUsuario.ATIVO
        assert usuario.is_ativo() is True
    
    def test_desativar_usuario(self):
        # Testa desativação de usuário.
        usuario = Usuario(
            uuid=None,
            nome="João",
            email="joao@example.com",
            senha_hash=Usuario.hash_senha("senha"),
            status=StatusUsuario.ATIVO
        )
        
        usuario.desativar()
        assert usuario.status == StatusUsuario.INATIVO
        assert usuario.is_ativo() is False
    
    def test_set_status_valido(self):
        # Testa definição de status explícito.
        usuario = Usuario(
            uuid=None,
            nome="João",
            email="joao@example.com",
            senha_hash=Usuario.hash_senha("senha")
        )
        
        usuario.set_status(StatusUsuario.INATIVO)
        assert usuario.status == StatusUsuario.INATIVO
    
    def test_set_status_invalido(self):
        # Testa que tipo inválido gera erro.
        usuario = Usuario(
            uuid=None,
            nome="João",
            email="joao@example.com",
            senha_hash=Usuario.hash_senha("senha")
        )
        
        with pytest.raises(ValueError, match="deve ser uma instância de StatusUsuario"):
            usuario.set_status("ATIVO")  # String ao invés de enum


class TestUltimoLogin:
    # Testes de registro de último login.
    
    def test_registrar_ultimo_login_com_data(self):
        # Testa registro de login com data específica.
        usuario = Usuario(
            uuid=None,
            nome="João",
            email="joao@example.com",
            senha_hash=Usuario.hash_senha("senha")
        )
        
        data_login = datetime(2024, 11, 10, 10, 30, 0, tzinfo=timezone.utc)
        usuario.registrar_ultimo_login(data_login)
        
        assert usuario.ultimo_login == data_login
    
    def test_registrar_ultimo_login_sem_data(self):
        # Testa registro de login usando data atual (UTC).
        usuario = Usuario(
            uuid=None,
            nome="João",
            email="joao@example.com",
            senha_hash=Usuario.hash_senha("senha")
        )
        
        antes = datetime.now(timezone.utc)
        usuario.registrar_ultimo_login()
        depois = datetime.now(timezone.utc)
        
        assert usuario.ultimo_login is not None
        assert antes <= usuario.ultimo_login <= depois
    
    def test_registrar_ultimo_login_tipo_invalido(self):
        # Testa que tipo inválido gera erro.
        usuario = Usuario(
            uuid=None,
            nome="João",
            email="joao@example.com",
            senha_hash=Usuario.hash_senha("senha")
        )
        
        with pytest.raises(ValueError, match="deve ser um datetime ou None"):
            usuario.registrar_ultimo_login("2024-11-10")
    
    def test_get_ultimo_login(self):
        # Testa recuperação do último login.
        usuario = Usuario(
            uuid=None,
            nome="João",
            email="joao@example.com",
            senha_hash=Usuario.hash_senha("senha")
        )
        
        assert usuario.get_ultimo_login() is None
        
        data_login = datetime.now(timezone.utc)
        usuario.registrar_ultimo_login(data_login)
        
        assert usuario.get_ultimo_login() == data_login


class TestPermissoes:
    # Testes de sistema de permissões.
    
    def test_admin_tem_todas_permissoes(self):
        # Testa que admin tem todas as permissões.
        usuario = Usuario(
            uuid=None,
            nome="Admin",
            email="admin@example.com",
            senha_hash=Usuario.hash_senha("senha"),
            perfil=PerfilUsuario.ADMIN
        )
        
        assert usuario.pode("visualizar") is True
        assert usuario.pode("criar") is True
        assert usuario.pode("editar") is True
        assert usuario.pode("excluir") is True
        assert usuario.pode("qualquer_coisa") is True
    
    def test_recepcionista_permissoes(self):
        # Testa permissões de recepcionista.
        usuario = Usuario(
            uuid=None,
            nome="Recepcionista",
            email="recepcao@example.com",
            senha_hash=Usuario.hash_senha("senha"),
            perfil=PerfilUsuario.RECEPCIONISTA
        )
        
        assert usuario.pode("visualizar") is True
        assert usuario.pode("criar") is True
        assert usuario.pode("editar") is False
        assert usuario.pode("excluir") is False
    
    def test_veterinario_permissoes(self):
        # Testa permissões de veterinário.
        usuario = Usuario(
            uuid=None,
            nome="Dr. Silva",
            email="vet@example.com",
            senha_hash=Usuario.hash_senha("senha"),
            perfil=PerfilUsuario.VETERINARIO
        )
        
        assert usuario.pode("visualizar") is True
        assert usuario.pode("criar") is False
        assert usuario.pode("editar") is False
        assert usuario.pode("excluir") is False
    
    def test_usuario_inativo_sem_permissoes(self):
        # Testa que usuário inativo não tem permissões.
        usuario = Usuario(
            uuid=None,
            nome="Admin",
            email="admin@example.com",
            senha_hash=Usuario.hash_senha("senha"),
            perfil=PerfilUsuario.ADMIN,
            status=StatusUsuario.INATIVO
        )
        
        assert usuario.pode("visualizar") is False
        assert usuario.pode("criar") is False
    
    def test_pode_normaliza_acao(self):
        # Testa que ações são normalizadas (lowercase, strip).
        usuario = Usuario(
            uuid=None,
            nome="Recepcionista",
            email="recepcao@example.com",
            senha_hash=Usuario.hash_senha("senha"),
            perfil=PerfilUsuario.RECEPCIONISTA
        )
        
        assert usuario.pode("  VISUALIZAR  ") is True
        assert usuario.pode("Criar") is True
        assert usuario.pode("EDITAR") is False
    
    def test_pode_acao_vazia(self):
        # Testa que ação vazia retorna False.
        usuario = Usuario(
            uuid=None,
            nome="Admin",
            email="admin@example.com",
            senha_hash=Usuario.hash_senha("senha"),
            perfil=PerfilUsuario.ADMIN
        )
        
        assert usuario.pode("") is False
        assert usuario.pode("   ") is False
    
    def test_pode_acao_tipo_invalido(self):
        # Testa que tipo inválido retorna False.
        usuario = Usuario(
            uuid=None,
            nome="Admin",
            email="admin@example.com",
            senha_hash=Usuario.hash_senha("senha"),
            perfil=PerfilUsuario.ADMIN
        )
        
        assert usuario.pode(None) is False
        assert usuario.pode(123) is False
        assert usuario.pode([]) is False


class TestRepr:
    # Testes de representação string.
    
    def test_repr_completo(self):
        # Testa representação __repr__ com todos os dados.
        uuid = str(uuid4())
        data_login = datetime(2024, 11, 10, 10, 30, 0, tzinfo=timezone.utc)
        
        usuario = Usuario(
            uuid=uuid,
            nome="João Silva",
            email="joao@example.com",
            senha_hash=Usuario.hash_senha("senha"),
            perfil=PerfilUsuario.ADMIN,
            status=StatusUsuario.ATIVO,
            ultimo_login=data_login
        )
        
        repr_str = repr(usuario)
        
        assert "Usuario(" in repr_str
        assert f"uuid={uuid!r}" in repr_str
        assert "nome='João Silva'" in repr_str
        assert "email='joao@example.com'" in repr_str
        assert "status='ativo'" in repr_str
        assert "2024-11-10T10:30:00" in repr_str
    
    def test_repr_sem_ultimo_login(self):
        # Testa representação sem último login.
        usuario = Usuario(
            uuid=None,
            nome="João",
            email="joao@example.com",
            senha_hash=Usuario.hash_senha("senha"))