import psycopg2
import psycopg2.extras
import os

class Conexao:

    # Inicializa a configuração de conexão, pode usar string ou variáveis de ambiente.
    def __init__(self, conn_str=None):
        if conn_str:
            # Exemplo: "dbname='agendavta' user='postgres' password='123' host='localhost' port='5432'"
            self.conn_str = conn_str
            self.db_config = None
        else:
            # Usa variáveis de ambiente
            self.conn_str = None
            self.db_config = {
                "dbname": os.getenv("DB_NAME", "agendavta"),
                "user": os.getenv("DB_USER", "postgres"),
                "password": os.getenv("DB_PASSWORD", "postgres"),
                "host": os.getenv("DB_HOST", "localhost"),
                "port": os.getenv("DB_PORT", "5432"),
            }

    # Abre uma conexão com o banco de dados PostgreSQL.
    def _get_conn(self):
        if self.conn_str:
            # Conecta usando string de conexão direta
            return psycopg2.connect(self.conn_str, cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            # Conecta usando dicionário de configuração
            return psycopg2.connect(**self.db_config, cursor_factory=psycopg2.extras.RealDictCursor)