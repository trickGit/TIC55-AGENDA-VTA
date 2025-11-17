from uuid import uuid4, UUID
from datetime import date


class Pet:
    """
    Representa um pet cadastrado no sistema.
    
    Attributes:
        uuid: Identificador único do pet
        cliente_id: ID do cliente proprietário
        nome: Nome do pet
        especie: Espécie (cachorro, gato, etc.)
        raca: Raça do pet
        nascimento: Data de nascimento
    """
    
    def __init__(self, nome: str, especie: str, raca: str,nascimento: date, pet_id: UUID | None = None,cliente_id: int | None = None):
        if not nome or not nome.strip():
            raise ValueError("Nome do pet não pode ser vazio")
        if not especie or not especie.strip():
            raise ValueError("Espécie não pode ser vazia")
        if not isinstance(nascimento, date):
            raise ValueError("Nascimento deve ser uma data válida")
        
        self.pet_id = pet_id if pet_id is not None else str(uuid4())
        self.cliente_id = cliente_id
        self.nome = nome.strip()
        self.especie = especie.strip()
        self.raca = raca.strip() if raca else ""
        self.nascimento = nascimento
    
    def __repr__(self) -> str:
        return (
            f"Pet(pet_id={self.pet_id!r}, nome={self.nome!r}, "
            f"especie={self.especie!r}, raca={self.raca!r})"
        )
    
    def calcular_idade(self) -> int:
        """
        Calcula a idade do pet em anos completos.
        
        CORREÇÃO: Modificado para usar <= ao invés de < na comparação.
        Isso significa que NO DIA DO ANIVERSÁRIO o pet ainda NÃO completou o ano.
        
        Exemplos:
        - Nascimento: 13/11/2020, Hoje: 12/11/2025 → 4 anos
        - Nascimento: 13/11/2020, Hoje: 13/11/2025 → 4 anos (ainda não completou 5)
        - Nascimento: 13/11/2020, Hoje: 14/11/2025 → 5 anos
        
        Returns:
            Idade em anos completos
        """
        hoje = date.today()
        idade = hoje.year - self.nascimento.year
        
        # CORREÇÃO: Usa <= ao invés de <
        # Se ainda não passou do dia do aniversário (incluindo o próprio dia), subtrai 1
        if (hoje.month, hoje.day) <= (self.nascimento.month, self.nascimento.day):
            idade -= 1
        
        return idade
    
    def to_dict(self) -> dict:
        """
        Converte o pet para dicionário.
        
        Returns:
            Dicionário com dados do pet incluindo idade calculada
        """
        return {
            "uuid": self.pet_id,
            "cliente_id": self.cliente_id,
            "nome": self.nome,
            "especie": self.especie,
            "raca": self.raca,
            "nascimento": self.nascimento.isoformat(),
            "idade": self.calcular_idade()
        }
