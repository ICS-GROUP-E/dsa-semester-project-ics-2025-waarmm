import sqlite3
import os

def get_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "../../hospital.db")
    return sqlite3.connect(os.path.abspath(db_path))
  
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "hospital.db"))

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def init_db():

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            condition TEXT
        )
    """)

    conn.commit()


def insert_patient_to_db(patient):
    sql = """
        INSERT OR REPLACE INTO patients (id, name, age, condition)
        VALUES (?, ?, ?, ?)
    """
    cursor.execute(sql, (patient.id, patient.name, patient.age, patient.condition))
    conn.commit()


def delete_patient_from_db(patient_id):
    sql = """
        DELETE FROM patients WHERE id = ?
    """
    cursor.execute(sql, (patient_id, ))
    conn.commit()


def get_all_patients():
    cursor.execute("SELECT id, name, age, condition FROM patients")
    return cursor.fetchall()
