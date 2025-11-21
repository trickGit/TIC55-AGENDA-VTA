import os
import hashlib
import hmac
import re
from datetime import datetime, timezone
from uuid import uuid4, UUID
from backend.enums.perfil_usuario import PerfilUsuario
from backend.enums.status_usuario import StatusUsuario

class Usuario:
    """
    Representa um usuário do sistema com autenticação e controle de permissões.
    
    Attributes:
        uuid: Identificador único do usuário
        nome: Nome completo
        email: Email (normalizado para lowercase)
        senha_hash: Hash da senha (formato: iterations$salt$hash)
        perfil: Perfil do usuário (define permissões)
        status: Status do usuário (ativo/inativo)
        ultimo_login: Timestamp do último login (UTC)
    """
    
    # Permissões padrão (nenhuma por padrão)
    PERMISSOES_PADRAO = frozenset()

    # Mapa de permissões por perfil
    PERMISSOES_POR_PERFIL = {
        PerfilUsuario.ADMIN: frozenset({"visualizar", "criar", "editar", "excluir"}),
        PerfilUsuario.RECEPCIONISTA: frozenset({"visualizar", "criar"}),
        PerfilUsuario.VETERINARIO: frozenset({"visualizar"}),
    }

    # Padrão de validação de email (básico mas mais robusto)
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    def __init__(self, nome: str, email: str, telefone: int, senha_hash: str, usuario_id: UUID | None = None, perfil: PerfilUsuario = PerfilUsuario.RECEPCIONISTA, status: StatusUsuario = StatusUsuario.ATIVO, ultimo_login: datetime | None = None) -> None:
        """
        Inicializa um novo usuário.
        
        Args:
            nome: Nome do usuário (não pode ser vazio)
            email: Email válido
            senha_hash: Hash da senha já processado
            uuid: UUID do usuário (gerado automaticamente se None)
            perfil: Perfil de permissões
            status: Status inicial
            ultimo_login: Timestamp do último login (UTC)
            
        Raises:
            ValueError: Se dados inválidos forem fornecidos
        """
        # Validações
        if not nome or not nome.strip():
            raise ValueError("Nome não pode ser vazio")
        
        email = email.strip().lower() if email else ""
        if not self._validar_email(email):
            raise ValueError(f"Email inválido: {email}")
        
        if not senha_hash or not senha_hash.strip():
            raise ValueError("Hash de senha não pode ser vazio")
        
        if not isinstance(perfil, PerfilUsuario):
            raise ValueError("Perfil deve ser uma instância de PerfilUsuario")
        
        if not isinstance(status, StatusUsuario):
            raise ValueError("Status deve ser uma instância de StatusUsuario")
        
        if ultimo_login is not None and not isinstance(ultimo_login, datetime):
            raise ValueError("ultimo_login deve ser datetime ou None")
        
        # Atribuições
        self.usuario_id = str(usuario_id) if usuario_id is not None else str(uuid4())
        self.nome = ' '.join(nome.strip().split())
        self.email = email
        self.telefone = telefone  
        self.senha_hash = senha_hash.strip()
        self.perfil = perfil
        self.status = status
        self.ultimo_login = ultimo_login

    @classmethod
    def _validar_email(cls, email: str) -> bool:
        """Valida formato do email."""
        return bool(email and cls.EMAIL_REGEX.match(email))

    def __repr__(self) -> str:
        """Representação em string do usuário."""
        ult = self.ultimo_login.isoformat() if self.ultimo_login else None
        return (
            f"Usuario(uuid={self.uuid!r}, nome={self.nome!r}, "
            f"email={self.email!r}, perfil={self.perfil.value!r}, "
            f"status={self.status.value!r}, ultimo_login={ult!r})"
        )

    def __eq__(self, other) -> bool:
        """Compara usuários pelo UUID."""
        if not isinstance(other, Usuario):
            return False
        return self.uuid == other.uuid

    def __hash__(self) -> int:
        """Hash baseado no UUID."""
        return hash(self.uuid)

    @staticmethod
    def hash_senha(senha: str, iterations: int = 600_000) -> str:
        """
        Gera hash seguro da senha usando PBKDF2-HMAC-SHA256.
        
        Args:
            senha: Senha em texto plano
            iterations: Número de iterações (mínimo 600.000 recomendado pela OWASP)
            
        Returns:
            Hash no formato: iterations$salt_hex$hash_hex
            
        Raises:
            ValueError: Se senha for vazia ou iterations < 100.000
        """
        if not senha or not senha.strip():
            raise ValueError("Senha não pode ser vazia")
        
        if iterations < 100_000:
            raise ValueError("Número de iterações muito baixo (mínimo: 100.000)")
        
        salt = os.urandom(16)
        dk = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, iterations)
        return f"{iterations}${salt.hex()}${dk.hex()}"

    @staticmethod
    def validar_senha(senha_hash: str, senha: str) -> bool:
        """
        Valida se a senha corresponde ao hash armazenado.
        
        Suporta dois formatos:
        - PBKDF2 (atual): iterations$salt$hash
        - SHA256 (legacy): hash_simples (INSEGURO - apenas para migração)
        
        Args:
            senha_hash: Hash armazenado
            senha: Senha em texto plano para validar
            
        Returns:
            True se a senha está correta, False caso contrário
        """
        if not isinstance(senha_hash, str) or not isinstance(senha, str):
            return False

        if not senha_hash or not senha:
            return False

        try:
            # Formato PBKDF2 (atual)
            if "$" in senha_hash:
                partes = senha_hash.split("$", 2)
                if len(partes) != 3:
                    return False
                
                iterations_str, salt_hex, dk_hex = partes
                iterations = int(iterations_str)
                salt = bytes.fromhex(salt_hex)
                dk_stored = bytes.fromhex(dk_hex)
                
                dk_new = hashlib.pbkdf2_hmac(
                    "sha256", 
                    senha.encode("utf-8"), 
                    salt, 
                    iterations
                )
                return hmac.compare_digest(dk_new, dk_stored)

            # Formato SHA256 antigo (INSEGURO - apenas para migração de dados legados)
            # TODO: Remover após migração completa
            hash_simples = hashlib.sha256(senha.encode("utf-8")).hexdigest()
            return hmac.compare_digest(senha_hash, hash_simples)

        except (ValueError, TypeError, AttributeError):
            return False

    # Métodos de Status

    def is_ativo(self) -> bool:
        """Verifica se o usuário está ativo."""
        return self.status == StatusUsuario.ATIVO

    def ativar(self) -> None:
        """Ativa o usuário."""
        self.status = StatusUsuario.ATIVO

    def desativar(self) -> None:
        """Desativa o usuário."""
        self.status = StatusUsuario.INATIVO

    def set_status(self, status: StatusUsuario) -> None:
        """
        Define o status do usuário.
        
        Args:
            status: Novo status
            
        Raises:
            ValueError: Se status não for instância de StatusUsuario
        """
        if not isinstance(status, StatusUsuario):
            raise ValueError("status deve ser uma instância de StatusUsuario")
        self.status = status

    # Métodos de Login

    def registrar_ultimo_login(self, data_hora: datetime | None = None) -> None:
        """
        Registra o timestamp do último login.
        
        Args:
            data_hora: Timestamp do login (UTC atual se None)
            
        Raises:
            ValueError: Se data_hora não for datetime ou None
        """
        if data_hora is None:
            data_hora = datetime.now(timezone.utc)
        
        if not isinstance(data_hora, datetime):
            raise ValueError("data_hora deve ser datetime ou None")
        
        # Garante timezone UTC
        if data_hora.tzinfo is None:
            data_hora = data_hora.replace(tzinfo=timezone.utc)
        
        self.ultimo_login = data_hora

    def get_ultimo_login(self) -> datetime | None:
        """Retorna o timestamp do último login."""
        return self.ultimo_login

    # Sistema de Permissões

    def pode(self, acao: str) -> bool:
        """
        Verifica se o usuário tem permissão para executar uma ação.
        
        Args:
            acao: Nome da ação (visualizar, criar, editar, excluir)
            
        Returns:
            True se o usuário tem permissão, False caso contrário
            
        Notes:
            - Usuários inativos nunca têm permissão
            - Admin tem todas as permissões
            - Ação é normalizada (lowercase, sem espaços)
        """
        # Usuários inativos não têm permissão
        if not self.is_ativo():
            return False

        # Validação da ação
        if not isinstance(acao, str):
            return False
        
        acao_limpa = acao.strip().lower()
        if not acao_limpa:
            return False

        # Admin tem acesso total
        if self.perfil == PerfilUsuario.ADMIN:
            return True

        # Verifica permissões do perfil
        permissoes = self.PERMISSOES_POR_PERFIL.get(
            self.perfil, 
            self.PERMISSOES_PADRAO
        )
        return acao_limpa in permissoes

    def get_permissoes(self) -> frozenset[str]:
        """
        Retorna todas as permissões do usuário.
        
        Returns:
            Set imutável de permissões
        """
        if not self.is_ativo():
            return frozenset()
        
        if self.perfil == PerfilUsuario.ADMIN:
            return frozenset({"visualizar", "criar", "editar", "excluir"})
        
        return self.PERMISSOES_POR_PERFIL.get(
            self.perfil, 
            self.PERMISSOES_PADRAO
        )

    # Métodos de Serialização

    def to_dict(self) -> dict:
        """
        Converte o usuário para dicionário.
        
        Returns:
            Dicionário com todos os dados do usuário (sem senha_hash)
        """
        return {
            "usuario_id": self.usuario_id,
            "nome": self.nome,
            "email": self.email,
            "perfil": self.perfil.value,
            "status": self.status.value,
            "ultimo_login": self.ultimo_login.isoformat() if self.ultimo_login else None,
            "permissoes": list(self.get_permissoes())
        }

    @classmethod
    def from_dict(cls, data: dict, senha_hash: str) -> "Usuario":
        """
        Cria usuário a partir de dicionário.
        
        Args:
            data: Dicionário com dados do usuário
            senha_hash: Hash da senha (não incluído no dict por segurança)
            
        Returns:
            Nova instância de Usuario
        """
        ultimo_login = None
        if data.get("ultimo_login"):
            ultimo_login = datetime.fromisoformat(data["ultimo_login"])
        
        # CORREÇÃO 2: Tratar perfil como string (busca por nome ou valor)
        perfil_valor = data.get("perfil", PerfilUsuario.RECEPCIONISTA.value)
        if isinstance(perfil_valor, str):
            try:
                # Tenta pelo valor primeiro
                perfil = PerfilUsuario(perfil_valor)
            except ValueError:
                # Se falhar, tenta pelo nome (ex: "VETERINARIO")
                try:
                    perfil = PerfilUsuario[perfil_valor]
                except KeyError:
                    perfil = PerfilUsuario.RECEPCIONISTA
        else:
            perfil = perfil_valor
        
        status_valor = data.get("status", StatusUsuario.ATIVO.value)
        if isinstance(status_valor, str):
            try:
                # Tenta pelo valor primeiro
                status = StatusUsuario(status_valor)
            except ValueError:
                # Se falhar, tenta pelo nome (ex: "ATIVO")
                try:
                    status = StatusUsuario[status_valor]
                except KeyError:
                    status = StatusUsuario.ATIVO
        else:
            status = status_valor
        
        return cls(
            usuario_id=data.get("usuario_id"),
            nome=data["nome"],
            email=data["email"],
            senha_hash=senha_hash,
            perfil=perfil,
            status=status,
            ultimo_login=ultimo_login
        )