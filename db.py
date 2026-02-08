"""
conectar db
"""
import sqlite3
import os
BASE_DIR =os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "database.db")

DB_NAME = 'database.db'
def conectar():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            codigo TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            categoria TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

