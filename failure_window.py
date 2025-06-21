import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import db_utils

def show_failure_window(username, back_to_menu_func):
    window = tk.Tk()
    window.title("Zgłoś awarię - CMMS by RafałS")
    window.geometry("1200x800")
    window.configure(bg="#ffffff")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", font=("Segoe UI", 11), background="#ffffff")
    style.configure("TEntry", font=("Segoe UI", 11))
    style.configure("TButton", font=("Segoe UI", 11))
    style.configure("TCombobox", font=("Segoe UI", 11))

    main_frame = ttk.Frame(window, padding=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    def add_entry(label, row):
        ttk.Label(main_frame, text=label).grid(row=row, column=0, sticky="w", pady=5)
        entry = ttk.Entry(main_frame, width=40)
        entry.grid(row=row, column=1, sticky="w", pady=5)
        return entry

    def add_combobox(label, values, row):
        ttk.Label(main_frame, text=label).grid(row=row, column=0, sticky="w", pady=5)
        combo = ttk.Combobox(main_frame, values=values, width=38, state="readonly")
        combo.grid(row=row, column=1, sticky="w", pady=5)
        return combo

    def add_datetime(label_date, label_time, row):
        ttk.Label(main_frame, text=label_date).grid(row=row, column=0, sticky="w", pady=5)
        date_entry = ttk.Entry(main_frame, width=20)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.grid(row=row, column=1, sticky="w", pady=5)

        ttk.Label(main_frame, text=label_time).grid(row=row, column=2, sticky="w", pady=5)
        time_entry = ttk.Entry(main_frame, width=10)
        time_entry.insert(0, datetime.now().strftime("%H:%M"))
        time_entry.grid(row=row, column=3, sticky="w", pady=5)

        return date_entry, time_entry

    # Pola formularza
    data_start_entry, czas_start_entry = add_datetime("Data zgłoszenia awarii:", "Godzina zgłoszenia:", 4)
    data_end_entry, czas_end_entry = add_datetime("Data zakończenia awarii:", "Godzina zakończenia:", 5)

    fields = {
        "obszar_system": add_combobox("Obszar / System:", ["Wtryskarki", "Prasy", "Montaż", "Lakiernia"], 0),
        "podsystem": add_entry("Podsystem:", 1),
        "podsystem_funkcjonalny": add_entry("Podsystem funkcjonalny:", 2),
        "zmiana": add_combobox("Zmiana:", ["1", "2", "3"], 3),
        "czas_awarii": add_entry("Czas trwania awarii (minuty):", 6),
        "dzial": add_combobox("Dział odpowiedzialny:", ["UR", "IT", "Automatyka", "BHP"], 7),
        "kategoria_awarii": add_combobox("Kategoria awarii:", ["Mechaniczna", "Elektryczna", "Pneumatyczna", "Inna"], 8),
        "awaria_jaka": add_entry("Jaka była awaria:", 9),
        "opis_awarii": add_entry("Opis awarii:", 10),
        "osoba_niwelujaca": add_entry("Osoba usuwająca awarię:", 11)
    }

    def submit():
        try:
            data = {
                "username": username,
                "obszar_system": fields["obszar_system"].get(),
                "podsystem": fields["podsystem"].get(),
                "podsystem_funkcjonalny": fields["podsystem_funkcjonalny"].get(),
                "zmiana": fields["zmiana"].get(),
                "data_zgloszenia": data_start_entry.get(),
                "godzina_zgloszenia": czas_start_entry.get(),
                "data_zakonczenia": data_end_entry.get(),
                "godzina_zakonczenia": czas_end_entry.get(),
                "czas_awarii": fields["czas_awarii"].get(),
                "dzial": fields["dzial"].get(),
                "kategoria_awarii": fields["kategoria_awarii"].get(),
                "awaria_jaka": fields["awaria_jaka"].get(),
                "opis_awarii": fields["opis_awarii"].get(),
                "osoba_niwelujaca": fields["osoba_niwelujaca"].get()
            }

            if not all(data.values()):
                messagebox.showwarning("Brak danych", "Wszystkie pola muszą być wypełnione.")
                return

            db_utils.add_failure(data)
            messagebox.showinfo("Sukces", "Awaria została zapisana.")
            window.destroy()
            back_to_menu_func(username)
        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    def show_history():
        failures = db_utils.get_failure_history()
        if not failures:
            messagebox.showinfo("Historia", "Brak zapisanych awarii.")
            return

        history_window = tk.Toplevel(window)
        history_window.title("Historia awarii")
        history_window.geometry("1200x600")
        text = tk.Text(history_window, wrap="word")
        text.pack(expand=True, fill=tk.BOTH)

        for f in failures:
            text.insert(tk.END, "\n".join([f"{key}: {value}" for key, value in zip(db_utils.FAILURE_FIELDS, f)]) + "\n\n")

    # Przyciski
    btn_frame = ttk.Frame(main_frame)
    btn_frame.grid(row=12, column=0, columnspan=4, pady=20)

    ttk.Button(btn_frame, text="Zapisz zgłoszenie", command=submit).grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Historia awarii", command=show_history).grid(row=0, column=1, padx=10)
    ttk.Button(btn_frame, text="Powrót do menu", command=lambda: (window.destroy(), back_to_menu_func(username))).grid(row=0, column=2, padx=10)

    window.mainloop()
