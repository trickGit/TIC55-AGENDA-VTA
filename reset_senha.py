# reset_senha.py CORRIGIDO
from werkzeug.security import generate_password_hash

senha_nova = 'admin123'
hash_novo = generate_password_hash(senha_nova)

print("\n--- COPIE O COMANDO SQL ABAIXO E COLE NO psql ---\n")
print(f"UPDATE usuarios SET senha_hash = '{hash_novo}' WHERE email = 'admin@vta.com';")