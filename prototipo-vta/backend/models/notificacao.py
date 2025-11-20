from datetime import datetime, timezone
from uuid import uuid4, UUID
from backend.models.usuario import Usuario


class Notificacao:
    """
    Representa uma notificação do sistema para um usuário.
    
    Attributes:
        notificacao_id: Identificador único da notificação
        usuario_id: UUID do usuário que receberá a notificação
        tipo: Tipo/categoria da notificação
        titulo: Título da notificação
        mensagem: Conteúdo da mensagem
        criada_em: Timestamp de criação (UTC)
        lida: Indica se a notificação foi lida
    """
    
    # Tipos de notificação permitidos
    TIPOS_VALIDOS = frozenset({
        "info", "aviso", "erro", "sucesso", 
        "lembrete", "alerta", "sistema"
    })
    
    def __init__(self, usuario_id: UUID | str, tipo: str, titulo: str, mensagem: str,notificacao_id: UUID | str | None = None,criada_em: datetime | None = None,lida: bool = False
    ) -> None:
        """
        Inicializa uma nova notificação.
        
        Args:
            usuario_id: UUID do usuário destinatário
            tipo: Tipo da notificação (deve estar em TIPOS_VALIDOS)
            titulo: Título da notificação (não pode ser vazio)
            mensagem: Conteúdo da mensagem (não pode ser vazio)
            notificacao_id: UUID da notificação (gerado automaticamente se None)
            criada_em: Timestamp de criação (UTC atual se None)
            lida: Status de leitura (padrão: False)
            
        Raises:
            ValueError: Se dados inválidos forem fornecidos
        """
        # Validação do notificacao_id
        if notificacao_id is None:
            self.notificacao_id = str(uuid4())
        else:
            self.notificacao_id = str(notificacao_id)
        
        # Validação do usuario_id
        if usuario_id is None:
            raise ValueError("usuario_id não pode ser None")
        self.usuario_id = str(usuario_id)
        
        # Validação do tipo
        tipo = tipo.strip().lower() if isinstance(tipo, str) else ""
        if not tipo:
            raise ValueError("Tipo não pode ser vazio")
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(
                f"Tipo inválido: {tipo}. Tipos válidos: {', '.join(sorted(self.TIPOS_VALIDOS))}"
            )
        self.tipo = tipo
        
        # Validação do título
        if not titulo or not titulo.strip():
            raise ValueError("Título não pode ser vazio")
        self.titulo = titulo.strip()
        
        # Validação da mensagem
        if not mensagem or not mensagem.strip():
            raise ValueError("Mensagem não pode ser vazia")
        self.mensagem = mensagem.strip()
        
        # Validação da data de criação
        if criada_em is None:
            criada_em = datetime.now(timezone.utc)
        elif not isinstance(criada_em, datetime):
            raise ValueError("criada_em deve ser datetime ou None")
        
        # Garante timezone UTC
        if criada_em.tzinfo is None:
            criada_em = criada_em.replace(tzinfo=timezone.utc)
        self.criada_em = criada_em
        
        # Validação do status de leitura
        if not isinstance(lida, bool):
            raise ValueError("lida deve ser um booleano")
        self.lida = lida

    def __repr__(self) -> str:
        """Representação em string da notificação."""
        return (
            f"Notificacao(notificacao_id={self.notificacao_id!r}, "
            f"usuario_id={self.usuario_id!r}, tipo={self.tipo!r}, "
            f"titulo={self.titulo!r}, lida={self.lida})"
        )
    
    def __eq__(self, other) -> bool:
        """Compara notificações pelo ID."""
        if not isinstance(other, Notificacao):
            return False
        return self.notificacao_id == other.notificacao_id
    
    def __hash__(self) -> int:
        """Hash baseado no ID da notificação."""
        return hash(self.notificacao_id)
    
    # Métodos de Status de Leitura
    
    def marcar_como_lida(self) -> None:
        """Marca a notificação como lida."""
        self.lida = True
    
    def marcar_como_nao_lida(self) -> None:
        """Marca a notificação como não lida."""
        self.lida = False
    
    def is_lida(self) -> bool:
        """Verifica se a notificação foi lida."""
        return self.lida
    
    def is_nao_lida(self) -> bool:
        """Verifica se a notificação não foi lida."""
        return not self.lida
    
    # Métodos de Tipo
    
    def is_tipo(self, tipo: str) -> bool:
        """
        Verifica se a notificação é de um tipo específico.
        
        Args:
            tipo: Tipo para verificar
            
        Returns:
            True se o tipo corresponde, False caso contrário
        """
        if not isinstance(tipo, str):
            return False
        return self.tipo == tipo.strip().lower()
    
    def is_urgente(self) -> bool:
        """Verifica se a notificação é urgente (erro ou alerta)."""
        return self.tipo in {"erro", "alerta"}
    
    # Métodos de Serialização
    
    def to_dict(self) -> dict:
        """
        Converte a notificação para dicionário.
        
        Returns:
            Dicionário com todos os dados da notificação
        """
        return {
            "notificacao_id": self.notificacao_id,
            "usuario_id": self.usuario_id,
            "tipo": self.tipo,
            "titulo": self.titulo,
            "mensagem": self.mensagem,
            "criada_em": self.criada_em.isoformat(),
            "lida": self.lida
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Notificacao":
        """
        Cria notificação a partir de dicionário.
        
        Args:
            data: Dicionário com dados da notificação
            
        Returns:
            Nova instância de Notificacao
            
        Raises:
            ValueError: Se dados obrigatórios estiverem faltando
        """
        # Campos obrigatórios
        campos_obrigatorios = ["usuario_id", "tipo", "titulo", "mensagem"]
        for campo in campos_obrigatorios:
            if campo not in data:
                raise ValueError(f"Campo obrigatório ausente: {campo}")
        
        # Conversão da data
        criada_em = None
        if data.get("criada_em"):
            criada_em = datetime.fromisoformat(data["criada_em"])
        
        return cls(
            notificacao_id=data.get("notificacao_id"),
            usuario_id=data["usuario_id"],
            tipo=data["tipo"],
            titulo=data["titulo"],
            mensagem=data["mensagem"],
            criada_em=criada_em,
            lida=data.get("lida", False)
        )
    
    # Métodos Utilitários
    
    def get_preview(self, max_chars: int = 50) -> str:
        """
        Retorna um preview da mensagem.
        
        Args:
            max_chars: Número máximo de caracteres (padrão: 50)
            
        Returns:
            Mensagem truncada com reticências se necessário
        """
        if len(self.mensagem) <= max_chars:
            return self.mensagem
        return self.mensagem[:max_chars].rstrip() + "..."
    
    def get_idade_em_segundos(self) -> float:
        """
        Retorna a idade da notificação em segundos.
        
        Returns:
            Número de segundos desde a criação
        """
        agora = datetime.now(timezone.utc)
        delta = agora - self.criada_em
        return delta.total_seconds()
    
    def is_recente(self, minutos: int = 60) -> bool:
        """
        Verifica se a notificação é recente.
        
        Args:
            minutos: Número de minutos para considerar recente (padrão: 60)
            
        Returns:
            True se a notificação foi criada nos últimos X minutos
        """
        segundos = self.get_idade_em_segundos()
        return segundos <= (minutos * 60)