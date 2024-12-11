import sqlite3

# Cria (ou conecta) ao banco de dados
conn = sqlite3.connect("troubleshooting.db")
cursor = conn.cursor()

# Lista das máquinas
machines = [
    "COR300",
    "PRE30",
    "AROPOL_2_V",
    "COR250",
    "AROPOL_VV300A"
]

# Criação das tabelas
for machine in machines:
    # Ajuste o nome para evitar problemas com caracteres especiais
    table_name = machine.replace(" ", "_")
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problema TEXT NOT NULL,
            solucao TEXT NOT NULL
        )
    """)
    print(f"Tabela '{table_name}' criada com sucesso!")

# Salva as alterações e fecha a conexão
conn.commit()
conn.close()
