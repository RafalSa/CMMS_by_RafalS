import customtkinter as ctk
import tkinter.messagebox
import db_utils
from datetime import datetime

class FailureWindow(ctk.CTkToplevel):
    def __init__(self, master, username):
        super().__init__(master)
        self.title("Zgłaszanie awarii")
        self.geometry("600x900")
        self.configure(fg_color="#2b2b2b")  # Ciemne tło
        self.username = username

        # Główna ramka z przewijaniem
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="#2b2b2b", width=580, height=800)
        self.scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.header = ctk.CTkLabel(self.scrollable_frame, text="Zgłoszenie awarii", font=("Arial", 24), text_color="white")
        self.header.pack(pady=15)

        # Pola formularza
        self.fields = {
            "Obszar systemu": ctk.CTkEntry(self.scrollable_frame),
            "Podsystem": ctk.CTkEntry(self.scrollable_frame),
            "Podsystem funkcjonalny": ctk.CTkEntry(self.scrollable_frame),
            "Data zgłoszenia (YYYY-MM-DD)": ctk.CTkEntry(self.scrollable_frame),
            "Zmiana": ctk.CTkComboBox(self.scrollable_frame, values=["1", "2", "3"]),
            "Godzina zgłoszenia (HH:MM)": ctk.CTkEntry(self.scrollable_frame),
            "Godzina zakończenia (HH:MM)": ctk.CTkEntry(self.scrollable_frame),
            "Czas awarii (minuty)": ctk.CTkEntry(self.scrollable_frame),
            "Dział": ctk.CTkComboBox(self.scrollable_frame,
                                     values=["Utrzymanie ruchu", "IT", "Produkcja", "Logistyka"]),
            "Kategoria awarii": ctk.CTkComboBox(self.scrollable_frame,
                                                values=["Mechaniczna", "Elektryczna", "Programowa", "Inna"]),
            "Typ awarii": ctk.CTkComboBox(self.scrollable_frame,
                                          values=["Błąd czujnika", "Uszkodzenie silnika", "Brak zasilania",
                                                  "Zawieszenie systemu"]),
            "Opis awarii": ctk.CTkTextbox(self.scrollable_frame, height=120),
            "Osoba niwelująca": ctk.CTkEntry(self.scrollable_frame)
        }

        self.fields["Dział"].set("Utrzymanie ruchu")
        self.fields["Kategoria awarii"].set("Mechaniczna")
        self.fields["Typ awarii"].set("Błąd czujnika")

        # Ustaw aktualną datę i godzinę
        self.fields["Data zgłoszenia (YYYY-MM-DD)"].insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.fields["Godzina zgłoszenia (HH:MM)"].insert(0, datetime.now().strftime("%H:%M"))

        for label, widget in self.fields.items():
            ctk.CTkLabel(self.scrollable_frame, text=label, text_color="white").pack(pady=(10, 0))
            widget.pack(padx=10, fill="x")

        # Ramka na przyciski, zawsze na dole
        self.bottom_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        self.bottom_frame.pack(pady=10)

        self.submit_button = ctk.CTkButton(self.bottom_frame, text="Zgłoś awarię", command=self.submit_failure, fg_color="#1f6aa5")
        self.submit_button.pack(side="left", padx=10)

        self.history_button = ctk.CTkButton(self.bottom_frame, text="Pokaż historię awarii", command=self.show_history, fg_color="#1f6aa5")
        self.history_button.pack(side="left", padx=10)

    def submit_failure(self):
        data = {
            "username": self.username,
            "obszar_system": self.fields["Obszar systemu"].get(),
            "podsystem": self.fields["Podsystem"].get(),
            "podsystem_funkcjonalny": self.fields["Podsystem funkcjonalny"].get(),
            "data_zgloszenia": self.fields["Data zgłoszenia (YYYY-MM-DD)"].get(),
            "zmiana": self.fields["Zmiana"].get(),
            "godzina_zgloszenia": self.fields["Godzina zgłoszenia (HH:MM)"].get(),
            "godzina_zakonczenia": self.fields["Godzina zakończenia (HH:MM)"].get(),
            "czas_awarii": self.fields["Czas awarii (minuty)"].get(),
            "dzial": self.fields["Dział"].get(),
            "kategoria_awarii": self.fields["Kategoria awarii"].get(),
            "awaria_jaka": self.fields["Typ awarii"].get(),
            "opis_awarii": self.fields["Opis awarii"].get("0.0", "end").strip(),
            "osoba_niwelujaca": self.fields["Osoba niwelująca"].get()
        }

        db_utils.add_failure(data)
        tkinter.messagebox.showinfo("Sukces", "Awaria została zgłoszona.")

    def show_history(self):
        history_window = ctk.CTkToplevel(self)
        history_window.title("Historia Awarii")
        history_window.geometry("1000x600")
        history_window.configure(fg_color="#2b2b2b")

        failures = db_utils.get_failure_history()

        text = ctk.CTkTextbox(history_window, font=("Consolas", 12), wrap="word", text_color="white",
                              fg_color="#1e1e1e")
        text.pack(fill="both", expand=True, padx=10, pady=10)

        if not failures:
            text.insert("end", "Brak zgłoszonych awarii.")
        else:
            for f in failures:
                entry = "\n".join([f"{k}: {v}" for k, v in zip(db_utils.FAILURE_FIELDS, f)])
                text.insert("end", entry + "\n" + "-" * 80 + "\n")

# Funkcja pomocnicza dla main.py:
def open_failure_window(username, return_callback):
    window = FailureWindow(return_callback, username)
    window.grab_set()  # modalne okno
