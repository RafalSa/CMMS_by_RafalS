import customtkinter as ctk

def show_print_tasks_window(username, back_to_menu_func):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    window = ctk.CTk()
    window.title("Drukowanie zadań TPM - CMMS by RafałS")
    window.geometry("500x350")
    window.resizable(False, False)

    frame = ctk.CTkFrame(window, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    label = ctk.CTkLabel(
        frame,
        text=f"Drukowanie zadań TPM\nUżytkownik: {username}",
        font=ctk.CTkFont(size=20, weight="bold"),
        justify="center"
    )
    label.pack(pady=(30, 20))

    # Tu można dodać przyszłe opcje np. wybór zakresu dat, rodzaju wydruku itd.
    ctk.CTkButton(frame, text="(Wkrótce) Drukuj zadania", state="disabled").pack(pady=10)

    btn_back = ctk.CTkButton(
        frame,
        text="Powrót do menu",
        width=200,
        command=lambda: back_to_menu(window, back_to_menu_func, username)
    )
    btn_back.pack(pady=(20, 30))

    window.mainloop()

def back_to_menu(window, back_to_menu_func, username):
    window.destroy()
    back_to_menu_func(username)
