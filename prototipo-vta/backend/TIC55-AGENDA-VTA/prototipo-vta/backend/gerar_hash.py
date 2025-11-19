# gerar_hash.py
from werkzeug.security import generate_password_hash

# Senhas que você quer criptografar
senha_admin = 'admin123'
senha_recepcao = 'recepcao123'
senha_vet = 'vet123'

# Gerar os hashes
hash_admin = generate_password_hash(senha_admin)
hash_recepcao = generate_password_hash(senha_recepcao)
hash_vet = generate_password_hash(senha_vet)

print("\n--- COPIE OS COMANDOS SQL ABAIXO E COLE NO psql ---\n")
print(f"INSERT INTO usuarios (nome, email, senha_hash, perfil) VALUES ('Administrador', 'admin@vta.com', '{hash_admin}', 'Administrador');")
print(f"INSERT INTO usuarios (nome, email, senha_hash, perfil) VALUES ('Recepcionista', 'recepcao@vta.com', '{hash_recepcao}', 'Recepcionista');")
print(f"INSERT INTO usuarios (nome, email, senha_hash, perfil) VALUES ('Veterinário', 'veterinario@vta.com', '{hash_vet}', 'Veterinário');")
print("\n")