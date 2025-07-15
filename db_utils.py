import sqlite3
from datetime import date

DB_PATH = 'cmms.db'

FAILURE_HEADERS = [
    "Użytkownik", "Obszar", "Podsystem", "Podsystem funkcjonalny", "Data",
    "Zmiana", "Godzina zgłoszenia", "Godzina zakończenia", "Czas przestoju (min)",
    "Dział", "Kategoria", "Typ awarii", "Opis awarii", "Osoba niwelująca"
]

def connect():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = connect()
    c = conn.cursor()

    # Tabela użytkowników
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL
    )
    ''')

    # Tabela awarii
    c.execute('DROP TABLE IF EXISTS failures')
    c.execute('''
    CREATE TABLE failures (
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

    # Tabela zadań TPM
    c.execute('DROP TABLE IF EXISTS tpm_tasks')
    c.execute('''
        CREATE TABLE tpm_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            field TEXT NOT NULL,
            type TEXT NOT NULL,
            description TEXT NOT NULL
        )
        ''')

    # Tabela magazynowa
    c.execute("DROP TABLE IF EXISTS inventory")
    c.execute('''
        CREATE TABLE inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sap_number TEXT NOT NULL,
            reference_number TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            location TEXT NOT NULL
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
    ''', (
        data["username"],
        data["obszar_system"],
        data["podsystem"],
        data["podsystem_funkcjonalny"],
        data["data_zgloszenia"],
        data["zmiana"],
        data["godzina_zgloszenia"],
        data["godzina_zakonczenia"],
        int(data["czas_awarii"]),
        data["dzial"],
        data["kategoria_awarii"],
        data["awaria_jaka"],
        data["opis_awarii"],
        data["osoba_niwelujaca"]
    ))
    conn.commit()
    conn.close()

def get_failure_history():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            user, area, subsystem, functional_subsystem, date,
            shift, time_reported, time_resolved, downtime_minutes,
            department, category, failure_type, failure_description, resolver
        FROM failures
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_tpm_task(date, field, type_, desc):
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO tpm_tasks (date, field, type, description) VALUES (?, ?, ?, ?)", (date, field, type_, desc))
    conn.commit()
    conn.close()

def get_today_tpm_tasks():
    today_str = date.today().isoformat()
    conn = connect()
    c = conn.cursor()
    # Poprawka tutaj:
    c.execute("SELECT date, field, type, description FROM tpm_tasks WHERE date = ?", (today_str,))
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_tpm_tasks():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id, date, field, type, description FROM tpm_tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks

def update_tpm_task(old_date, date, field, type_, desc):
    conn = connect()
    c = conn.cursor()
    c.execute("UPDATE tpm_tasks SET date=?, field=?, type=?, description=? WHERE date=?", (date, field, type_, desc, old_date))
    conn.commit()
    conn.close()


def get_inventory_items(search_query=""):
    conn = connect()
    c = conn.cursor()
    if search_query:
        search_query = f"%{search_query}%"
        c.execute("""
            SELECT id, name, sap_number, reference_number, quantity, location
            FROM inventory
            WHERE name LIKE ? OR CAST(id AS TEXT) LIKE ?
        """, (search_query, search_query))
    else:
        c.execute("SELECT id, name, sap_number, reference_number, quantity, location FROM inventory")

    results = c.fetchall()
    conn.close()
    return results


def add_inventory_item(name, sap_number, reference_number, quantity, location):
    conn = connect()
    c = conn.cursor()
    c.execute('''
        INSERT INTO inventory (name, sap_number, reference_number, quantity, location)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, sap_number, reference_number, quantity, location))
    conn.commit()
    conn.close()
