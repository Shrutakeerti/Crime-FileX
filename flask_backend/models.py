# models.py
import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_details TEXT NOT NULL,
            location TEXT NOT NULL,
            crime_type TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_case(case_details, location, crime_type):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cases (case_details, location, crime_type) VALUES (?, ?, ?)
    ''', (case_details, location, crime_type))
    conn.commit()
    conn.close()
