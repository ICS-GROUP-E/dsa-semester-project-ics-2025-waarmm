import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('stacks_db.db')
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS input (
                                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        title TEXT,
                                                        content TEXT,
                                                        created_at TEXT NOT NULL
                   )
                   ''')
    conn.commit()
    conn.close()

def save_input(title, content):
    conn = sqlite3.connect('stacks_db.db')
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO input (title, content, created_at) VALUES (?, ?, ?)
                   ''', (title, content, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_input():
    conn = sqlite3.connect('stacks_db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, created_at FROM input ORDER BY created_at DESC')
    content = cursor.fetchall()
    conn.close()
    return content

def load_input(input_id):
    conn = sqlite3.connect('stacks_db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM input WHERE id = ?', (input_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else ""






# import sqlite3

# from tkinter import ttk
# from datetime import datetime
#
# def init_db():
#     conn = sqlite3.connect('stacks_db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS input (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         title TEXT,
#         content TEXT,
#         created_at TEXT NOT NULL
#         )
#     ''')
#     conn.commit()
#     conn.close()
#
# def save_input(title, content):
#     conn = sqlite3.connect('stacks_db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO input (title, content, created_at) VALUES (?, ?, ?)
#     ''', (title, content, datetime.now().isoformat()))
#     conn.commit()
#     conn.close()
#
# def get_input():
#     conn = sqlite3.connect('stacks_db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT ID, title, created_at FROM input ORDER BY created_at DESC')
#     content = cursor.fetchall()
#     conn.close()
#     return content
#
# def load_input(input_id):
#     conn = sqlite3.connect('stacks_db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT content FROM input WHERE id = ? ' , (input_id))
#     result = cursor.fetchone()
#     conn.close()
#     return result[0] if result else ""