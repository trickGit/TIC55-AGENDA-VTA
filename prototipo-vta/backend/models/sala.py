from uuid import uuid4, UUID
from datetime import datetime


class Sala:
    """
    Representa uma sala/consultório do sistema (Anemic Domain Model).
    
    Lógica de negócio gerenciada por SalaServico.
    
    Attributes:
        uuid: Identificador único da sala
        nome: Nome ou número da sala
        tipo: Tipo de sala (consultório, cirurgia, internação, etc.)
        ativa: Se a sala está ativa/disponível
    """
    
    def __init__(self, nome: str, tipo: str, ativa: bool = True, sala_id: UUID | None = None):
        """
        Inicializa uma nova sala.
        
        Args:
            nome: Nome ou número da sala
            tipo: Tipo de sala
            ativa: Se a sala está ativa
            uuid: UUID da sala (gerado automaticamente se None)
            
        Raises:
            ValueError: Se dados inválidos forem fornecidos
        """
        if not nome or not nome.strip():
            raise ValueError("Nome da sala não pode ser vazio")
        
        if not tipo or not tipo.strip():
            raise ValueError("Tipo da sala não pode ser vazio")
        
        if not isinstance(ativa, bool):
            raise ValueError("Ativa deve ser booleano")
        
        self.sala_id = sala_id if sala_id is not None else str(uuid4())
        self.nome = nome.strip()
        self.tipo = tipo.strip()
        self.ativa = ativa
    
    def __repr__(self) -> str:
        return (
            f"Sala(uuid={self.uuid!r}, nome={self.nome!r}, "
            f"tipo={self.tipo!r}, ativa={self.ativa})"
        )
    
    def statusEm(self, dataHora: datetime, reservas: list = None) -> str:
        """
        Retorna o status da sala em um horário específico.
        
        Args:
            dataHora: Data/hora para verificar
            reservas: Lista de reservas (objetos com .inicio e .fim)
            
        Returns:
            'bloqueada', 'ocupada' ou 'livre'
            
        Note:
            Este método NÃO busca reservas do banco. Recebe reservas
            já carregadas pelo SalaServico ou AgendaServico.
        """
        if not self.ativa:
            return "bloqueada"
        
        if reservas is None:
            reservas = []
        
        for reserva in reservas:
            if hasattr(reserva, 'inicio') and hasattr(reserva, 'fim'):
                if reserva.inicio <= dataHora <= reserva.fim:
                    return "ocupada"
        
        return "livre"
    
    def to_dict(self) -> dict:
        """Converte a sala para dicionário."""
        return {
            "sala_id": self.sala_id,
            "nome": self.nome,
            "tipo": self.tipo,
            "ativa": self.ativa
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Sala":
        """Cria sala a partir de dicionário."""
        return cls(
            sala_id=data.get("sala_id"),
            nome=data["nome"],
            tipo=data["tipo"],
            ativa=data.get("ativa", True)
        )