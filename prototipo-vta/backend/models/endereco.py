from uuid import uuid4

class Endereco:
    """
    Representa um endereço de cliente.
    
    Attributes:
        uuid: Identificador único do endereço
        cliente_id: ID do cliente
        rua: Nome da rua
        numero: Número do endereço
        bairro: Bairro
        cidade: Cidade
        uf: Estado (sigla)
        cep: CEP
    """
    
    def __init__(self, rua: str, numero: str | int, bairro: str, cidade: str, uf: str, cep: str, endereco_uuid: str | None = None, cliente_id: int | None = None):
        if not rua or not rua.strip():
            raise ValueError("Rua não pode ser vazia")
        if not bairro or not bairro.strip():
            raise ValueError("Bairro não pode ser vazio")
        if not cidade or not cidade.strip():
            raise ValueError("Cidade não pode ser vazia")
        if not uf or len(uf.strip()) != 2:
            raise ValueError("UF deve ter 2 caracteres (ex: RS, SP)")
        
        cep_limpo = self._validar_cep(cep)
        if not cep_limpo:
            raise ValueError("CEP inválido (use formato: 00000-000 ou 00000000)")
        
        self.uuid = endereco_uuid if endereco_uuid is not None else str(uuid4())
        self.cliente_id = cliente_id
        self.rua = rua.strip()
        self.numero = str(numero).strip()
        self.bairro = bairro.strip()
        self.cidade = cidade.strip()
        self.uf = uf.strip().upper()
        self.cep = cep_limpo
    
    @staticmethod
    def _validar_cep(cep: str) -> str | None:
        """Valida e normaliza o CEP."""
        if not cep:
            return None
        cep_numeros = ''.join(c for c in cep if c.isdigit())
        if len(cep_numeros) != 8:
            return None
        return f"{cep_numeros[:5]}-{cep_numeros[5:]}"
    
    def __repr__(self) -> str:
        return (
            f"Endereco(uuid={self.uuid!r}, rua={self.rua!r}, "
            f"numero={self.numero!r}, cidade={self.cidade!r}, uf={self.uf!r})"
        )
    
    def endereco_completo(self) -> str:
        """Retorna o endereço formatado como string."""
        return (
            f"{self.rua}, {self.numero} - {self.bairro}\n"
            f"{self.cidade}/{self.uf} - CEP: {self.cep}"
        )
    
    def to_dict(self) -> dict:
        return {
            "uuid": self.uuid,
            "cliente_id": self.cliente_id,
            "rua": self.rua,
            "numero": self.numero,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "uf": self.uf,
            "cep": self.cep
        }
              