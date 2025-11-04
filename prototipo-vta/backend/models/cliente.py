from uuid import uuid4

class cliente:
    
    # método construtor da classe cliente
    def __init__(self, nome, telefone, email, uuid=None):
        self.uuid = uuid if uuid is not None else str(uuid4())
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.ativo = True

    # método para exibir informações do cliente
    def exibir_informacoes(self):
        
        return (
            f"UUID: {self.uuid}, Nome: {self.nome}, "
            f"Telefone: {self.telefone}, Email: {self.email}, Ativo: {self.ativo}"
        )

    # método para marcar cliente como inativo
    def inativar(self):
        self.ativo = False

    # método para representar o objeto como string
    def __repr__(self):
        return f"<cliente uuid={self.uuid} nome={self.nome} ativo={self.ativo}>"