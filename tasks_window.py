# tasks_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import db_utils


class TasksWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Zadania TPM")
        self.tree = ttk.Treeview(master, columns=("Data", "Dzial", "Typ", "Opis"), show="headings")

        for col in ("Data", "Dzial", "Typ", "Opis"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=10)

        add_btn = tk.Button(btn_frame, text="Dodaj zadanie", command=self.add_task)
        edit_btn = tk.Button(btn_frame, text="Edytuj zadanie", command=self.edit_task)
        add_btn.grid(row=0, column=0, padx=5)
        edit_btn.grid(row=0, column=1, padx=5)

        self.load_tasks()

    def load_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for task in db_utils.get_tpm_tasks():
            self.tree.insert("", "end", values=(task[1], task[2], task[3], task[4]))

    def add_task(self):
        self.task_editor()

    def edit_task(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Brak wyboru", "Wybierz zadanie do edycji")
            return
        values = self.tree.item(selected, 'values')
        self.task_editor(values)

    def task_editor(self, values=None):
        editor = tk.Toplevel(self.master)
        editor.title("Edytuj zadanie" if values else "Dodaj zadanie")

        tk.Label(editor, text="Data przeglądu (YYYY-MM-DD):").grid(row=0, column=0)
        date_entry = tk.Entry(editor)
        date_entry.grid(row=0, column=1)

        tk.Label(editor, text="Dział (mechanik/elektryk/automatyk):").grid(row=1, column=0)
        field_entry = tk.Entry(editor)
        field_entry.grid(row=1, column=1)

        tk.Label(editor, text="Typ zadania (np. TPM):").grid(row=2, column=0)
        type_entry = tk.Entry(editor)
        type_entry.grid(row=2, column=1)

        tk.Label(editor, text="Opis czynności:").grid(row=3, column=0)
        desc_entry = tk.Entry(editor, width=40)
        desc_entry.grid(row=3, column=1)

        if values:
            date_entry.insert(0, values[0])
            field_entry.insert(0, values[1])
            type_entry.insert(0, values[2])
            desc_entry.insert(0, values[3])

        def save():
            date = date_entry.get()
            field = field_entry.get()
            type_ = type_entry.get()
            desc = desc_entry.get()

            if not (date and field and type_ and desc):
                messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione")
                return

            if values:
                db_utils.update_tpm_task(values[0], date, field, type_, desc)
            else:
                db_utils.add_tpm_task(date, field, type_, desc)

            editor.destroy()
            self.load_tasks()

        tk.Button(editor, text="Zapisz", command=save).grid(row=4, column=0, columnspan=2, pady=10)

def show_tasks_window(username, back_callback):
    window = tk.Toplevel()
    app = TasksWindow(window)

    def on_close():
        window.destroy()
        back_callback()

    window.protocol("WM_DELETE_WINDOW", on_close)
    window.mainloop()

def back_to_menu(window, back_to_menu_func, username):
    window.destroy()
    back_to_menu_func(username)


if __name__ == '__main__':
    root = tk.Tk()
    app = TasksWindow(root)
    root.mainloop()