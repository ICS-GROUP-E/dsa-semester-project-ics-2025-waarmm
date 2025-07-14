import sqlite3

def get_connection():
    conn = sqlite3.connect("priorityQueue_patients.db")
    return conn

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            priority INTEGER NOT NULL,
            arrival_order INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()
