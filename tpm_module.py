import tempfile
import os
from tkinter import messagebox
from datetime import date
from db_utils import get_today_tpm_tasks

def print_tpm():
    tasks = get_today_tpm_tasks()
    if not tasks:
        messagebox.showinfo("TPM", "Brak zadań TPM zaplanowanych na dziś.")
        return

    today_str = date.today().strftime("%d.%m.%Y")
    content = f"Zadania TPM na dziś ({today_str}):\n\n"
    for i, (desc, category) in enumerate(tasks, 1):
        content += f"{i}. [{category}] {desc}\n"

    # Zapisz do tymczasowego pliku i wyślij do drukarki
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding='utf-8') as tf:
            tf.write(content)
            temp_path = tf.name

        os.startfile(temp_path, "print")  # działa tylko na Windows
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił problem z drukowaniem:\n{e}")
