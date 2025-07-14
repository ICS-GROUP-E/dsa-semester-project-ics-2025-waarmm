import sqlite3
import os

# Define the database path
DB_PATH = os.path.join(os.path.dirname(__file__), "hospital.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            condition TEXT,
            priority INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_patient(name, age, condition, priority):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients (name, age, condition, priority)
        VALUES (?, ?, ?, ?)
    """, (name, age, condition, priority))
    conn.commit()
    conn.close()

def get_all_patients_sorted():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, age, condition, priority, timestamp
        FROM patients
        ORDER BY priority ASC, timestamp ASC
    """)
    patients = cursor.fetchall()
    conn.close()
    return patients

def delete_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    conn.commit()
    conn.close()
