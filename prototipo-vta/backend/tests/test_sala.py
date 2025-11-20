"""
Testes para a classe Sala
pytest test_sala.py -v
"""

import pytest
from datetime import datetime, timedelta

# Importações
import sys
sys.path.insert(0, '/mnt/user-data/outputs')

from backend.models.sala import Sala


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sala_valida():
    """Cria uma sala válida para testes."""
    return Sala(
        nome="Consultório 1",
        tipo="Consulta",
        ativa=True
    )


@pytest.fixture
def sala_inativa():
    """Cria uma sala inativa para testes."""
    return Sala(
        nome="Sala Desativada",
        tipo="Manutenção",
        ativa=False
    )


# ============================================================================
# TESTES DO CONSTRUTOR
# ============================================================================

class TestSalaConstructor:
    """Testes do construtor da classe Sala."""
    
    def test_criar_sala_valida(self):
        """Deve criar sala com dados válidos."""
        sala = Sala(
            nome="Sala Cirúrgica",
            tipo="Cirurgia",
            ativa=True
        )
        
        assert sala.nome == "Sala Cirúrgica"
        assert sala.tipo == "Cirurgia"
        assert sala.ativa is True
        assert sala.uuid is not None
    
    def test_sala_ativa_padrao(self):
        """Deve criar sala ativa por padrão."""
        sala = Sala(
            nome="Consultório 2",
            tipo="Consulta"
        )
        
        assert sala.ativa is True
    
    def test_sala_inativa(self):
        """Deve criar sala inativa."""
        sala = Sala(
            nome="Sala em Reforma",
            tipo="Manutenção",
            ativa=False
        )
        
        assert sala.ativa is False
    
    def test_nome_com_espacos_extras(self):
        """Deve remover espaços extras do nome."""
        sala = Sala(
            nome="  Consultório 1  ",
            tipo="  Consulta  "
        )
        
        assert sala.nome == "Consultório 1"
        assert sala.tipo == "Consulta"
    
    def test_tipo_com_espacos_extras(self):
        """Deve remover espaços extras do tipo."""
        sala = Sala(
            nome="Sala 1",
            tipo="  Cirurgia  ",
            ativa=True
        )
        
        assert sala.tipo == "Cirurgia"
    
    def test_uuid_customizado(self):
        """Deve aceitar UUID customizado."""
        uuid_custom = "123e4567-e89b-12d3-a456-426614174000"
        sala = Sala(
            nome="Sala 1",
            tipo="Consulta",
            uuid=uuid_custom
        )
        
        assert sala.uuid == uuid_custom
    
    def test_uuid_gerado_automaticamente(self):
        """Deve gerar UUID automaticamente se não fornecido."""
        sala = Sala(
            nome="Sala 1",
            tipo="Consulta"
        )
        
        assert sala.uuid is not None
        assert len(sala.uuid) == 36
        assert "-" in sala.uuid
    
    def test_erro_nome_vazio(self):
        """Deve falhar com nome vazio."""
        with pytest.raises(ValueError, match="Nome da sala não pode ser vazio"):
            Sala(nome="", tipo="Consulta")
    
    def test_erro_nome_apenas_espacos(self):
        """Deve falhar com nome apenas espaços."""
        with pytest.raises(ValueError, match="Nome da sala não pode ser vazio"):
            Sala(nome="   ", tipo="Consulta")
    
    def test_erro_nome_none(self):
        """Deve falhar com nome None."""
        with pytest.raises((ValueError, AttributeError)):
            Sala(nome=None, tipo="Consulta")
    
    def test_erro_tipo_vazio(self):
        """Deve falhar com tipo vazio."""
        with pytest.raises(ValueError, match="Tipo da sala não pode ser vazio"):
            Sala(nome="Sala 1", tipo="")
    
    def test_erro_tipo_apenas_espacos(self):
        """Deve falhar com tipo apenas espaços."""
        with pytest.raises(ValueError, match="Tipo da sala não pode ser vazio"):
            Sala(nome="Sala 1", tipo="   ")
    
    def test_erro_tipo_none(self):
        """Deve falhar com tipo None."""
        with pytest.raises((ValueError, AttributeError)):
            Sala(nome="Sala 1", tipo=None)
    
    def test_erro_ativa_nao_booleano(self):
        """Deve falhar se ativa não for booleano."""
        with pytest.raises(ValueError, match="Ativa deve ser booleano"):
            Sala(nome="Sala 1", tipo="Consulta", ativa="true")
    
    def test_erro_ativa_string(self):
        """Deve falhar com ativa como string."""
        with pytest.raises(ValueError, match="Ativa deve ser booleano"):
            Sala(nome="Sala 1", tipo="Consulta", ativa="True")
    
    def test_erro_ativa_inteiro(self):
        """Deve falhar com ativa como inteiro."""
        with pytest.raises(ValueError, match="Ativa deve ser booleano"):
            Sala(nome="Sala 1", tipo="Consulta", ativa=1)


# ============================================================================
# TESTES DO MÉTODO statusEm
# ============================================================================

class TestSalaStatusEm:
    """Testes do método statusEm."""
    
    def test_statusEm_sala_livre(self, sala_valida):
        """Deve retornar 'livre' para sala sem reservas."""
        agora = datetime.now()
        status = sala_valida.statusEm(agora)
        
        assert status == "livre"
    
    def test_statusEm_sala_livre_com_lista_vazia(self, sala_valida):
        """Deve retornar 'livre' com lista de reservas vazia."""
        agora = datetime.now()
        status = sala_valida.statusEm(agora, [])
        
        assert status == "livre"
    
    def test_statusEm_sala_bloqueada(self, sala_inativa):
        """Deve retornar 'bloqueada' para sala inativa."""
        agora = datetime.now()
        status = sala_inativa.statusEm(agora)
        
        assert status == "bloqueada"
    
    def test_statusEm_sala_bloqueada_ignora_reservas(self, sala_inativa):
        """Sala inativa deve retornar 'bloqueada' mesmo com reservas."""
        agora = datetime.now()
        
        class ReservaSimulada:
            def __init__(self, inicio, fim):
                self.inicio = inicio
                self.fim = fim
        
        reserva = ReservaSimulada(
            inicio=agora - timedelta(hours=1),
            fim=agora + timedelta(hours=1)
        )
        
        status = sala_inativa.statusEm(agora, [reserva])
        assert status == "bloqueada"
    
    def test_statusEm_sala_ocupada(self, sala_valida):
        """Deve retornar 'ocupada' se há reserva no horário."""
        agora = datetime.now()
        
        class ReservaSimulada:
            def __init__(self, inicio, fim):
                self.inicio = inicio
                self.fim = fim
        
        reserva = ReservaSimulada(
            inicio=agora - timedelta(hours=1),
            fim=agora + timedelta(hours=1)
        )
        
        status = sala_valida.statusEm(agora, [reserva])
        assert status == "ocupada"
    
    def test_statusEm_horario_inicio_reserva(self, sala_valida):
        """Deve retornar 'ocupada' exatamente no início da reserva."""
        agora = datetime.now()
        
        class ReservaSimulada:
            def __init__(self, inicio, fim):
                self.inicio = inicio
                self.fim = fim
        
        reserva = ReservaSimulada(
            inicio=agora,
            fim=agora + timedelta(hours=1)
        )
        
        status = sala_valida.statusEm(agora, [reserva])
        assert status == "ocupada"
    
    def test_statusEm_horario_fim_reserva(self, sala_valida):
        """Deve retornar 'ocupada' exatamente no fim da reserva."""
        agora = datetime.now()
        
        class ReservaSimulada:
            def __init__(self, inicio, fim):
                self.inicio = inicio
                self.fim = fim
        
        reserva = ReservaSimulada(
            inicio=agora - timedelta(hours=1),
            fim=agora
        )
        
        status = sala_valida.statusEm(agora, [reserva])
        assert status == "ocupada"
    
    def test_statusEm_fora_horario_reserva_passado(self, sala_valida):
        """Deve retornar 'livre' se fora do horário (reserva passou)."""
        agora = datetime.now()
        
        class ReservaSimulada:
            def __init__(self, inicio, fim):
                self.inicio = inicio
                self.fim = fim
        
        reserva = ReservaSimulada(
            inicio=agora - timedelta(hours=3),
            fim=agora - timedelta(hours=2)
        )
        
        status = sala_valida.statusEm(agora, [reserva])
        assert status == "livre"
    
    def test_statusEm_fora_horario_reserva_futuro(self, sala_valida):
        """Deve retornar 'livre' se fora do horário (reserva futura)."""
        agora = datetime.now()
        
        class ReservaSimulada:
            def __init__(self, inicio, fim):
                self.inicio = inicio
                self.fim = fim
        
        reserva = ReservaSimulada(
            inicio=agora + timedelta(hours=2),
            fim=agora + timedelta(hours=3)
        )
        
        status = sala_valida.statusEm(agora, [reserva])
        assert status == "livre"
    
    def test_statusEm_multiplas_reservas_nenhuma_agora(self, sala_valida):
        """Deve verificar múltiplas reservas e retornar 'livre'."""
        agora = datetime.now()
        
        class ReservaSimulada:
            def __init__(self, inicio, fim):
                self.inicio = inicio
                self.fim = fim
        
        reservas = [
            ReservaSimulada(
                inicio=agora - timedelta(hours=5),
                fim=agora - timedelta(hours=4)
            ),
            ReservaSimulada(
                inicio=agora + timedelta(hours=2),
                fim=agora + timedelta(hours=3)
            ),
            ReservaSimulada(
                inicio=agora + timedelta(hours=5),
                fim=agora + timedelta(hours=6)
            )
        ]
        
        status = sala_valida.statusEm(agora, reservas)
        assert status == "livre"
    
    def test_statusEm_multiplas_reservas_uma_agora(self, sala_valida):
        """Deve encontrar reserva atual entre múltiplas."""
        agora = datetime.now()
        
        class ReservaSimulada:
            def __init__(self, inicio, fim):
                self.inicio = inicio
                self.fim = fim
        
        reservas = [
            ReservaSimulada(
                inicio=agora - timedelta(hours=5),
                fim=agora - timedelta(hours=4)
            ),
            ReservaSimulada(
                inicio=agora - timedelta(minutes=30),
                fim=agora + timedelta(minutes=30)
            ),
            ReservaSimulada(
                inicio=agora + timedelta(hours=2),
                fim=agora + timedelta(hours=3)
            )
        ]
        
        status = sala_valida.statusEm(agora, reservas)
        assert status == "ocupada"
    
    def test_statusEm_reserva_sem_atributos(self, sala_valida):
        """Deve ignorar reservas sem atributos inicio/fim."""
        agora = datetime.now()
        
        class ReservaInvalida:
            pass
        
        reservas = [ReservaInvalida()]
        status = sala_valida.statusEm(agora, reservas)
        
        assert status == "livre"
    
    def test_statusEm_reserva_apenas_inicio(self, sala_valida):
        """Deve ignorar reserva com apenas inicio."""
        agora = datetime.now()
        
        class ReservaParcial:
            def __init__(self):
                self.inicio = agora
        
        reservas = [ReservaParcial()]
        status = sala_valida.statusEm(agora, reservas)
        
        assert status == "livre"
    
    def test_statusEm_reserva_apenas_fim(self, sala_valida):
        """Deve ignorar reserva com apenas fim."""
        agora = datetime.now()
        
        class ReservaParcial:
            def __init__(self):
                self.fim = agora
        
        reservas = [ReservaParcial()]
        status = sala_valida.statusEm(agora, reservas)
        
        assert status == "livre"
    
    def test_statusEm_reservas_sobrepostas(self, sala_valida):
        """Deve retornar 'ocupada' com reservas sobrepostas."""
        agora = datetime.now()
        
        class ReservaSimulada:
            def __init__(self, inicio, fim):
                self.inicio = inicio
                self.fim = fim
        
        # Duas reservas sobrepostas cobrindo o horário atual
        reservas = [
            ReservaSimulada(
                inicio=agora - timedelta(hours=2),
                fim=agora + timedelta(minutes=30)
            ),
            ReservaSimulada(
                inicio=agora - timedelta(minutes=30),
                fim=agora + timedelta(hours=2)
            )
        ]
        
        status = sala_valida.statusEm(agora, reservas)
        assert status == "ocupada"


# ============================================================================
# TESTES DE SERIALIZAÇÃO
# ============================================================================

class TestSalaSerializacao:
    """Testes de to_dict."""
    
    def test_to_dict_completo(self, sala_valida):
        """Deve converter para dicionário completo."""
        dados = sala_valida.to_dict()
        
        assert isinstance(dados, dict)
        assert dados["uuid"] == sala_valida.uuid
        assert dados["nome"] == sala_valida.nome
        assert dados["tipo"] == sala_valida.tipo
        assert dados["ativa"] == sala_valida.ativa
    
    def test_to_dict_sala_ativa(self, sala_valida):
        """Deve indicar sala ativa no dict."""
        dados = sala_valida.to_dict()
        assert dados["ativa"] is True
    
    def test_to_dict_sala_inativa(self, sala_inativa):
        """Deve indicar sala inativa no dict."""
        dados = sala_inativa.to_dict()
        assert dados["ativa"] is False
    
    def test_to_dict_tipos_corretos(self, sala_valida):
        """Deve ter tipos corretos no dicionário."""
        dados = sala_valida.to_dict()
        
        assert isinstance(dados["uuid"], str)
        assert isinstance(dados["nome"], str)
        assert isinstance(dados["tipo"], str)
        assert isinstance(dados["ativa"], bool)
    
    def test_repr_legivel(self, sala_valida):
        """Deve ter repr legível."""
        repr_str = repr(sala_valida)
        
        assert "Sala" in repr_str
        assert sala_valida.nome in repr_str
        assert sala_valida.tipo in repr_str
    
    def test_repr_contem_status(self, sala_valida):
        """Deve incluir status ativa no repr."""
        repr_str = repr(sala_valida)
        assert "ativa=" in repr_str
        assert "True" in repr_str or "False" in repr_str


# ============================================================================
# TESTES DE CASOS ESPECIAIS
# ============================================================================

class TestSalaCasosEspeciais:
    """Testes de casos especiais e edge cases."""
    
    def test_nome_muito_longo(self):
        """Deve aceitar nome muito longo."""
        nome_longo = "Sala " + "A" * 200
        sala = Sala(
            nome=nome_longo,
            tipo="Especial"
        )
        
        assert sala.nome == nome_longo
    
    def test_tipo_muito_longo(self):
        """Deve aceitar tipo muito longo."""
        tipo_longo = "Tipo " + "B" * 200
        sala = Sala(
            nome="Sala 1",
            tipo=tipo_longo
        )
        
        assert sala.tipo == tipo_longo
    
    def test_nome_com_caracteres_especiais(self):
        """Deve aceitar nome com caracteres especiais."""
        sala = Sala(
            nome="Consultório São João - Ala Norte",
            tipo="Consulta"
        )
        
        assert "São" in sala.nome
        assert "-" in sala.nome
    
    def test_tipo_com_caracteres_especiais(self):
        """Deve aceitar tipo com caracteres especiais."""
        sala = Sala(
            nome="Sala 1",
            tipo="Cirurgia Ortopédica & Traumatologia"
        )
        
        assert "&" in sala.tipo
    
    def test_multiplas_salas_uuids_diferentes(self):
        """Deve gerar UUIDs diferentes para cada sala."""
        salas = [
            Sala(f"Sala {i}", "Consulta")
            for i in range(10)
        ]
        
        uuids = [s.uuid for s in salas]
        assert len(set(uuids)) == 10
    
    def test_reserva_de_um_minuto(self, sala_valida):
        """Deve lidar com reserva muito curta."""
        agora = datetime.now()
        
        class ReservaSimulada:
            def __init__(self, inicio, fim):
                self.inicio = inicio
                self.fim = fim
        
        reserva = ReservaSimulada(
            inicio=agora,
            fim=agora + timedelta(minutes=1)
        )
        
        status = sala_valida.statusEm(agora, [reserva])
        assert status == "ocupada"
    
    def test_reserva_de_varios_dias(self, sala_valida):
        """Deve lidar com reserva muito longa."""
        agora = datetime.now()
        
        class ReservaSimulada:
            def __init__(self, inicio, fim):
                self.inicio = inicio
                self.fim = fim
        
        reserva = ReservaSimulada(
            inicio=agora - timedelta(days=1),
            fim=agora + timedelta(days=1)
        )
        
        status = sala_valida.statusEm(agora, [reserva])
        assert status == "ocupada"


# ============================================================================
# TESTES DE INTEGRAÇÃO
# ============================================================================

class TestSalaIntegracao:
    """Testes de integração e casos de uso reais."""
    
    def test_fluxo_agendamento_simples(self):
        """Testa fluxo básico de agendamento."""
        # Criar sala
        sala = Sala("Consultório 1", "Consulta", ativa=True)
        
        # Verificar disponibilidade agora
        agora = datetime.now()
        assert sala.statusEm(agora) == "livre"
        
        # Simular agendamento
        class Agendamento:
            def __init__(self, inicio, fim):
                self.inicio = inicio
                self.fim = fim
        
        agendamento = Agendamento(
            inicio=agora,
            fim=agora + timedelta(hours=1)
        )
        
        # Verificar sala ocupada
        assert sala.statusEm(agora, [agendamento]) == "ocupada"
        
        # Verificar sala livre após agendamento
        depois = agora + timedelta(hours=2)
        assert sala.statusEm(depois, [agendamento]) == "livre"
    
    def test_sala_com_multiplos_agendamentos_dia(self):
        """Testa sala com vários agendamentos no dia."""
        sala = Sala("Consultório 2", "Consulta", ativa=True)
        
        base = datetime(2025, 11, 20, 8, 0)  # 08:00
        
        class Agendamento:
            def __init__(self, inicio, fim):
                self.inicio = inicio
                self.fim = fim
        
        # Agendamentos do dia
        agendamentos = [
            Agendamento(base, base + timedelta(hours=1)),           # 08:00-09:00
            Agendamento(base + timedelta(hours=2), base + timedelta(hours=3)),   # 10:00-11:00
            Agendamento(base + timedelta(hours=4), base + timedelta(hours=5)),   # 12:00-13:00
        ]
        
        # Testa vários horários
        assert sala.statusEm(base + timedelta(minutes=30), agendamentos) == "ocupada"  # 08:30
        assert sala.statusEm(base + timedelta(hours=1, minutes=30), agendamentos) == "livre"  # 09:30
        assert sala.statusEm(base + timedelta(hours=2, minutes=30), agendamentos) == "ocupada"  # 10:30
        assert sala.statusEm(base + timedelta(hours=6), agendamentos) == "livre"  # 14:00


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])