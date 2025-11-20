from datetime import datetime
from typing import Optional


class Agendamento:
    """
    Classe de modelo (entidade) para representar um agendamento.
    Contém apenas dados e validações básicas de domínio.
    
    A lógica de negócio (criar, editar, cancelar, etc.) deve estar
    na camada de serviço (AgendaServico).
    """
    
    def __init__(self,id: str,sala_id: str,profissional_id: str,cliente_id: str,pet_id: str,inicio: datetime,fim: datetime,tipo_atendimento: str,observacoes: Optional[str] = None,criado_por: Optional[str] = None):
        """
        Inicializa um novo agendamento.
        
        Args:
            id: Identificador único do agendamento
            sala_id: Identificador da sala
            profissional_id: Identificador do profissional
            cliente_id: Identificador do cliente
            pet_id: Identificador do pet
            inicio: Data e hora de início
            fim: Data e hora de término
            tipo_atendimento: Tipo do atendimento
            observacoes: Observações adicionais (opcional)
            criado_por: Identificador de quem criou (opcional)
        """
        # Validações básicas de domínio
        self._validar_datas(inicio, fim)
        self._validar_ids(id, sala_id, profissional_id, cliente_id, pet_id)
        
        # Atributos principais
        self.id = id
        self.sala_id = sala_id
        self.profissional_id = profissional_id
        self.cliente_id = cliente_id
        self.pet_id = pet_id
        self.inicio = inicio
        self.fim = fim
        self.tipo_atendimento = tipo_atendimento
        self.observacoes = observacoes
        self.criado_por = criado_por
        
        # Atributos de controle
        self.status = "AGENDADO"
        self.criado_em = datetime.now()
        self.cancelado_por: Optional[str] = None
        self.cancelado_em: Optional[datetime] = None
    
    def _validar_datas(self, inicio: datetime, fim: datetime) -> None:
        """Valida se as datas são válidas."""
        if inicio >= fim:
            raise ValueError("A data de início deve ser anterior à data de término")
    
    def _validar_ids(self, *ids: str) -> None:
        """Valida se os IDs não estão vazios."""
        for id_val in ids:
            if not id_val or not id_val.strip():
                raise ValueError("IDs não podem ser vazios")
    
    def gerar_ticket_texto(self) -> str:
        """
        Gera um ticket em formato texto com todas as informações do agendamento.
        Este método pode permanecer aqui pois é apenas uma representação dos dados.
        
        Returns:
            String formatada com o ticket
        """
        formato_data = "%d/%m/%Y %H:%M"
        
        ticket = []
        ticket.append("=" * 50)
        ticket.append("         TICKET DE AGENDAMENTO         ".center(50))
        ticket.append("=" * 50)
        ticket.append("")
        ticket.append(f"ID do Agendamento: {self.id}")
        ticket.append(f"Status: {self.status}")
        ticket.append("")
        ticket.append("-" * 50)
        ticket.append("INFORMAÇÕES DO AGENDAMENTO")
        ticket.append("-" * 50)
        ticket.append(f"Tipo de Atendimento: {self.tipo_atendimento}")
        ticket.append(f"Data/Hora Início: {self.inicio.strftime(formato_data)}")
        ticket.append(f"Data/Hora Fim: {self.fim.strftime(formato_data)}")
        ticket.append(f"Sala: {self.sala_id}")
        ticket.append("")
        ticket.append("-" * 50)
        ticket.append("RESPONSÁVEIS")
        ticket.append("-" * 50)
        ticket.append(f"Profissional ID: {self.profissional_id}")
        ticket.append(f"Cliente ID: {self.cliente_id}")
        ticket.append(f"Pet ID: {self.pet_id}")
        ticket.append("")
        
        if self.observacoes:
            ticket.append("-" * 50)
            ticket.append("OBSERVAÇÕES")
            ticket.append("-" * 50)
            ticket.append(self.observacoes)
            ticket.append("")
        
        ticket.append("-" * 50)
        ticket.append(f"Criado em: {self.criado_em.strftime(formato_data)}")
        ticket.append(f"Criado por: {self.criado_por if self.criado_por else 'N/A'}")
        
        if self.cancelado_em:
            ticket.append(f"Cancelado em: {self.cancelado_em.strftime(formato_data)}")
            ticket.append(f"Cancelado por: {self.cancelado_por}")
        
        ticket.append("=" * 50)
        
        return "\n".join(ticket)
    
    def __str__(self) -> str:
        """Representação em string do agendamento."""
        return (
            f"Agendamento(id='{self.id}', sala_id='{self.sala_id}', "
            f"profissional_id='{self.profissional_id}', cliente_id='{self.cliente_id}', "
            f"pet_id='{self.pet_id}', inicio={self.inicio}, fim={self.fim}, "
            f"status='{self.status}', tipo_atendimento='{self.tipo_atendimento}')"
        )
    
    def __repr__(self) -> str:
        """Representação técnica do agendamento."""
        return self.__str__()
    
    def to_dict(self) -> dict:
        """
        Converte o agendamento para um dicionário.
        
        Returns:
            Dicionário com todos os atributos do agendamento
        """
        return {
            'id': self.id,
            'sala_id': self.sala_id,
            'profissional_id': self.profissional_id,
            'cliente_id': self.cliente_id,
            'pet_id': self.pet_id,
            'inicio': self.inicio.isoformat(),
            'fim': self.fim.isoformat(),
            'tipo_atendimento': self.tipo_atendimento,
            'status': self.status,
            'observacoes': self.observacoes,
            'criado_por': self.criado_por,
            'criado_em': self.criado_em.isoformat(),
            'cancelado_por': self.cancelado_por,
            'cancelado_em': self.cancelado_em.isoformat() if self.cancelado_em else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Agendamento':
        """
        Cria um agendamento a partir de um dicionário.
        
        Args:
            data: Dicionário com os dados do agendamento
            
        Returns:
            Nova instância de Agendamento
        """
        agendamento = cls(
            id=data['id'],
            sala_id=data['sala_id'],
            profissional_id=data['profissional_id'],
            cliente_id=data['cliente_id'],
            pet_id=data['pet_id'],
            inicio=datetime.fromisoformat(data['inicio']),
            fim=datetime.fromisoformat(data['fim']),
            tipo_atendimento=data['tipo_atendimento'],
            observacoes=data.get('observacoes'),
            criado_por=data.get('criado_por')
        )
        
        # Restaura os atributos de controle
        agendamento.status = data['status']
        agendamento.criado_em = datetime.fromisoformat(data['criado_em'])
        agendamento.cancelado_por = data.get('cancelado_por')
        if data.get('cancelado_em'):
            agendamento.cancelado_em = datetime.fromisoformat(data['cancelado_em'])
        
        return agendamento