from enum import Enum  # Para criar enumerações

# Enumeração dos status possíveis para agendamentos no sistema
class statusAgendamento(Enum):
    AGENDADO = "AGENDADO" # Status quando o agendamento está confirmado
    CANCELADO = "CANCELADO" # Status quando o agendamento foi cancelado
    CONCLUIDO = "CONCLUIDO" # Status quando o agendamento foi finalizado
    PENDENTE = "PENDENTE" # Status quando o agendamento está aguardando confirmação