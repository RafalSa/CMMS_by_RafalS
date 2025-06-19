import sqlite3

DB_PATH = 'cmms.db'

def connect():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = connect()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def add_user(username, password_hash, salt):
    conn = connect()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                  (username, password_hash, salt))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user(username):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id, username, password_hash, salt FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user
