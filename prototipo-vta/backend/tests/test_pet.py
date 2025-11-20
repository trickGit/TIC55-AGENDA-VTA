"""
Testes para a classe Pet
pytest test_pet.py -v
"""

import pytest
from datetime import date, timedelta

# Importações
import sys
sys.path.insert(0, '/mnt/user-data/outputs')

from backend.models.pet import Pet


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def pet_valido():
    """Cria um pet válido para testes."""
    return Pet(
        nome="Rex",
        especie="Cachorro",
        raca="Golden Retriever",
        nascimento=date(2020, 3, 15),
        cliente_id=123
    )


# ============================================================================
# TESTES DO CONSTRUTOR
# ============================================================================

class TestPetConstructor:
    """Testes do construtor da classe Pet."""
    
    def test_criar_pet_valido(self):
        """Deve criar pet com dados válidos."""
        pet = Pet(
            nome="Luna",
            especie="Gato",
            raca="Siamês",
            nascimento=date(2021, 7, 20),
            cliente_id=789
        )
        
        assert pet.nome == "Luna"
        assert pet.especie == "Gato"
        assert pet.raca == "Siamês"
        assert pet.nascimento == date(2021, 7, 20)
        assert pet.cliente_id == 789
        assert pet.uuid is not None
    
    def test_criar_pet_sem_cliente_id(self):
        """Deve criar pet sem cliente_id."""
        pet = Pet(
            nome="Thor",
            especie="Cachorro",
            raca="Husky",
            nascimento=date(2020, 1, 1)
        )
        
        assert pet.cliente_id is None
    
    def test_nome_com_espacos_extras(self):
        """Deve remover espaços extras do nome."""
        pet = Pet(
            nome="  Thor  ",
            especie="Cachorro",
            raca="Husky",
            nascimento=date(2020, 1, 1)
        )
        
        assert pet.nome == "Thor"
    
    def test_especie_com_espacos_extras(self):
        """Deve remover espaços extras da espécie."""
        pet = Pet(
            nome="Miau",
            especie="  Gato  ",
            raca="Persa",
            nascimento=date(2020, 1, 1)
        )
        
        assert pet.especie == "Gato"
    
    def test_raca_com_espacos_extras(self):
        """Deve remover espaços extras da raça."""
        pet = Pet(
            nome="Rex",
            especie="Cachorro",
            raca="  Golden Retriever  ",
            nascimento=date(2020, 1, 1)
        )
        
        assert pet.raca == "Golden Retriever"
    
    def test_raca_vazia_aceita(self):
        """Deve aceitar raça vazia."""
        pet = Pet(
            nome="Miau",
            especie="Gato",
            raca="",
            nascimento=date(2020, 1, 1)
        )
        
        assert pet.raca == ""
    
    def test_raca_none_vira_string_vazia(self):
        """Deve converter None para string vazia."""
        pet = Pet(
            nome="Miau",
            especie="Gato",
            raca=None,
            nascimento=date(2020, 1, 1)
        )
        
        assert pet.raca == ""
    
    def test_uuid_customizado(self):
        """Deve aceitar UUID customizado."""
        uuid_custom = "123e4567-e89b-12d3-a456-426614174000"
        pet = Pet(
            nome="Rex",
            especie="Cachorro",
            raca="SRD",
            nascimento=date(2020, 1, 1),
            pet_uuid=uuid_custom
        )
        
        assert pet.uuid == uuid_custom
    
    def test_uuid_gerado_automaticamente(self):
        """Deve gerar UUID automaticamente se não fornecido."""
        pet = Pet(
            nome="Rex",
            especie="Cachorro",
            raca="SRD",
            nascimento=date(2020, 1, 1)
        )
        
        assert pet.uuid is not None
        assert len(pet.uuid) == 36  # Formato UUID
        assert "-" in pet.uuid
    
    def test_erro_nome_vazio(self):
        """Deve falhar com nome vazio."""
        with pytest.raises(ValueError, match="Nome do pet não pode ser vazio"):
            Pet(
                nome="",
                especie="Cachorro",
                raca="SRD",
                nascimento=date(2020, 1, 1)
            )
    
    def test_erro_nome_apenas_espacos(self):
        """Deve falhar com nome apenas espaços."""
        with pytest.raises(ValueError, match="Nome do pet não pode ser vazio"):
            Pet(
                nome="   ",
                especie="Cachorro",
                raca="SRD",
                nascimento=date(2020, 1, 1)
            )
    
    def test_erro_nome_none(self):
        """Deve falhar com nome None."""
        with pytest.raises((ValueError, AttributeError)):
            Pet(
                nome=None,
                especie="Cachorro",
                raca="SRD",
                nascimento=date(2020, 1, 1)
            )
    
    def test_erro_especie_vazia(self):
        """Deve falhar com espécie vazia."""
        with pytest.raises(ValueError, match="Espécie não pode ser vazia"):
            Pet(
                nome="Rex",
                especie="",
                raca="SRD",
                nascimento=date(2020, 1, 1)
            )
    
    def test_erro_especie_apenas_espacos(self):
        """Deve falhar com espécie apenas espaços."""
        with pytest.raises(ValueError, match="Espécie não pode ser vazia"):
            Pet(
                nome="Rex",
                especie="   ",
                raca="SRD",
                nascimento=date(2020, 1, 1)
            )
    
    def test_erro_nascimento_invalido(self):
        """Deve falhar com nascimento inválido."""
        with pytest.raises(ValueError, match="Nascimento deve ser uma data válida"):
            Pet(
                nome="Rex",
                especie="Cachorro",
                raca="SRD",
                nascimento="2020-01-01"  # String em vez de date
            )
    
    def test_erro_nascimento_none(self):
        """Deve falhar com nascimento None."""
        with pytest.raises(ValueError, match="Nascimento deve ser uma data válida"):
            Pet(
                nome="Rex",
                especie="Cachorro",
                raca="SRD",
                nascimento=None
            )


# ============================================================================
# TESTES DE MÉTODOS
# ============================================================================

class TestPetMetodos:
    """Testes dos métodos da classe Pet."""
    
    def test_calcular_idade_anos_completos(self):
        """Deve calcular idade corretamente."""
        # Pet nascido há 5 anos
        data_nascimento = date.today() - timedelta(days=5*365)
        pet = Pet(
            nome="Rex",
            especie="Cachorro",
            raca="SRD",
            nascimento=data_nascimento
        )
        
        assert pet.calcular_idade() == 5
    
    def test_calcular_idade_antes_aniversario(self):
        """Deve considerar se ainda não fez aniversário este ano."""
        hoje = date.today()
        
        # Se hoje é janeiro, teste com aniversário em dezembro
        if hoje.month == 1:
            ano_nascimento = hoje.year - 6
            data_nascimento = date(ano_nascimento, 12, 15)
            idade_esperada = 5
        else:
            # Nasceu há 5 anos, mas aniversário ainda não chegou
            ano_nascimento = hoje.year - 5
            mes_nascimento = (hoje.month % 12) + 1
            data_nascimento = date(ano_nascimento, mes_nascimento, 1)
            idade_esperada = 4
        
        pet = Pet(
            nome="Rex",
            especie="Cachorro",
            raca="SRD",
            nascimento=data_nascimento
        )
        
        assert pet.calcular_idade() == idade_esperada
    
    def test_calcular_idade_recem_nascido(self):
        """Deve retornar 0 para recém-nascido."""
        pet = Pet(
            nome="Filhote",
            especie="Cachorro",
            raca="SRD",
            nascimento=date.today()
        )
        
        assert pet.calcular_idade() == 0
    
    def test_calcular_idade_um_dia(self):
        """Deve retornar 0 para pet de um dia."""
        pet = Pet(
            nome="Filhote",
            especie="Cachorro",
            raca="SRD",
            nascimento=date.today() - timedelta(days=1)
        )
        
        assert pet.calcular_idade() == 0
    
    def test_calcular_idade_11_meses(self):
        """Deve retornar 0 para pet com menos de 1 ano."""
        pet = Pet(
            nome="Filhote",
            especie="Cachorro",
            raca="SRD",
            nascimento=date.today() - timedelta(days=330)  # ~11 meses
        )
        
        assert pet.calcular_idade() == 0
    
    def test_to_dict_completo(self, pet_valido):
        """Deve converter para dicionário completo."""
        dados = pet_valido.to_dict()
        
        assert isinstance(dados, dict)
        assert dados["uuid"] == pet_valido.uuid
        assert dados["cliente_id"] == pet_valido.cliente_id
        assert dados["nome"] == pet_valido.nome
        assert dados["especie"] == pet_valido.especie
        assert dados["raca"] == pet_valido.raca
        assert dados["nascimento"] == pet_valido.nascimento.isoformat()
        assert "idade" in dados
        assert isinstance(dados["idade"], int)
    
    def test_to_dict_sem_cliente_id(self):
        """Deve funcionar sem cliente_id."""
        pet = Pet(
            nome="Rex",
            especie="Cachorro",
            raca="SRD",
            nascimento=date(2020, 1, 1)
        )
        
        dados = pet.to_dict()
        assert dados["cliente_id"] is None
    
    def test_to_dict_idade_calculada(self):
        """Deve incluir idade calculada no dict."""
        pet = Pet(
            nome="Rex",
            especie="Cachorro",
            raca="SRD",
            nascimento=date.today() - timedelta(days=3*365)
        )
        
        dados = pet.to_dict()
        assert dados["idade"] == 3
    
    def test_repr_legivel(self, pet_valido):
        """Deve ter repr legível."""
        repr_str = repr(pet_valido)
        
        assert "Pet" in repr_str
        assert pet_valido.nome in repr_str
        assert pet_valido.especie in repr_str
        assert pet_valido.raca in repr_str
    
    def test_repr_contem_uuid(self, pet_valido):
        """Deve incluir UUID no repr."""
        repr_str = repr(pet_valido)
        assert "uuid=" in repr_str


# ============================================================================
# TESTES DE CASOS ESPECIAIS
# ============================================================================

class TestPetCasosEspeciais:
    """Testes de casos especiais e edge cases."""
    
    def test_pet_muito_velho(self):
        """Deve calcular idade para pet muito velho."""
        pet = Pet(
            nome="Velho",
            especie="Cachorro",
            raca="SRD",
            nascimento=date(1995, 1, 1)
        )
        
        idade = pet.calcular_idade()
        assert idade >= 29  # Em 2025
        assert idade < 100  # Sanidade
    
    def test_pet_nascido_bissexto(self):
        """Deve lidar com nascimento em ano bissexto."""
        pet = Pet(
            nome="Bissexto",
            especie="Gato",
            raca="SRD",
            nascimento=date(2020, 2, 29)  # Ano bissexto
        )
        
        idade = pet.calcular_idade()
        assert isinstance(idade, int)
        assert idade >= 0
    
    def test_nome_muito_longo(self):
        """Deve aceitar nome muito longo."""
        nome_longo = "A" * 200
        pet = Pet(
            nome=nome_longo,
            especie="Cachorro",
            raca="SRD",
            nascimento=date(2020, 1, 1)
        )
        
        assert pet.nome == nome_longo
    
    def test_especie_exotica(self):
        """Deve aceitar espécies exóticas."""
        especies = ["Iguana", "Papagaio", "Hamster", "Coelho", "Tartaruga"]
        
        for especie in especies:
            pet = Pet(
                nome="Exótico",
                especie=especie,
                raca="Rara",
                nascimento=date(2020, 1, 1)
            )
            assert pet.especie == especie
    
    def test_raca_com_caracteres_especiais(self):
        """Deve aceitar raça com caracteres especiais."""
        pet = Pet(
            nome="Rex",
            especie="Cachorro",
            raca="São Bernardo",
            nascimento=date(2020, 1, 1)
        )
        
        assert pet.raca == "São Bernardo"
    
    def test_multiplos_pets_uuids_diferentes(self):
        """Deve gerar UUIDs diferentes para cada pet."""
        pets = [
            Pet("Pet1", "Cachorro", "SRD", date(2020, 1, 1))
            for _ in range(10)
        ]
        
        uuids = [p.uuid for p in pets]
        assert len(set(uuids)) == 10  # Todos únicos


# ============================================================================
# TESTES DE INTEGRAÇÃO
# ============================================================================

class TestPetIntegracao:
    """Testes de integração e casos de uso reais."""
    
    def test_fluxo_cadastro_completo(self):
        """Testa fluxo completo de cadastro de pet."""
        # Criar pet
        pet = Pet(
            nome="Buddy",
            especie="Cachorro",
            raca="Labrador",
            nascimento=date(2022, 6, 15),
            cliente_id=456
        )
        
        # Verificar dados
        assert pet.nome == "Buddy"
        assert pet.cliente_id == 456
        
        # Calcular idade
        idade = pet.calcular_idade()
        assert idade >= 2
        
        # Serializar
        dados = pet.to_dict()
        assert dados["nome"] == "Buddy"
        assert dados["idade"] >= 2
    
    def test_varios_pets_mesmo_cliente(self):
        """Testa múltiplos pets do mesmo cliente."""
        cliente_id = 789
        
        pets = [
            Pet("Thor", "Cachorro", "Husky", date(2019, 1, 1), cliente_id=cliente_id),
            Pet("Luna", "Gato", "Siamês", date(2021, 6, 15), cliente_id=cliente_id),
            Pet("Bob", "Coelho", "Angorá", date(2023, 3, 10), cliente_id=cliente_id)
        ]
        
        # Todos do mesmo cliente
        assert all(p.cliente_id == cliente_id for p in pets)
        
        # UUIDs únicos
        uuids = [p.uuid for p in pets]
        assert len(set(uuids)) == 3
        
        # Idades diferentes
        idades = [p.calcular_idade() for p in pets]
        assert len(set(idades)) >= 2  # Pelo menos 2 idades diferentes


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])