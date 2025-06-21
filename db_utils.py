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

    # USUŃ STARĄ TABELĘ FAILURES (opcjonalnie)
    c.execute('DROP TABLE IF EXISTS failures')

    # UTWÓRZ NOWĄ STRUKTURĘ
    c.execute('''
    CREATE TABLE IF NOT EXISTS failures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        area TEXT NOT NULL,
        subsystem TEXT NOT NULL,
        functional_subsystem TEXT NOT NULL,
        date TEXT NOT NULL,
        shift TEXT NOT NULL,
        time_reported TEXT NOT NULL,
        time_resolved TEXT NOT NULL,
        downtime_minutes INTEGER NOT NULL,
        department TEXT NOT NULL,
        category TEXT NOT NULL,
        failure_type TEXT NOT NULL,
        failure_description TEXT NOT NULL,
        resolver TEXT NOT NULL
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

def add_failure(data):
    conn = connect()
    c = conn.cursor()
    c.execute('''
        INSERT INTO failures (
            user, area, subsystem, functional_subsystem, date,
            shift, time_reported, time_resolved, downtime_minutes,
            department, category, failure_type, failure_description, resolver
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

