import tkinter as tk
import sqlite3
from datetime import datetime

def show_failure_form():
    def submit():
        conn = sqlite3.connect("cmms.db")
        c = conn.cursor()
        c.execute("INSERT INTO failures (description, parts_used, duration, response_time, date) VALUES (?, ?, ?, ?, ?)",
                  (desc.get(), parts.get(), float(duration.get()), float(response.get()), datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        conn.close()
        win.destroy()

    win = tk.Toplevel()
    win.title("Zgłoszenie awarii")

    tk.Label(win, text="Opis awarii").pack()
    desc = tk.Entry(win, width=50)
    desc.pack()

    tk.Label(win, text="Wymienione części").pack()
    parts = tk.Entry(win, width=50)
    parts.pack()

    tk.Label(win, text="Czas trwania [min]").pack()
    duration = tk.Entry(win)
    duration.pack()

    tk.Label(win, text="Czas reakcji [min]").pack()
    response = tk.Entry(win)
    response.pack()

    tk.Button(win, text="Zgłoś", command=submit).pack(pady=10)
