import sqlite3

def create_connection():
    conn = sqlite3.connect('criminal_db.sqlite')
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS cases (
                      case_id TEXT PRIMARY KEY,
                      name TEXT,
                      blood_group TEXT,
                      dna TEXT,
                      retina_scan TEXT,
                      fingerprint TEXT,
                      photos BLOB
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      user_id INTEGER PRIMARY KEY,
                      username TEXT,
                      password TEXT
                    )''')
    conn.commit()
    conn.close()

create_tables()
