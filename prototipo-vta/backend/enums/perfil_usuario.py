from enum import Enum  # Para criar enumerações

# Enumeração dos tipos de perfis de usuário disponíveis no sistema
class PerfilUsuario(Enum):
    ADMIN = "admin"  # Perfil com acesso total
    RECEPCIONISTA = "recepcionista"  # Perfil com acesso intermediário
    VETERINARIO = "veterinario"  # Perfil com acesso limitado