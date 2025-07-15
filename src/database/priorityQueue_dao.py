from .priorityQueue_db_config import get_connection

arrival_counter = 0

def add_patient_to_db(name, priority):
    global arrival_counter
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO patients (name, priority, arrival_order) VALUES (?, ?, ?)",
                   (name, priority, arrival_counter))
    arrival_counter += 1
    conn.commit()
    conn.close()

def get_all_patients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, priority, arrival_order FROM patients ORDER BY priority ASC, arrival_order ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

import sqlite3

def delete_all_patients():
    conn = sqlite3.connect("patients.db")  # use your correct DB path if different
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients")
    conn.commit()
    conn.close()

def delete_all_patients():
    conn = sqlite3.connect("patients.db")  # use your correct DB path if different
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients")
    conn.commit()
    conn.close()

