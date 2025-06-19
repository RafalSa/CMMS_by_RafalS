import customtkinter as ctk
from tasks_window import show_tasks_window
from print_tasks_window import show_print_tasks_window
from failure_window import show_failure_window
from inventory_window import show_inventory_window
import login_window

def show_main_menu(username):
    ctk.set_appearance_mode("dark")      # Tryb: 'light', 'dark', 'system'
    ctk.set_default_color_theme("blue")  # Motyw: 'blue', 'green', 'dark-blue'

    window = ctk.CTk()
    window.title(f"Witaj {username} - CMMS by RafałS")
    window.geometry("1920x1080")
    window.state("zoomed")  # Pełny ekran

    frame = ctk.CTkFrame(window, corner_radius=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    title = ctk.CTkLabel(frame, text=f"Panel główny - {username}", font=ctk.CTkFont(size=28, weight="bold"))
    title.pack(pady=(30, 40))

    def open_subwindow(func):
        window.destroy()
        func(username, show_main_menu)

    btn_tasks = ctk.CTkButton(frame, text="Zarządzaj zadaniami", width=300, height=50, font=ctk.CTkFont(size=16), command=lambda: open_subwindow(show_tasks_window))
    btn_tasks.pack(pady=10)

    btn_print = ctk.CTkButton(frame, text="Drukuj zadania dzienne (TPM)", width=300, height=50, font=ctk.CTkFont(size=16), command=lambda: open_subwindow(show_print_tasks_window))
    btn_print.pack(pady=10)

    btn_failure = ctk.CTkButton(frame, text="Zgłoś awarię", width=300, height=50, font=ctk.CTkFont(size=16), command=lambda: open_subwindow(show_failure_window))
    btn_failure.pack(pady=10)

    btn_inventory = ctk.CTkButton(frame, text="Przeglądaj magazyn", width=300, height=50, font=ctk.CTkFont(size=16), command=lambda: open_subwindow(show_inventory_window))
    btn_inventory.pack(pady=10)

    btn_logout = ctk.CTkButton(frame, text="Wyloguj się", width=300, height=50, font=ctk.CTkFont(size=16), fg_color="red", hover_color="#990000", command=lambda: [window.destroy(), login_window.show_login_window()])
    btn_logout.pack(pady=(40, 20))

    window.mainloop()
