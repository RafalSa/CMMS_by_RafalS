import tkinter as tk
from tkinter import messagebox
import db_utils
from datetime import datetime

def show_failure_form(username):
    def submit():
        try:
            data = (
                username,
                area.get(),
                subsystem.get(),
                func_subsystem.get(),
                date.get(),
                shift.get(),
                time_reported.get(),
                time_resolved.get(),
                int(downtime.get()),
                department.get(),
                category.get(),
                failure_type.get(),
                description.get(),
                resolver.get()
            )
            if not all(data):
                messagebox.showwarning("Uwaga", "Wszystkie pola muszą być wypełnione.")
                return

            db_utils.add_failure(data)
            messagebox.showinfo("Sukces", "Awaria została zgłoszona.")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    win = tk.Toplevel()
    win.title("Zgłoszenie awarii")

    def add_label_entry(label, row):
        tk.Label(win, text=label).grid(row=row, column=0, sticky="w")
        entry = tk.Entry(win, width=40)
        entry.grid(row=row, column=1)
        return entry

    area = add_label_entry("Obszar / System:", 0)
    subsystem = add_label_entry("Podsystem:", 1)
    func_subsystem = add_label_entry("Podsystem funkcjonalny:", 2)
    date = add_label_entry("Data (YYYY-MM-DD):", 3)
    shift = add_label_entry("Zmiana (1/2/3):", 4)
    time_reported = add_label_entry("Godzina zgłoszenia (HH:MM):", 5)
    time_resolved = add_label_entry("Godzina zakończenia (HH:MM):", 6)
    downtime = add_label_entry("Czas awarii (minuty):", 7)
    department = add_label_entry("Dział:", 8)
    category = add_label_entry("Kategoria:", 9)
    failure_type = add_label_entry("Typ awarii:", 10)
    description = add_label_entry("Opis awarii:", 11)
    resolver = add_label_entry("Osoba usuwająca:", 12)

    tk.Button(win, text="Zgłoś awarię", command=submit).grid(row=13, columnspan=2, pady=10)
