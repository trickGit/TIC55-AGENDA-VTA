from backend.DB.conexao import Conexao
from backend.models.sala import Sala
from datetime import datetime

class SalaServico(Conexao):
    """
    Serviço responsável pelo gerenciamento de salas.
    
    Contém toda a lógica de negócio relacionada a salas:
    - CRUD completo
    - Ativação/desativação
    - Consulta de disponibilidade
    - Integração com agendamentos
    """
    
    def criar_sala(self, nome: str, tipo: str, ativa: bool = True) -> Sala | None:
        """
        Cria uma nova sala no sistema.
        
        Args:
            nome: Nome ou número da sala
            tipo: Tipo de sala
            ativa: Se a sala inicia ativa
            
        Returns:
            Sala criada ou None se falhar
        """
        try:
            sala = Sala(nome=nome, tipo=tipo, ativa=ativa)
        except ValueError as e:
            print(f"Erro de validação: {e}")
            return None
        
        with self._get_conn() as conn, conn.cursor() as cur:
            # Verifica se já existe sala com esse nome
            cur.execute("SELECT uuid FROM sala WHERE nome = %s;", (sala.nome,))
            if cur.fetchone():
                print(f"Já existe uma sala com o nome '{sala.nome}'")
                return None
            
            # Insere sala
            cur.execute("""
                INSERT INTO sala (uuid, nome, tipo, ativa)
                VALUES (%s, %s, %s, %s);
            """, (sala.uuid, sala.nome, sala.tipo, sala.ativa))
            
            conn.commit()
            print(f"✓ Sala '{sala.nome}' criada com sucesso!")
            return sala
    
    def buscar_sala(self, sala_uuid: str) -> Sala | None:
        """
        Busca uma sala por UUID.
        
        Args:
            sala_uuid: UUID da sala
            
        Returns:
            Sala encontrada ou None
        """
        with self._get_conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM sala WHERE uuid = %s;", (sala_uuid,))
            row = cur.fetchone()
            
            if not row:
                return None
            
            return Sala(
                uuid=row["uuid"],
                nome=row["nome"],
                tipo=row["tipo"],
                ativa=row["ativa"]
            )
    
    def buscar_sala_por_nome(self, nome: str) -> Sala | None:
        """
        Busca uma sala por nome.
        
        Args:
            nome: Nome da sala
            
        Returns:
            Sala encontrada ou None
        """
        with self._get_conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM sala WHERE nome = %s;", (nome,))
            row = cur.fetchone()
            
            if not row:
                return None
            
            return Sala(
                uuid=row["uuid"],
                nome=row["nome"],
                tipo=row["tipo"],
                ativa=row["ativa"]
            )
    
    def listar_salas(self, apenas_ativas: bool = False) -> list[Sala]:
        """
        Lista todas as salas.
        
        Args:
            apenas_ativas: Se True, retorna apenas salas ativas
            
        Returns:
            Lista de salas
        """
        with self._get_conn() as conn, conn.cursor() as cur:
            if apenas_ativas:
                cur.execute("SELECT * FROM sala WHERE ativa = TRUE ORDER BY nome;")
            else:
                cur.execute("SELECT * FROM sala ORDER BY nome;")
            
            salas = []
            for row in cur.fetchall():
                sala = Sala(
                    uuid=row["uuid"],
                    nome=row["nome"],
                    tipo=row["tipo"],
                    ativa=row["ativa"]
                )
                salas.append(sala)
            
            return salas
    
    def atualizar_sala(self, sala_uuid: str, nome: str = None, 
                       tipo: str = None) -> bool:
        """
        Atualiza dados de uma sala.
        
        Args:
            sala_uuid: UUID da sala
            nome: Novo nome (None para manter)
            tipo: Novo tipo (None para manter)
            
        Returns:
            True se atualizado, False caso contrário
        """
        campos = []
        valores = []
        
        if nome is not None:
            campos.append("nome = %s")
            valores.append(nome)
        
        if tipo is not None:
            campos.append("tipo = %s")
            valores.append(tipo)
        
        if not campos:
            print("Nenhum campo para atualizar")
            return False
        
        valores.append(sala_uuid)
        query = f"UPDATE sala SET {', '.join(campos)} WHERE uuid = %s;"
        
        with self._get_conn() as conn, conn.cursor() as cur:
            cur.execute(query, valores)
            
            if cur.rowcount == 0:
                print(f"Sala {sala_uuid} não encontrada")
                return False
            
            conn.commit()
            print(f"✓ Sala atualizada com sucesso!")
            return True
    
    def ativar_sala(self, sala_uuid: str) -> bool:
        """
        Ativa uma sala.
        
        Args:
            sala_uuid: UUID da sala
            
        Returns:
            True se ativada, False caso contrário
        """
        with self._get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE sala SET ativa = TRUE WHERE uuid = %s;",
                (sala_uuid,)
            )
            
            if cur.rowcount == 0:
                print(f"Sala {sala_uuid} não encontrada")
                return False
            
            conn.commit()
            print(f"✓ Sala ativada com sucesso!")
            return True
    
    def desativar_sala(self, sala_uuid: str) -> bool:
        """
        Desativa uma sala.
        
        Args:
            sala_uuid: UUID da sala
            
        Returns:
            True se desativada, False caso contrário
        """
        with self._get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE sala SET ativa = FALSE WHERE uuid = %s;",
                (sala_uuid,)
            )
            
            if cur.rowcount == 0:
                print(f"Sala {sala_uuid} não encontrada")
                return False
            
            conn.commit()
            print(f"✓ Sala desativada com sucesso!")
            return True
    
    def excluir_sala(self, sala_uuid: str) -> bool:
        """
        Exclui uma sala (hard delete).
        
        Args:
            sala_uuid: UUID da sala
            
        Returns:
            True se excluída, False caso contrário
            
        Warning:
            Verifica se há agendamentos antes de excluir
        """
        with self._get_conn() as conn, conn.cursor() as cur:
            # Verifica se há agendamentos
            cur.execute("""
                SELECT COUNT(*) as total 
                FROM agendamento 
                WHERE fk_sala_uuid = %s;
            """, (sala_uuid,))
            
            resultado = cur.fetchone()
            if resultado and resultado["total"] > 0:
                print(f"Não é possível excluir: sala possui {resultado['total']} agendamento(s)")
                return False
            
            # Exclui sala
            cur.execute("DELETE FROM sala WHERE uuid = %s;", (sala_uuid,))
            
            if cur.rowcount == 0:
                print(f"Sala {sala_uuid} não encontrada")
                return False
            
            conn.commit()
            print(f"✓ Sala excluída com sucesso!")
            return True
    
    def consultar_disponibilidade(self, sala_uuid: str, 
                                  dataHora: datetime) -> str:
        """
        Consulta disponibilidade de uma sala em um horário.
        
        Args:
            sala_uuid: UUID da sala
            dataHora: Data/hora para verificar
            
        Returns:
            'bloqueada', 'ocupada', 'livre' ou 'sala_nao_encontrada'
        """
        sala = self.buscar_sala(sala_uuid)
        if not sala:
            return "sala_nao_encontrada"
        
        # Busca reservas/agendamentos da sala nesse horário
        with self._get_conn() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT inicio, fim 
                FROM agendamento 
                WHERE fk_sala_uuid = %s 
                  AND status != 'CANCELADO'
                  AND %s BETWEEN inicio AND fim;
            """, (sala_uuid, dataHora))
            
            reservas = cur.fetchall()
        
        return sala.statusEm(dataHora, reservas)
    
    def listar_salas_disponiveis(self, dataHora: datetime) -> list[Sala]:
        """
        Lista salas disponíveis em um horário específico.
        
        Args:
            dataHora: Data/hora para verificar
            
        Returns:
            Lista de salas livres
        """
        salas_ativas = self.listar_salas(apenas_ativas=True)
        salas_livres = []
        
        for sala in salas_ativas:
            status = self.consultar_disponibilidade(sala.uuid, dataHora)
            if status == "livre":
                salas_livres.append(sala)
        
        return salas_livres
