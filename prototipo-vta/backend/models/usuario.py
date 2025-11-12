# Importações necessárias
import os  # Para funções do sistema operacional, usado para gerar salt aleatório
import hashlib  # Para funções de hash criptográfico
import hmac  # Para comparação segura de strings
from enum import Enum  # Para criar enumerações
from datetime import datetime  # Para registrar último login
from uuid import uuid4  # Para gerar UUIDs únicos

# Enumeração dos tipos de perfis de usuário disponíveis no sistema
class PerfilUsuario(Enum):
    ADMIN = "admin"  # Perfil com acesso total
    RECEPCIONISTA = "recepcionista"  # Perfil com acesso intermediário
    VETERINARIO = "veterinario"  # Perfil com acesso limitado

# Enumeração dos status possíveis para um usuário
class StatusUsuario(Enum):
    ATIVO = "ativo"  # Usuário ativo
    INATIVO = "inativo"  # Usuário inativo

class Usuario:
    # Permissões padrão usadas como fallback quando um perfil não está no mapa
    # Esta constante é um frozenset vazio, tornando-a imutável e compartilhada entre todas as instâncias da classe.
    PERMISSOES_PADRAO = frozenset()  # nenhum acesso por padrão

    # Mapa que define as permissões específicas para cada tipo de perfil
    PERMISSOES_POR_PERFIL = {
        PerfilUsuario.ADMIN: {"visualizar", "criar", "editar", "excluir"},  # Todas as permissões
        PerfilUsuario.RECEPCIONISTA: {"visualizar", "criar"},  # Permissões básicas
        PerfilUsuario.VETERINARIO: {"visualizar"},  # Apenas visualização
    }

    # Construtor da classe Usuario
    def __init__(self, uuid: int, nome: str, email: str, senha_hash: str, perfil: PerfilUsuario = PerfilUsuario.RECEPCIONISTA, status: StatusUsuario = StatusUsuario.ATIVO, ultimo_login: datetime | None = None) -> None:
        self.uuid = uuid if uuid is not None else str(uuid4())
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.perfil = perfil
        self.status = status
        self.ultimo_login = ultimo_login  # datetime ou None

    # Representação em string do objeto Usuario
    def __repr__(self) -> str:
        ult = self.ultimo_login.isoformat() if isinstance(self.ultimo_login, datetime) else None
        return f"Usuario(id={self.id!r}, nome={self.nome!r}, email={self.email!r}, status={self.status.value!r}, ultimo_login={ult!r})"

    # Static method para gerar hash de senha usando PBKDF2 e um salt aleatório
    @staticmethod
    def hash_senha(senha: str, iterations: int = 100_000) -> str:
        salt = os.urandom(16)  # Gera um salt aleatório de 16 bytes
        dk = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, iterations)
        return f"{iterations}${salt.hex()}${dk.hex()}"

    # Static method para verificar se uma senha corresponde ao hash armazenado
   
    @staticmethod
    def validar_senha(stored, senha) -> bool:
        # Se o hash ou senha forem inválidos, retorna False
        if not isinstance(stored, str) or not isinstance(senha, str):
            return False

        try:
            # Converte bytes para string, se necessário
            if isinstance(stored, bytes):
                stored = stored.decode("utf-8", errors="ignore")

            # Formato PBKDF2
            if "$" in stored:
                iterations_str, salt_hex, dk_hex = stored.split("$", 2)
                iterations = int(iterations_str)
                salt = bytes.fromhex(salt_hex)
                dk_stored = bytes.fromhex(dk_hex)
                dk_new = hashlib.pbkdf2_hmac("sha256", senha.encode(), salt, iterations)
                return hmac.compare_digest(dk_new, dk_stored)

            # Formato SHA256 antigo
            return hmac.compare_digest(hashlib.sha256(senha.encode()).hexdigest(), stored)

        except Exception:
            return False

    # Instance method para autenticar o usuário (verifica também se está ativo)
    def autenticar(self, senha: str) -> bool:
        if not self.is_ativo():
            return False
        return Usuario.verify_senha(self.senha_hash, senha)

    # Verifica se o usuário está ativo
    def is_ativo(self) -> bool:
        return self.status == StatusUsuario.ATIVO

    # Ativa o usuário
    def ativar(self) -> None:
        self.status = StatusUsuario.ATIVO

    # Desativa o usuário
    def desativar(self) -> None:
        self.status = StatusUsuario.INATIVO

    # Define explicitamente o status (aceita apenas StatusUsuario)
    def set_status(self, status: StatusUsuario) -> None:
        if not isinstance(status, StatusUsuario):
            raise ValueError("status deve ser uma instância de StatusUsuario")
        self.status = status
    
    # Registra o último login (usa UTC atual se data_hora for None)
    def registrar_ultimologin(self, data_hora: datetime | None = None) -> None:
        if data_hora is None:
            data_hora = datetime.utcnow()
        if not isinstance(data_hora, datetime):
            raise ValueError("data_hora deve ser um datetime ou None")
        self.ultimo_login = data_hora

    # Retorna o último login (datetime ou None)
    def get_ultimo_login(self) -> datetime | None:
        return self.ultimo_login
    
    # Instance method para verificar se o usuário tem permissão para executar uma ação
    def pode(self, acao) -> bool:
        # Usuários inativos nunca têm permissão
        if not self.is_ativo():
            return False

        # A ação deve ser string não vazia
        if not isinstance(acao, str):
            return False
        acao_limpa = acao.strip().lower()
        if not acao_limpa:
            return False

        # Admin tem todas as permissões
        if self.perfil == PerfilUsuario.ADMIN:
            return True

        # Permissões do perfil
        permissoes = self.PERMISSOES_POR_PERFIL.get(self.perfil, self.PERMISSOES_PADRAO)
        return acao_limpa in permissoes