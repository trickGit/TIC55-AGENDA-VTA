import os
import secrets
from datetime import datetime, timedelta
from backend.models.usuario import Usuario  # Importa tua classe Usuario existente


class AutenticacaoServico:

    # Construtor da classe AutenticacaoServico
    def __init__(self, usuarios: list[Usuario]):
        self.usuarios = usuarios
        self.tokens_recuperacao = {}  # token -> {uuid, expira, usado}

    # Autentica um usuário e registra o login.
    def sessao_login(self, email: str, senha: str) -> Usuario | None:
        for usuario in self.usuarios:
            if usuario.email == email and Usuario.validar_senha(usuario.senha_hash, senha):
                if not usuario.is_ativo():
                    print("Usuário inativo. Contate o administrador.")
                    return None
                usuario.registrar_ultimologin()
                print(f"Usuário {usuario.nome} logado com sucesso!")
                return usuario

        print("Email ou senha incorretos.")
        return None
    
    # Gera um token temporário para recuperação de senha.
    def solicitar_recuperacao_senha(self, email: str) -> str | None:
        usuario = next((u for u in self.usuarios if u.email == email), None)
        if not usuario:
            print("Usuário não encontrado.")
            return None

        token = secrets.token_urlsafe(24)  # token seguro e compatível com URL
        expira = datetime.utcnow() + timedelta(hours=1)

        self.tokens_recuperacao[token] = {
            "uuid": usuario.uuid,
            "expira": expira,
            "usado": False,
        }

        print(f"Token gerado para {email}: {token} (expira às {expira})")
        return token

    # Redefine a senha de um usuário se o token for válido.
    def redefinir_senha(self, token: str, nova_senha: str) -> bool:
        meta = self.tokens_recuperacao.get(token)

        if not meta:
            print("Token inválido.")
            return False
        if meta["usado"]:
            print("Token já utilizado.")
            return False
        if meta["expira"] < datetime.utcnow():
            print("Token expirado.")
            return False

        usuario = next((u for u in self.usuarios if u.uuid == meta["uuid"]), None)
        if not usuario:
            print("Usuário não encontrado.")
            return False

        usuario.senha_hash = Usuario.hash_senha(nova_senha)
        meta["usado"] = True
        print(f"Senha redefinida com sucesso para {usuario.nome}.")
        return True