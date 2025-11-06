from enum import Enum  # Para criar enumerações

# Enumeração dos status possíveis para um usuário
class StatusUsuario(Enum):
    ATIVO = "ativo"  # Usuário ativo
    INATIVO = "inativo"  # Usuário inativo