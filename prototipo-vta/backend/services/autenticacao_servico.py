from datetime import datetime, timezone, timedelta
from uuid import UUID
import os
from backend.enums.perfil_usuario import PerfilUsuario
from backend.enums.status_usuario import StatusUsuario
from backend.models.usuario import Usuario
from backend.DB.conexao import Conexao

class AutenticacaoServico(Conexao):
    """
    Serviço responsável por autenticação, gerenciamento de senhas e tokens.
    
    Utiliza o sistema de hash do Usuario (PBKDF2 com 600k iterações).
    """

    # Configurações de token
    TOKEN_EXPIRACAO_MINUTOS = 30
    TOKEN_TAMANHO_BYTES = 32  # 64 caracteres hex

    def sessao_login(self, email: str, senha: str) -> Usuario | None:
        """
        Realiza login do usuário.
        
        Args:
            email: Email do usuário
            senha: Senha em texto plano
            
        Returns:
            Usuario se autenticado com sucesso, None caso contrário
            
        Notes:
            - Valida email, senha e status do usuário
            - Atualiza campo ultimo_login se existir
            - Mensagens genéricas para não revelar se email existe
        """
        if not email or not senha:
            print("Credenciais inválidas.")
            return None

        with self._get_conn() as conn, conn.cursor() as cur:
            # Busca usuário por email
            cur.execute(
                "SELECT * FROM usuario WHERE email = %s;", 
                (email.strip().lower(),)
            )
            usuario_row = cur.fetchone()

            # Validações (mensagem genérica para não revelar se email existe)
            if not usuario_row:
                print("Credenciais inválidas.")
                return None

            # Valida senha usando o método do Usuario
            if not Usuario.validar_senha(usuario_row["senhahash"], senha):
                print("Credenciais inválidas.")
                return None

            # Verifica se usuário está ativo
            status = StatusUsuario(usuario_row["status"])
            if status != StatusUsuario.ATIVO:
                print("Usuário inativo. Contate o administrador.")
                return None

            # Atualiza último login (se o campo existir na tabela)
            try:
                cur.execute(
                    "UPDATE usuario SET ultimo_login = %s WHERE idusuario = %s;",
                    (datetime.now(timezone.utc), usuario_row["idusuario"])
                )
                conn.commit()
            except Exception as e:
                # Campo ultimo_login pode não existir na tabela
                print(f"Aviso: não foi possível atualizar último login: {e}")

            print(f"Usuário {usuario_row['nome']} logado com sucesso!")

            # Cria objeto Usuario a partir dos dados do banco
            usuario = self._criar_usuario_from_row(usuario_row)
            return usuario

    def _criar_usuario_from_row(self, row: dict) -> Usuario:
        """
        Cria objeto Usuario a partir de uma linha do banco.
        
        Args:
            row: Dicionário com dados do banco (fetchone())
            
        Returns:
            Instância de Usuario
        """
        # Parse do último login se existir
        ultimo_login = None
        if "ultimo_login" in row and row["ultimo_login"]:
            ultimo_login = row["ultimo_login"]
            if isinstance(ultimo_login, str):
                ultimo_login = datetime.fromisoformat(ultimo_login)
            # Garante timezone UTC
            if ultimo_login and ultimo_login.tzinfo is None:
                ultimo_login = ultimo_login.replace(tzinfo=timezone.utc)

        # Cria usuário
        return Usuario(
            uuid=UUID(row["uuid"]) if row.get("uuid") else None,
            nome=row["nome"],
            email=row["email"],
            senha_hash=row["senhahash"],
            perfil=PerfilUsuario(row["perfil"]),
            status=StatusUsuario(row["status"]),
            ultimo_login=ultimo_login
        )

    def criar_usuario(self, nome: str, email: str, senha: str,perfil: PerfilUsuario = PerfilUsuario.RECEPCIONISTA) -> Usuario | None:
        """
        Cria novo usuário no sistema.
        
        Args:
            nome: Nome completo
            email: Email único
            senha: Senha em texto plano (será hashada)
            perfil: Perfil de permissões
            
        Returns:
            Usuario criado ou None se falhar
            
        Raises:
            ValueError: Se dados inválidos
        """
        # Validações básicas
        if not nome or not email or not senha:
            raise ValueError("Nome, email e senha são obrigatórios")
        
        if len(senha) < 8:
            raise ValueError("Senha deve ter no mínimo 8 caracteres")

        # Gera hash da senha usando o método do Usuario
        senha_hash = Usuario.hash_senha(senha)

        # Cria usuário (validações feitas no construtor)
        usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            perfil=perfil,
            status=StatusUsuario.ATIVO
        )

        # Insere no banco
        with self._get_conn() as conn, conn.cursor() as cur:
            # Verifica se email já existe
            cur.execute(
                "SELECT idusuario FROM usuario WHERE email = %s;",
                (usuario.email,)
            )
            if cur.fetchone():
                print(f"Email {usuario.email} já cadastrado.")
                return None

            # Insere usuário
            cur.execute("""
                INSERT INTO usuario (uuid, nome, email, senhahash, perfil, status, ultimo_login)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING idusuario;
            """, (
                usuario.uuid,
                usuario.nome,
                usuario.email,
                usuario.senha_hash,
                usuario.perfil.value,
                usuario.status.value,
                None  # ultimo_login = NULL inicialmente
            ))
            
            usuario_id = cur.fetchone()["idusuario"]
            conn.commit()
            
            print(f"Usuário {usuario.nome} criado com sucesso! ID: {usuario_id}")
            return usuario

    def alterar_senha(self, email: str, senha_atual: str, senha_nova: str) -> bool:
        """
        Altera senha do usuário (requer senha atual).
        
        Args:
            email: Email do usuário
            senha_atual: Senha atual para validação
            senha_nova: Nova senha em texto plano
            
        Returns:
            True se senha foi alterada, False caso contrário
        """
        if not email or not senha_atual or not senha_nova:
            print("Todos os campos são obrigatórios.")
            return False

        if len(senha_nova) < 8:
            print("Nova senha deve ter no mínimo 8 caracteres.")
            return False

        with self._get_conn() as conn, conn.cursor() as cur:
            # Busca usuário
            cur.execute(
                "SELECT idusuario, senhahash FROM usuario WHERE email = %s;",
                (email.strip().lower(),)
            )
            usuario_row = cur.fetchone()

            if not usuario_row:
                print("Usuário não encontrado.")
                return False

            # Valida senha atual
            if not Usuario.validar_senha(usuario_row["senhahash"], senha_atual):
                print("Senha atual incorreta.")
                return False

            # Gera novo hash
            novo_hash = Usuario.hash_senha(senha_nova)

            # Atualiza no banco
            cur.execute(
                "UPDATE usuario SET senhahash = %s WHERE idusuario = %s;",
                (novo_hash, usuario_row["idusuario"])
            )
            conn.commit()

            print("Senha alterada com sucesso.")
            return True

    def solicitar_recuperacao_senha(self, email: str) -> str | None:
        """
        Gera token de recuperação de senha.
        
        Args:
            email: Email do usuário
            
        Returns:
            Token gerado (64 chars hex) ou None se email não encontrado
            
        Notes:
            - Token expira em 30 minutos
            - Não revela se email existe (sempre retorna mensagem de sucesso)
            - Em produção, enviar token por email em vez de retornar
        """
        if not email:
            print("Email é obrigatório.")
            return None

        email = email.strip().lower()

        with self._get_conn() as conn, conn.cursor() as cur:
            # Busca usuário
            cur.execute(
                "SELECT idusuario FROM usuario WHERE email = %s;", 
                (email,)
            )
            usuario = cur.fetchone()
            
            # Não revela se email existe (segurança)
            if not usuario:
                print(f"Se o email {email} estiver cadastrado, você receberá instruções de recuperação.")
                return None

            # Gera token seguro
            token = os.urandom(self.TOKEN_TAMANHO_BYTES).hex()
            expira_em = datetime.now(timezone.utc) + timedelta(minutes=self.TOKEN_EXPIRACAO_MINUTOS)

            # Insere token no banco
            cur.execute("""
                INSERT INTO tokenrecuperacao 
                    (token, expiraem, utilizado, fk_usuario_idusuario)
                VALUES (%s, %s, FALSE, %s);
            """, (token, expira_em, usuario["idusuario"]))
            
            conn.commit()

            print(f"Token de recuperação gerado para {email}")
            print(f"Token: {token} (expira às {expira_em.isoformat()})")
            
            # TODO: Em produção, enviar token por email em vez de printar
            # self._enviar_email_recuperacao(email, token)
            
            return token

    def redefinir_senha(self, token: str, nova_senha: str) -> bool:
        """
        Redefine senha usando token de recuperação.
        
        Args:
            token: Token de recuperação (64 chars hex)
            nova_senha: Nova senha em texto plano
            
        Returns:
            True se senha foi redefinida, False caso contrário
        """
        if not token or not nova_senha:
            print("Token e nova senha são obrigatórios.")
            return False

        if len(nova_senha) < 8:
            print("Nova senha deve ter no mínimo 8 caracteres.")
            return False

        with self._get_conn() as conn, conn.cursor() as cur:
            # Busca token
            cur.execute("""
                SELECT t.idtoken, t.expiraem, t.utilizado, u.idusuario
                FROM tokenrecuperacao t
                JOIN usuario u ON u.idusuario = t.fk_usuario_idusuario
                WHERE t.token = %s;
            """, (token,))
            
            meta = cur.fetchone()

            # Validações (mensagens genéricas por segurança)
            if not meta:
                print("Token inválido ou expirado.")
                return False
                
            if meta["utilizado"]:
                print("Token inválido ou expirado.")
                return False

            # Verifica expiração
            expira_em = meta["expiraem"]
            if expira_em.tzinfo is None:
                expira_em = expira_em.replace(tzinfo=timezone.utc)
                
            if expira_em <= datetime.now(timezone.utc):
                print("Token inválido ou expirado.")
                return False

            # Gera novo hash usando método do Usuario
            novo_hash = Usuario.hash_senha(nova_senha)
            
            # Atualiza senha e marca token como utilizado
            cur.execute(
                "UPDATE usuario SET senhahash = %s WHERE idusuario = %s;",
                (novo_hash, meta["idusuario"])
            )
            cur.execute(
                "UPDATE tokenrecuperacao SET utilizado = TRUE WHERE idtoken = %s;",
                (meta["idtoken"],)
            )
            
            conn.commit()
            print("Senha redefinida com sucesso.")
            return True

    def invalidar_tokens_usuario(self, usuario_id: int) -> int:
        """
        Invalida todos os tokens de recuperação ativos de um usuário.
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            Número de tokens invalidados
            
        Notes:
            Útil para casos de segurança (conta comprometida, etc)
        """
        with self._get_conn() as conn, conn.cursor() as cur:
            cur.execute("""
                UPDATE tokenrecuperacao 
                SET utilizado = TRUE 
                WHERE fk_usuario_idusuario = %s 
                  AND utilizado = FALSE 
                  AND expiraem > %s;
            """, (usuario_id, datetime.now(timezone.utc)))
            
            tokens_invalidados = cur.rowcount
            conn.commit()
            
            print(f"{tokens_invalidados} token(s) invalidado(s) para usuário {usuario_id}.")
            return tokens_invalidados

    def limpar_tokens_expirados(self) -> int:
        """
        Remove tokens expirados do banco (manutenção).
        
        Returns:
            Número de tokens removidos
            
        Notes:
            Executar periodicamente (cron job, etc)
        """
        with self._get_conn() as conn, conn.cursor() as cur:
            cur.execute("""
                DELETE FROM tokenrecuperacao 
                WHERE expiraem < %s;
            """, (datetime.now(timezone.utc),))
            
            tokens_removidos = cur.rowcount
            conn.commit()
            
            print(f"{tokens_removidos} token(s) expirado(s) removido(s).")
            return tokens_removidos

    def verificar_email_disponivel(self, email: str) -> bool:
        """
        Verifica se um email está disponível para cadastro.
        
        Args:
            email: Email para verificar
            
        Returns:
            True se disponível, False se já cadastrado
        """
        if not email:
            return False

        with self._get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM usuario WHERE email = %s LIMIT 1;",
                (email.strip().lower(),)
            )
            return cur.fetchone() is None

    def listar_usuarios_ativos(self) -> list[Usuario]:
        """
        Lista todos os usuários ativos.
        
        Returns:
            Lista de objetos Usuario ativos
        """
        with self._get_conn() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM usuario 
                WHERE status = %s 
                ORDER BY nome;
            """, (StatusUsuario.ATIVO.value,))
            
            usuarios = []
            for row in cur.fetchall():
                try:
                    usuario = self._criar_usuario_from_row(row)
                    usuarios.append(usuario)
                except Exception as e:
                    print(f"Erro ao criar usuário {row.get('email')}: {e}")
                    continue
            
            return usuarios

    def atualizar_perfil_usuario(self, email: str, novo_perfil: PerfilUsuario) -> bool:
        """
        Atualiza o perfil de um usuário.
        
        Args:
            email: Email do usuário
            novo_perfil: Novo perfil
            
        Returns:
            True se atualizado com sucesso, False caso contrário
        """
        if not isinstance(novo_perfil, PerfilUsuario):
            print("Perfil inválido.")
            return False

        with self._get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE usuario SET perfil = %s WHERE email = %s;",
                (novo_perfil.value, email.strip().lower())
            )
            
            if cur.rowcount == 0:
                print(f"Usuário {email} não encontrado.")
                return False
            
            conn.commit()
            print(f"Perfil de {email} atualizado para {novo_perfil.value}.")
            return True

    def desativar_usuario(self, email: str) -> bool:
        """
        Desativa um usuário (soft delete).
        
        Args:
            email: Email do usuário
            
        Returns:
            True se desativado com sucesso, False caso contrário
        """
        with self._get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE usuario SET status = %s WHERE email = %s;",
                (StatusUsuario.INATIVO.value, email.strip().lower())
            )
            
            if cur.rowcount == 0:
                print(f"Usuário {email} não encontrado.")
                return False
            
            conn.commit()
            print(f"Usuário {email} desativado.")
            return True

    def reativar_usuario(self, email: str) -> bool:
        """
        Reativa um usuário desativado.
        
        Args:
            email: Email do usuário
            
        Returns:
            True se reativado com sucesso, False caso contrário
        """
        with self._get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE usuario SET status = %s WHERE email = %s;",
                (StatusUsuario.ATIVO.value, email.strip().lower())
            )
            
            if cur.rowcount == 0:
                print(f"Usuário {email} não encontrado.")
                return False
            
            conn.commit()
            print(f"Usuário {email} reativado.")
            return True