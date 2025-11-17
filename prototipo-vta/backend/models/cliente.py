from uuid import uuid4, UUID

class Cliente:
    
    # Método construtor da classe cliente
    def __init__(self, nome, telefone, email, cliente_id =UUID):
        self.cliente_id = cliente_id if cliente_id is not None else str(uuid4())
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.ativo = True

    # Método para exibir informações do cliente
    def exibir_informacoes(self):
        
        return (
            f"Cliente_id: {self.cliente_id}, Nome: {self.nome}, "
            f"Telefone: {self.telefone}, Email: {self.email}, Ativo: {self.ativo}"
        )

    # Método para marcar cliente como inativo
    def inativar(self):
        self.ativo = False

    # Método para representar o objeto como string
    def __repr__(self):
        return f"<cliente uuid={self.uuid} nome={self.nome} ativo={self.ativo}>"