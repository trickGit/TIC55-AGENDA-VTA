from typing import List, Optional
from uuid import UUID
from models.pet import Pet


class PetServico:
    """
    Serviço para gerenciar operações relacionadas a pets.
    
    Attributes:
        pets: Lista de pets cadastrados no sistema
    """
    
    def __init__(self):
        """Inicializa o serviço com uma lista vazia de pets."""
        self.pets: List[Pet] = []
    
    def criar(self, pet: Pet) -> Pet:
        """
        Adiciona um novo pet ao sistema.
        
        Args:
            pet: Objeto Pet a ser cadastrado
            
        Returns:
            O pet cadastrado
            
        Raises:
            ValueError: Se já existir um pet com o mesmo UUID
        """
        # Verifica se já existe um pet com este UUID
        if any(p.pet_id == pet.pet_id for p in self.pets):
            raise ValueError(f"Pet com UUID {pet.pet_id} já existe")
        
        self.pets.append(pet)
        return pet
    
    def atualizar(self, pet: Pet) -> Pet:
        """
        Atualiza os dados de um pet existente.
        
        Args:
            pet: Objeto Pet com os dados atualizados
            
        Returns:
            O pet atualizado
            
        Raises:
            ValueError: Se o pet não for encontrado
        """
        for i, p in enumerate(self.pets):
            if p.pet_id == pet.pet_id:
                self.pets[i] = pet
                return pet
        
        raise ValueError(f"Pet com UUID {pet.pet_id} não encontrado")
    
    def buscar_por_cliente(self, cliente_id: int) -> List[Pet]:
        """
        Busca todos os pets de um cliente específico.
        
        Args:
            cliente_id: ID do cliente
            
        Returns:
            Lista de pets pertencentes ao cliente (pode ser vazia)
        """
        return [pet for pet in self.pets if pet.cliente_id == cliente_id]
    
    def buscar_por_uuid(self, pet_id: UUID | str) -> Optional[Pet]:
        """
        Busca um pet pelo seu UUID.
        
        Args:
            pet_id: UUID do pet (pode ser string ou UUID)
            
        Returns:
            O pet encontrado ou None se não existir
        """
        pet_id_str = str(pet_id)
        for pet in self.pets:
            if str(pet.pet_id) == pet_id_str:
                return pet
        return None
    
    def listar_todos(self) -> List[Pet]:
        """
        Lista todos os pets cadastrados.
        
        Returns:
            Lista com todos os pets
        """
        return self.pets.copy()
    
    def deletar(self, pet_id: UUID | str) -> bool:
        """
        Remove um pet do sistema.
        
        Args:
            pet_id: UUID do pet a ser removido
            
        Returns:
            True se o pet foi removido, False se não foi encontrado
        """
        pet_id_str = str(pet_id)
        for i, pet in enumerate(self.pets):
            if str(pet.pet_id) == pet_id_str:
                self.pets.pop(i)
                return True
        return False