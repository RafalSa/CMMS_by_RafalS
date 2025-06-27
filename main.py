import db_utils
import login_window
from db_utils import create_tables, add_tpm_task


if __name__ == "__main__":
    db_utils.create_tables()
    login_window.show_login_window()
add_tpm_task("Smarowanie prowadnicy liniowej", "2025-06-21", "Mechanik")
add_tpm_task("Wymiana filtra oleju", "2025-06-21", "Mechanik")
add_tpm_task("Kontrola czujnika indukcyjnego X12", "2025-06-21", "Automatyk")
add_tpm_task("Test wyłącznika krańcowego Z3", "2025-06-22", "Elektryk")