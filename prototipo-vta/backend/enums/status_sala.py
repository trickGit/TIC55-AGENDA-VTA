from enum import Enum  # Para criar enumerações

# Enumeração dos status possíveis para salas no sistema
class StatusSala(Enum):
    DISPONIVEL = "DISPONIVEL" # Sala está disponível para uso
    OCUPADA = "OCUPADA" # Sala está atualmente em uso
    BLOQUEADA = "BLOQUEADA" # Sala está bloqueada para manutenção ou outros motivos