import tkinter as tk
import sqlite3

def show_inventory():
    win = tk.Toplevel()
    win.title("Stan magazynowy")

    conn = sqlite3.connect("cmms.db")
    c = conn.cursor()
    c.execute("SELECT name, quantity FROM inventory")
    data = c.fetchall()
    conn.close()

    for name, qty in data:
        tk.Label(win, text=f"{name} – {qty} szt.").pack()
