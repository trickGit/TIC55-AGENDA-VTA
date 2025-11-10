from uuid import uuid4
from datetime import datetime

class Sala:
  
    # Inicializa uma nova sala com um ID único, nome, tipo e status de atividade
    def __init__(self, nome: str, tipo: str, ativa:bool, uuid=None):
        self.SalaID = uuid if uuid is not None else str(uuid4())
        self.nome = nome
        self.tipo = tipo
        self.ativa = ativa

    # Retorna o status da sala ('livre', 'ocupada' ou 'bloqueada') no horário informado
    def statusEm(self, dataHora: datetime) -> str:
        if not self.ativa:
            return "bloqueada"

        for reserva in self.reservas:
            if reserva.inicio <= dataHora <= reserva.fim:
                return "ocupada"

        return "livre"