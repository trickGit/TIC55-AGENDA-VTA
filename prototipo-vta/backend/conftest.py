"""
Configuração do pytest para o projeto TIC55-AGENDA-VTA.

Este arquivo deve estar na RAIZ do projeto (ao lado da pasta prototipo-vta).
Ele configura automaticamente o PYTHONPATH para que os testes encontrem o módulo backend.

Estrutura esperada:
    TIC55-AGENDA-VTA/
    ├── conftest.py              ← ESTE ARQUIVO
    └── prototipo-vta/
        └── backend/
            ├── __init__.py
            ├── models/
            ├── services/
            └── tests/
"""

import sys
from pathlib import Path

# ============================================================================
# CONFIGURAÇÃO DO PYTHONPATH
# ============================================================================

# Diretório raiz do projeto (onde está este conftest.py)
ROOT_DIR = Path(__file__).parent

# Diretório onde está o módulo backend
BACKEND_DIR = ROOT_DIR / "prototipo-vta"

# Adiciona ao PYTHONPATH se ainda não estiver
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
    print(f"✓ PYTHONPATH configurado: {BACKEND_DIR}")


# ============================================================================
# CONFIGURAÇÃO DO PYTEST
# ============================================================================

def pytest_configure(config):
    """
    Hook executado antes dos testes iniciarem.
    Configura marcadores customizados.
    """
    # Marcadores para categorizar testes
    config.addinivalue_line(
        "markers", 
        "unit: marca testes unitários (classes isoladas)"
    )
    config.addinivalue_line(
        "markers", 
        "integration: marca testes de integração (com banco/mocks)"
    )
    config.addinivalue_line(
        "markers", 
        "slow: marca testes lentos (>1 segundo)"
    )
    config.addinivalue_line(
        "markers", 
        "database: marca testes que requerem banco de dados"
    )


def pytest_collection_modifyitems(config, items):
    """
    Hook executado após coletar os testes.
    Pode modificar/filtrar testes antes da execução.
    """
    # Adiciona marcador 'unit' automaticamente para testes que não têm marcadores
    for item in items:
        if not any(item.iter_markers()):
            item.add_marker("unit")


# ============================================================================
# FIXTURES GLOBAIS (OPCIONAL)
# ============================================================================

import pytest
from datetime import datetime, timezone

@pytest.fixture
def data_atual():
    """Retorna data/hora atual em UTC."""
    return datetime.now(timezone.utc)


@pytest.fixture
def limpar_cache():
    """Limpa caches após cada teste."""
    yield
    # Código de limpeza aqui (se necessário)
    pass


# ============================================================================
# CONFIGURAÇÃO DE LOGGING (OPCIONAL)
# ============================================================================

import logging

def pytest_sessionstart(session):
    """Executado no início da sessão de testes."""
    # Configura logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("\n" + "="*70)
    print("🧪 INICIANDO TESTES DO SISTEMA VETERINÁRIO")
    print("="*70 + "\n")


def pytest_sessionfinish(session, exitstatus):
    """Executado no final da sessão de testes."""
    print("\n" + "="*70)
    print("✨ TESTES CONCLUÍDOS")
    print("="*70 + "\n")
