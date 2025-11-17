"""
Testes para a classe Endereco
pytest test_endereco.py -v
"""

import pytest

# Importações
import sys
sys.path.insert(0, '/mnt/user-data/outputs')

from backend.models.endereco import Endereco


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def endereco_valido():
    """Cria um endereço válido para testes."""
    return Endereco(
        rua="Rua das Flores",
        numero=123,
        bairro="Centro",
        cidade="Gravataí",
        uf="RS",
        cep="94010-000",
        cliente_id=456
    )


# ============================================================================
# TESTES DO CONSTRUTOR
# ============================================================================

class TestEnderecoConstructor:
    """Testes do construtor da classe Endereco."""
    
    def test_criar_endereco_valido(self):
        """Deve criar endereço com dados válidos."""
        endereco = Endereco(
            rua="Avenida Brasil",
            numero="456-A",
            bairro="Centro",
            cidade="Porto Alegre",
            uf="RS",
            cep="90000-000",
            cliente_id=789
        )
        
        assert endereco.rua == "Avenida Brasil"
        assert endereco.numero == "456-A"
        assert endereco.bairro == "Centro"
        assert endereco.cidade == "Porto Alegre"
        assert endereco.uf == "RS"
        assert endereco.cep == "90000-000"
        assert endereco.cliente_id == 789
        assert endereco.uuid is not None
    
    def test_criar_endereco_sem_cliente_id(self):
        """Deve criar endereço sem cliente_id."""
        endereco = Endereco(
            rua="Rua Teste",
            numero=1,
            bairro="Bairro",
            cidade="Cidade",
            uf="RS",
            cep="94010-000"
        )
        
        assert endereco.cliente_id is None
    
    def test_uf_normalizado_uppercase(self):
        """Deve converter UF para uppercase."""
        endereco = Endereco(
            rua="Rua Teste",
            numero=1,
            bairro="Bairro",
            cidade="Cidade",
            uf="rs",
            cep="94010-000"
        )
        
        assert endereco.uf == "RS"
    
    def test_uf_minuscula_convertida(self):
        """Deve converter UF minúscula para maiúscula."""
        ufs_teste = ["sp", "rj", "mg", "pr", "sc"]
        
        for uf_lower in ufs_teste:
            endereco = Endereco(
                rua="Rua",
                numero=1,
                bairro="Bairro",
                cidade="Cidade",
                uf=uf_lower,
                cep="94010-000"
            )
            assert endereco.uf == uf_lower.upper()
    
    def test_uf_mista_convertida(self):
        """Deve converter UF com case misto."""
        endereco = Endereco(
            rua="Rua",
            numero=1,
            bairro="Bairro",
            cidade="Cidade",
            uf="Rs",
            cep="94010-000"
        )
        
        assert endereco.uf == "RS"
    
    def test_cep_formatado_com_hifen(self):
        """Deve formatar CEP com hífen."""
        endereco = Endereco(
            rua="Rua Teste",
            numero=1,
            bairro="Bairro",
            cidade="Cidade",
            uf="RS",
            cep="94010000"
        )
        
        assert endereco.cep == "94010-000"
    
    def test_cep_ja_formatado(self):
        """Deve aceitar CEP já formatado."""
        endereco = Endereco(
            rua="Rua Teste",
            numero=1,
            bairro="Bairro",
            cidade="Cidade",
            uf="RS",
            cep="94010-000"
        )
        
        assert endereco.cep == "94010-000"
    
    def test_cep_com_espacos_removidos(self):
        """Deve remover espaços do CEP."""
        endereco = Endereco(
            rua="Rua Teste",
            numero=1,
            bairro="Bairro",
            cidade="Cidade",
            uf="RS",
            cep="94010 000"
        )
        
        assert endereco.cep == "94010-000"
    
    def test_cep_com_pontos_removidos(self):
        """Deve remover pontos do CEP."""
        endereco = Endereco(
            rua="Rua Teste",
            numero=1,
            bairro="Bairro",
            cidade="Cidade",
            uf="RS",
            cep="94.010.000"
        )
        
        assert endereco.cep == "94010-000"
    
    def test_numero_inteiro_convertido_string(self):
        """Deve converter número inteiro para string."""
        endereco = Endereco(
            rua="Rua Teste",
            numero=123,
            bairro="Bairro",
            cidade="Cidade",
            uf="RS",
            cep="94010-000"
        )
        
        assert endereco.numero == "123"
        assert isinstance(endereco.numero, str)
    
    def test_numero_string_aceito(self):
        """Deve aceitar número como string."""
        endereco = Endereco(
            rua="Rua Teste",
            numero="456-A",
            bairro="Bairro",
            cidade="Cidade",
            uf="RS",
            cep="94010-000"
        )
        
        assert endereco.numero == "456-A"
    
    def test_espacos_extras_removidos(self):
        """Deve remover espaços extras de todos os campos."""
        endereco = Endereco(
            rua="  Rua Teste  ",
            numero="  123  ",
            bairro="  Bairro  ",
            cidade="  Cidade  ",
            uf="  RS  ",
            cep="94010-000"
        )
        
        assert endereco.rua == "Rua Teste"
        assert endereco.numero == "123"
        assert endereco.bairro == "Bairro"
        assert endereco.cidade == "Cidade"
        assert endereco.uf == "RS"
    
    def test_uuid_customizado(self):
        """Deve aceitar UUID customizado."""
        uuid_custom = "123e4567-e89b-12d3-a456-426614174000"
        endereco = Endereco(
            rua="Rua Teste",
            numero=1,
            bairro="Bairro",
            cidade="Cidade",
            uf="RS",
            cep="94010-000",
            endereco_uuid=uuid_custom
        )
        
        assert endereco.uuid == uuid_custom
    
    def test_uuid_gerado_automaticamente(self):
        """Deve gerar UUID automaticamente."""
        endereco = Endereco(
            rua="Rua",
            numero=1,
            bairro="Bairro",
            cidade="Cidade",
            uf="RS",
            cep="94010-000"
        )
        
        assert endereco.uuid is not None
        assert len(endereco.uuid) == 36


# ============================================================================
# TESTES DE VALIDAÇÃO - ERROS
# ============================================================================

class TestEnderecoValidacoes:
    """Testes de validações que devem falhar."""
    
    def test_erro_rua_vazia(self):
        """Deve falhar com rua vazia."""
        with pytest.raises(ValueError, match="Rua não pode ser vazia"):
            Endereco(
                rua="",
                numero=1,
                bairro="Bairro",
                cidade="Cidade",
                uf="RS",
                cep="94010-000"
            )
    
    def test_erro_rua_apenas_espacos(self):
        """Deve falhar com rua apenas espaços."""
        with pytest.raises(ValueError, match="Rua não pode ser vazia"):
            Endereco(
                rua="   ",
                numero=1,
                bairro="Bairro",
                cidade="Cidade",
                uf="RS",
                cep="94010-000"
            )
    
    def test_erro_rua_none(self):
        """Deve falhar com rua None."""
        with pytest.raises((ValueError, AttributeError)):
            Endereco(
                rua=None,
                numero=1,
                bairro="Bairro",
                cidade="Cidade",
                uf="RS",
                cep="94010-000"
            )
    
    def test_erro_bairro_vazio(self):
        """Deve falhar com bairro vazio."""
        with pytest.raises(ValueError, match="Bairro não pode ser vazio"):
            Endereco(
                rua="Rua Teste",
                numero=1,
                bairro="",
                cidade="Cidade",
                uf="RS",
                cep="94010-000"
            )
    
    def test_erro_bairro_apenas_espacos(self):
        """Deve falhar com bairro apenas espaços."""
        with pytest.raises(ValueError, match="Bairro não pode ser vazio"):
            Endereco(
                rua="Rua Teste",
                numero=1,
                bairro="   ",
                cidade="Cidade",
                uf="RS",
                cep="94010-000"
            )
    
    def test_erro_cidade_vazia(self):
        """Deve falhar com cidade vazia."""
        with pytest.raises(ValueError, match="Cidade não pode ser vazia"):
            Endereco(
                rua="Rua Teste",
                numero=1,
                bairro="Bairro",
                cidade="",
                uf="RS",
                cep="94010-000"
            )
    
    def test_erro_cidade_apenas_espacos(self):
        """Deve falhar com cidade apenas espaços."""
        with pytest.raises(ValueError, match="Cidade não pode ser vazia"):
            Endereco(
                rua="Rua Teste",
                numero=1,
                bairro="Bairro",
                cidade="   ",
                uf="RS",
                cep="94010-000"
            )
    
    def test_erro_uf_invalida_tamanho(self):
        """Deve falhar com UF de tamanho inválido."""
        with pytest.raises(ValueError, match="UF deve ter 2 caracteres"):
            Endereco(
                rua="Rua Teste",
                numero=1,
                bairro="Bairro",
                cidade="Cidade",
                uf="RSX",
                cep="94010-000"
            )
    
    def test_erro_uf_um_caractere(self):
        """Deve falhar com UF de 1 caractere."""
        with pytest.raises(ValueError, match="UF deve ter 2 caracteres"):
            Endereco(
                rua="Rua Teste",
                numero=1,
                bairro="Bairro",
                cidade="Cidade",
                uf="R",
                cep="94010-000"
            )
    
    def test_erro_uf_vazia(self):
        """Deve falhar com UF vazia."""
        with pytest.raises(ValueError, match="UF deve ter 2 caracteres"):
            Endereco(
                rua="Rua Teste",
                numero=1,
                bairro="Bairro",
                cidade="Cidade",
                uf="",
                cep="94010-000"
            )
    
    def test_erro_cep_muito_curto(self):
        """Deve falhar com CEP muito curto."""
        with pytest.raises(ValueError, match="CEP inválido"):
            Endereco(
                rua="Rua Teste",
                numero=1,
                bairro="Bairro",
                cidade="Cidade",
                uf="RS",
                cep="123"
            )
    
    def test_erro_cep_muito_longo(self):
        """Deve falhar com CEP muito longo."""
        with pytest.raises(ValueError, match="CEP inválido"):
            Endereco(
                rua="Rua Teste",
                numero=1,
                bairro="Bairro",
                cidade="Cidade",
                uf="RS",
                cep="940100001234"
            )
    
    def test_erro_cep_com_letras(self):
        """Deve falhar com CEP contendo letras."""
        with pytest.raises(ValueError, match="CEP inválido"):
            Endereco(
                rua="Rua Teste",
                numero=1,
                bairro="Bairro",
                cidade="Cidade",
                uf="RS",
                cep="9401A-000"
            )
    
    def test_erro_cep_vazio(self):
        """Deve falhar com CEP vazio."""
        with pytest.raises(ValueError, match="CEP inválido"):
            Endereco(
                rua="Rua Teste",
                numero=1,
                bairro="Bairro",
                cidade="Cidade",
                uf="RS",
                cep=""
            )
    
    def test_erro_cep_apenas_letras(self):
        """Deve falhar com CEP apenas letras."""
        with pytest.raises(ValueError, match="CEP inválido"):
            Endereco(
                rua="Rua Teste",
                numero=1,
                bairro="Bairro",
                cidade="Cidade",
                uf="RS",
                cep="ABCDEFGH"
            )


# ============================================================================
# TESTES DE MÉTODOS
# ============================================================================

class TestEnderecoMetodos:
    """Testes dos métodos da classe Endereco."""
    
    def test_endereco_completo_formatado(self, endereco_valido):
        """Deve retornar endereço formatado."""
        completo = endereco_valido.endereco_completo()
        
        assert isinstance(completo, str)
        assert endereco_valido.rua in completo
        assert endereco_valido.numero in completo
        assert endereco_valido.bairro in completo
        assert endereco_valido.cidade in completo
        assert endereco_valido.uf in completo
        assert endereco_valido.cep in completo
        assert "\n" in completo
    
    def test_endereco_completo_formato_correto(self, endereco_valido):
        """Deve ter formato correto de endereço brasileiro."""
        completo = endereco_valido.endereco_completo()
        linhas = completo.split("\n")
        
        assert len(linhas) == 2
        # Primeira linha: Rua, número - Bairro
        assert endereco_valido.rua in linhas[0]
        assert endereco_valido.numero in linhas[0]
        assert endereco_valido.bairro in linhas[0]
        assert "-" in linhas[0]
        
        # Segunda linha: Cidade/UF - CEP: xxxxx-xxx
        assert endereco_valido.cidade in linhas[1]
        assert endereco_valido.uf in linhas[1]
        assert "CEP:" in linhas[1]
        assert "/" in linhas[1]
    
    def test_to_dict_completo(self, endereco_valido):
        """Deve converter para dicionário completo."""
        dados = endereco_valido.to_dict()
        
        assert isinstance(dados, dict)
        assert dados["uuid"] == endereco_valido.uuid
        assert dados["cliente_id"] == endereco_valido.cliente_id
        assert dados["rua"] == endereco_valido.rua
        assert dados["numero"] == endereco_valido.numero
        assert dados["bairro"] == endereco_valido.bairro
        assert dados["cidade"] == endereco_valido.cidade
        assert dados["uf"] == endereco_valido.uf
        assert dados["cep"] == endereco_valido.cep
    
    def test_to_dict_sem_cliente_id(self):
        """Deve funcionar sem cliente_id."""
        endereco = Endereco(
            rua="Rua",
            numero=1,
            bairro="Bairro",
            cidade="Cidade",
            uf="RS",
            cep="94010-000"
        )
        
        dados = endereco.to_dict()
        assert dados["cliente_id"] is None
    
    def test_to_dict_tipos_corretos(self, endereco_valido):
        """Deve ter tipos corretos no dicionário."""
        dados = endereco_valido.to_dict()
        
        assert isinstance(dados["uuid"], str)
        assert isinstance(dados["rua"], str)
        assert isinstance(dados["numero"], str)
        assert isinstance(dados["bairro"], str)
        assert isinstance(dados["cidade"], str)
        assert isinstance(dados["uf"], str)
        assert isinstance(dados["cep"], str)
    
    def test_repr_legivel(self, endereco_valido):
        """Deve ter repr legível."""
        repr_str = repr(endereco_valido)
        
        assert "Endereco" in repr_str
        assert endereco_valido.rua in repr_str
        assert endereco_valido.cidade in repr_str
        assert endereco_valido.uf in repr_str
    
    def test_repr_contem_uuid(self, endereco_valido):
        """Deve incluir UUID no repr."""
        repr_str = repr(endereco_valido)
        assert "uuid=" in repr_str


# ============================================================================
# TESTES DE CASOS ESPECIAIS
# ============================================================================

class TestEnderecoCasosEspeciais:
    """Testes de casos especiais e edge cases."""
    
    def test_rua_muito_longa(self):
        """Deve aceitar rua muito longa."""
        rua_longa = "Rua " + "A" * 200
        endereco = Endereco(
            rua=rua_longa,
            numero=1,
            bairro="Bairro",
            cidade="Cidade",
            uf="RS",
            cep="94010-000"
        )
        
        assert endereco.rua == rua_longa
    
    def test_numero_com_complemento(self):
        """Deve aceitar número com complemento."""
        numeros_teste = ["123-A", "456 Apto 101", "789/201", "S/N"]
        
        for num in numeros_teste:
            endereco = Endereco(
                rua="Rua",
                numero=num,
                bairro="Bairro",
                cidade="Cidade",
                uf="RS",
                cep="94010-000"
            )
            assert endereco.numero == num.strip()
    
    def test_numero_sem_numero(self):
        """Deve aceitar 'S/N' como número."""
        endereco = Endereco(
            rua="Rua",
            numero="S/N",
            bairro="Bairro",
            cidade="Cidade",
            uf="RS",
            cep="94010-000"
        )
        
        assert endereco.numero == "S/N"
    
    def test_cidade_com_acentos(self):
        """Deve aceitar cidade com acentos."""
        cidades = ["São Paulo", "Brasília", "Goiânia", "João Pessoa"]
        
        for cidade in cidades:
            endereco = Endereco(
                rua="Rua",
                numero=1,
                bairro="Bairro",
                cidade=cidade,
                uf="SP",
                cep="01000-000"
            )
            assert endereco.cidade == cidade
    
    def test_bairro_com_caracteres_especiais(self):
        """Deve aceitar bairro com caracteres especiais."""
        endereco = Endereco(
            rua="Rua",
            numero=1,
            bairro="Jardim América/Sul",
            cidade="Cidade",
            uf="RS",
            cep="94010-000"
        )
        
        assert "/" in endereco.bairro
    
    def test_todos_estados_brasileiros(self):
        """Deve aceitar todos os estados brasileiros."""
        estados = [
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
            "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
            "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
        ]
        
        for uf in estados:
            endereco = Endereco(
                rua="Rua",
                numero=1,
                bairro="Bairro",
                cidade="Cidade",
                uf=uf,
                cep="00000-000"
            )
            assert endereco.uf == uf
    
    def test_ceps_de_diferentes_estados(self):
        """Deve aceitar CEPs de diferentes estados."""
        ceps_teste = [
            "01000-000",  # SP
            "20000-000",  # RJ
            "30000-000",  # MG
            "40000-000",  # BA
            "50000-000",  # PE
            "60000-000",  # CE
            "70000-000",  # DF
            "80000-000",  # PR
            "90000-000",  # RS
        ]
        
        for cep in ceps_teste:
            endereco = Endereco(
                rua="Rua",
                numero=1,
                bairro="Bairro",
                cidade="Cidade",
                uf="SP",
                cep=cep
            )
            assert endereco.cep == cep
    
    def test_multiplos_enderecos_uuids_diferentes(self):
        """Deve gerar UUIDs diferentes para cada endereço."""
        enderecos = [
            Endereco(f"Rua {i}", i, "Bairro", "Cidade", "RS", "94010-000")
            for i in range(10)
        ]
        
        uuids = [e.uuid for e in enderecos]
        assert len(set(uuids)) == 10


# ============================================================================
# TESTES DE INTEGRAÇÃO
# ============================================================================

class TestEnderecoIntegracao:
    """Testes de integração e casos de uso reais."""
    
    def test_fluxo_cadastro_completo(self):
        """Testa fluxo completo de cadastro de endereço."""
        # Dados do formulário (com formatação variada)
        endereco = Endereco(
            rua="  Rua das Palmeiras  ",
            numero="  789-A  ",
            bairro="  Vila Nova  ",
            cidade="  GRAVATAI  ",
            uf="rs",
            cep="94040123",
            cliente_id=1001
        )
        
        # Verificar normalização
        assert endereco.rua == "Rua das Palmeiras"
        assert endereco.numero == "789-A"
        assert endereco.bairro == "Vila Nova"
        assert endereco.cidade == "GRAVATAI"  # Cidade não muda case
        assert endereco.uf == "RS"  # UF normalizado
        assert endereco.cep == "94040-123"  # CEP formatado
        
        # Verificar serialização
        dados = endereco.to_dict()
        assert dados["cliente_id"] == 1001
        
        # Verificar formatação
        completo = endereco.endereco_completo()
        assert "Rua das Palmeiras" in completo
        assert "94040-123" in completo
    
    def test_endereco_comercial_vs_residencial(self):
        """Testa diferentes tipos de endereço."""
        # Residencial
        residencial = Endereco(
            rua="Rua das Flores",
            numero="123",
            bairro="Jardim Botânico",
            cidade="Porto Alegre",
            uf="RS",
            cep="90000-000",
            cliente_id=1
        )
        
        # Comercial (com complemento)
        comercial = Endereco(
            rua="Avenida Paulista",
            numero="1000 Sala 501",
            bairro="Bela Vista",
            cidade="São Paulo",
            uf="SP",
            cep="01310-100",
            cliente_id=2
        )
        
        assert residencial.numero == "123"
        assert "Sala" in comercial.numero
        assert residencial.cliente_id != comercial.cliente_id
    
    def test_multiplos_enderecos_mesmo_cliente(self):
        """Testa múltiplos endereços do mesmo cliente."""
        cliente_id = 999
        
        enderecos = [
            Endereco("Rua A", 1, "Bairro A", "Cidade A", "RS", "90000-000", cliente_id=cliente_id),
            Endereco("Rua B", 2, "Bairro B", "Cidade B", "RS", "91000-000", cliente_id=cliente_id),
        ]
        
        # Todos do mesmo cliente
        assert all(e.cliente_id == cliente_id for e in enderecos)
        
        # UUIDs diferentes
        uuids = [e.uuid for e in enderecos]
        assert len(set(uuids)) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])