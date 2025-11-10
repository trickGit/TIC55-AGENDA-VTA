from uuid import uuid4

class endereco:
    
    def __init__(self, rua, numero, bairro, cidade, uf, cep, uuid=None):
        self.enderecoID = uuid if uuid is not None else str(uuid4())
        self.ClienteID = uuid if uuid is not None else str(uuid4())   
        self.rua = rua
        self.numero = numero  
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf
        self.cep = cep
              