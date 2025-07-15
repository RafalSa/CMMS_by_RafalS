import db_utils
import login_window
from db_utils import create_tables, add_tpm_task, add_inventory_item


if __name__ == "__main__":
    db_utils.create_tables()
    login_window.show_login_window()
add_tpm_task("Smarowanie prowadnicy liniowej", "2025-06-21", "Mechanik")
add_tpm_task("Wymiana filtra oleju", "2025-06-21", "Mechanik")
add_tpm_task("Kontrola czujnika indukcyjnego X12", "2025-07-14", "Automatyk")
add_tpm_task("Test wyłącznika krańcowego Z3", "2025-06-22", "Elektryk")

add_inventory_item("Łożysko kulkowe 6205", "SAP12345", "REF67890", 20, "Magazyn A")
add_inventory_item("Filtr oleju MF-123", "SAP54321", "REF09876", 15, "Magazyn B")
add_inventory_item("Czujnik indukcyjny X12", "SAP11111", "REF22222", 8, "Magazyn C")
add_inventory_item("Wyłącznik krańcowy Z3", "SAP33333", "REF44444", 12, "Magazyn A")
