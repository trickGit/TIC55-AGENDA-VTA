# Importações necessárias
import os  # Para funções do sistema operacional, usado para gerar salt aleatório
import hashlib  # Para funções de hash criptográfico
import hmac  # Para comparação segura de strings
from datetime import datetime, timezone, timedelta  # Adicionado timezone para datas UTC corretas
from uuid import uuid4, UUID  # Para gerar UUIDs únicos e converter valores do banco
from backend.enums.perfil_usuario import PerfilUsuario  # Importa enumeração de perfis de usuário
from backend.models.usuario import Usuario  # Importa a classe Usuario
from backend.DB.conexao import Conexao  # Classe responsável pela conexão com o banco de dados


# Classe de serviço para autenticação de usuários
class AutenticacaoServico(Conexao):

    # Método de login
    def sessao_login(self, email: str, senha: str) -> Usuario | None:
        with self._get_conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM Usuario WHERE email = %s;", (email,))
            usuario_row = cur.fetchone()

            if not usuario_row:
                print("Email não encontrado.")
                return None

            if not Usuario.validar_senha(usuario_row["senhahash"], senha):
                print("Senha incorreta.")
                return None

            if not usuario_row["status"]:
                print("Usuario inativo. Contate o administrador.")
                return None

            # Atualiza último login (se tiver o campo)
            cur.execute(
                "UPDATE Usuario SET perfil = perfil WHERE idUsuario = %s;",  # apenas força commit
                (usuario_row["idusuario"],)
            )

            print(f"Usuário {usuario_row['nome']} logado com sucesso!")

            # Cria objeto Usuario a partir da linha (corrigido: adiciona UUID)
            usuario = Usuario(
                uuid=UUID(usuario_row["uuid"]) if "uuid" in usuario_row and usuario_row["uuid"] else uuid4(),
                nome=usuario_row["nome"],
                email=usuario_row["email"],
                senha_hash=usuario_row["senhahash"],
                perfil=usuario_row["perfil"],
                status=usuario_row["status"]
            )
            return usuario

    # Geração de hash de senha com salt
    @staticmethod
    def gerar_hash_senha(senha: str, salt: bytes | None = None) -> str:
        if salt is None:
            salt = os.urandom(16)
        hash_senha = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, 100000)
        return salt.hex() + hash_senha.hex()

    # Verificação de senha
    @staticmethod
    def validar_senha(senha_hash: str, senha_tentativa: str) -> bool:
        salt = bytes.fromhex(senha_hash[:32])
        hash_armazenado = senha_hash[32:]
        hash_tentativa = hashlib.pbkdf2_hmac("sha256", senha_tentativa.encode("utf-8"), salt, 100000).hex()
        return hmac.compare_digest(hash_armazenado, hash_tentativa)

    # Solicitar recuperação de senha
    def solicitar_recuperacao_senha(self, email: str) -> str | None:
        with self._get_conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT idUsuario FROM Usuario WHERE email = %s;", (email,))
            usuario = cur.fetchone()
            if not usuario:
                print("Email não encontrado.")
                return None

            token = os.urandom(16).hex()
            expira_em = datetime.now(timezone.utc) + timedelta(minutes=30)

            cur.execute("""
                INSERT INTO TokenRecuperacao (token, expiraEm, utilizado, fk_Usuario_idUsuario)
                VALUES (%s, %s, FALSE, %s);
            """, (token, expira_em, usuario["idusuario"]))
            conn.commit()

            print(f"Token gerado para {email}: {token} (expira às {expira_em})")
            return token

    # Redefinir senha usando token
    def redefinir_senha(self, token: str, nova_senha: str) -> bool:
        with self._get_conn() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT t.idToken, t.expiraEm, t.utilizado, u.idUsuario
                FROM TokenRecuperacao t
                JOIN Usuario u ON u.idUsuario = t.fk_Usuario_idUsuario
                WHERE t.token = %s;
            """, (token,))
            meta = cur.fetchone()

            if not meta:
                print("Token inválido.")
                return False
            if meta["utilizado"]:
                print("Token já utilizado.")
                return False

            expira_em = meta["expiraem"]
            if expira_em.tzinfo is None:
                expira_em = expira_em.replace(tzinfo=timezone.utc)
            if expira_em <= datetime.now(timezone.utc):
                print("Token expirado.")
                return False

            # Atualiza a senha e marca token como utilizado
            nova_hash = Usuario.hash_senha(nova_senha)
            cur.execute(
                "UPDATE Usuario SET senhaHash = %s WHERE idUsuario = %s;",
                (nova_hash, meta["idusuario"])
            )
            cur.execute(
                "UPDATE TokenRecuperacao SET utilizado = TRUE WHERE idToken = %s;",
                (meta["idtoken"],)
            )
            conn.commit()
            print("Senha redefinida com sucesso.")
            return True