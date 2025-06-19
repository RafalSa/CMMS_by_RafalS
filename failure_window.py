import tkinter as tk
from tkinter import messagebox
import db_utils
import datetime

def show_failure_window(username, back_to_menu_func):
    window = tk.Tk()
    window.title("Zgłoś awarię")
    window.geometry("600x600")

    tk.Label(window, text=f"Zgłaszanie awarii | Użytkownik: {username}", font=("Arial", 14)).pack(pady=10)

    fields = {
        "Data od (RRRR-MM-DD HH:MM)": tk.Entry(window),
        "Data do (RRRR-MM-DD HH:MM)": tk.Entry(window),
        "Lokalizacja (np. Linia A1)": tk.Entry(window),
        "Typ maszyny (np. Robot ABB)": tk.Entry(window),
        "Opis awarii": tk.Text(window, height=3, width=50),
        "Podjęte działania": tk.Text(window, height=3, width=50),
        "Status (otwarta/zamknięta)": tk.Entry(window)
    }

    entries = {}
    for label, widget in fields.items():
        tk.Label(window, text=label).pack(pady=(10, 0))
        widget.pack()
        entries[label] = widget

    def save_failure():
        try:
            data_od = entries["Data od (RRRR-MM-DD HH:MM)"].get()
            data_do = entries["Data do (RRRR-MM-DD HH:MM)"].get()
            lokalizacja = entries["Lokalizacja (np. Linia A1)"].get()
            typ_maszyny = entries["Typ maszyny (np. Robot ABB)"].get()
            opis = entries["Opis awarii"].get("1.0", tk.END).strip()
            dzialania = entries["Podjęte działania"].get("1.0", tk.END).strip()
            status = entries["Status (otwarta/zamknięta)"].get()

            if not all([data_od, data_do, lokalizacja, typ_maszyny, opis, status]):
                messagebox.showwarning("Błąd", "Wszystkie pola muszą być uzupełnione.")
                return

            db_utils.add_failure(data_od, data_do, lokalizacja, typ_maszyny, opis, dzialania, username, status)
            messagebox.showinfo("Sukces", "Awaria została zapisana.")
        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    def show_reports():
        failures = db_utils.get_all_failures()
        report_win = tk.Toplevel(window)
        report_win.title("Zgłoszone awarie")
        report_win.geometry("700x400")

        text = tk.Text(report_win, wrap="word")
        text.pack(expand=True, fill="both")

        for f in failures:
            text.insert(tk.END, f"ID: {f[0]} | Od: {f[1]} | Do: {f[2]} | Gdzie: {f[3]} | Maszyna: {f[4]}\n")
            text.insert(tk.END, f"Opis: {f[5]}\nDziałania: {f[6]}\nZgłosił: {f[7]} | Status: {f[8]}\n{'-'*60}\n")

    tk.Button(window, text="Zapisz awarię", command=save_failure).pack(pady=10)
    tk.Button(window, text="Podgląd zgłoszonych awarii", command=show_reports).pack()
    tk.Button(window, text="Powrót do menu", command=lambda: back_to_menu(window, back_to_menu_func, username)).pack(pady=20)

    window.mainloop()

def back_to_menu(window, back_to_menu_func, username):
    window.destroy()
    back_to_menu_func(username)
