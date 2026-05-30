from fastapi import FastAPI
import sqlite3
import app.database.db  # Isso executa o código do db.py e cria a tabela

app = FastAPI()

def get_connection():
    # Conecta ao mesmo arquivo definido no db.py
    return sqlite3.connect("database.db")

@app.get("/")
def home():
    return {"msg": "API rodando"}

@app.get("/usuarios")
def listar_usuarios():
    conn = get_connection()
    # Configura para retornar os dados como dicionário em vez de tupla
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios")
    dados = cursor.fetchall()
    
    conn.close()
    return dados

@app.post("/usuarios")
def criar_usuario(nome: str, idade: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO usuarios (nome, idade) VALUES (?, ?)",
        (nome, idade)
    )

    conn.commit()
    conn.close()

    return {"msg": "Usuário criado"}

@app.delete("/usuarios/{id}")
def deletar_usuario(id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return {"msg": "Usuário deletado"}

@app.put("/usuarios/{id}")
def atualizar_usuario(id: int, nome: str, idade: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE usuarios SET nome = ?, idade = ? WHERE id = ?",
        (nome, idade, id)
    )

    conn.commit()
    conn.close()

    return {"msg": "Usuário atualizado"}