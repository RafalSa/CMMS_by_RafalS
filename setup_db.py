import sqlite3
import os

DB_PATH = os.path.join("App_Data", "chat.db")

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Użytkownicy
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'operator'
    )
    """)

    # Zadania dzienne
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        created_by TEXT,
        created_at TEXT,
        due_date TEXT,
        is_completed INTEGER DEFAULT 0
    )
    """)

    # Rejestr usterek
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS failures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        reported_by TEXT,
        status TEXT DEFAULT 'Zgłoszona',
        reported_at TEXT,
        resolved_at TEXT
    )
    """)

    # Magazyn części
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        part_name TEXT,
        quantity INTEGER,
        location TEXT,
        last_updated TEXT
    )
    """)

    # Historia pobrań części
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        part_id INTEGER,
        used_by TEXT,
        quantity_used INTEGER,
        used_at TEXT,
        FOREIGN KEY(part_id) REFERENCES inventory(id)
    )
    """)

    # Historia działań
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS maintenance_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        action TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Baza danych gotowa!")

if __name__ == "__main__":
    create_tables()
