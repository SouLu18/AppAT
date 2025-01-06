import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("assets/equipment.db")  # Substitua pelo nome do seu banco
cursor = conn.cursor()

# Apagar todos os dados da tabela
cursor.execute("DELETE FROM AROTEC")

# Resetar o autoincremento (opcional, se a tabela tiver uma coluna ID autoincremento)
cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'AROTEC'")

# Confirmar a alteração
conn.commit()

# Fechar a conexão
cursor.close()
conn.close()

print("Todos os dados foram apagados, mas as colunas permanecem.")
