import sqlite3
import os

# Garante que o banco seja criado na raiz do projeto ou caminho absoluto
db_path = "database.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    idade INTEGER
)
""")

conn.commit()
conn.close()
