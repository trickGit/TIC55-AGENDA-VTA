from uuid import uuid4, UUID
from datetime import date

class Pet :
    
    def __init__(self, nome: str, especie: str, raca: int, nascimento: date):
        self.PetID = uuid if uuid is not None else str(uuid4())
        self.ClienteID = 
        self.nome = nome
        self.especie = especie
        self.raca = raca
        self.nascimento = nascimento

    