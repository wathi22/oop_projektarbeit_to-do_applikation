# python3
# Projekt von Joel Fehr & Matthias Heiniger (angepasst: ohne os)

import csv
from datetime import datetime, timedelta

# --------- Speicherpfade (vereinfacht) ---------
STORE_FILENAME = "todos.csv"
STORE_PATH = STORE_FILENAME  # im aktuellen Verzeichnis

# --------- CSV-Header / Felder ---------
CSV_FIELDS = ["id", "description", "priority", "due_date", "status", "created_at"]

# --------- Format/Constants ---------
DATE_FMT = "%Y-%m-%d"

PRIO_LOW = "low"
PRIO_MED = "medium"
PRIO_HIGH = "high"
VALID_PRIORITIES = (PRIO_LOW, PRIO_MED, PRIO_HIGH)

STATUS_OPEN = "open"
STATUS_DONE = "done"
VALID_STATUS = (STATUS_OPEN, STATUS_DONE)

MENU_EXIT = "0"
MENU_SHOW = "1"
MENU_ADD = "2"
MENU_EDIT = "3"
MENU_TOGGLE = "4"
MENU_DELETE = "5"
MENU_FILTER_SORT = "6"
MENU_DEBUG = "7"
MENU_RESET = "8"

def file_exists(path):
    #Prüft, ob eine Datei existier
    try:
        with open(path, "r", encoding="utf-8"):
            return True
    except FileNotFoundError:
        return False
    except Exception:
        # andere Fehler bedeuten nicht zuverlässig 'nicht existent'
        return True


def file_read_text(path, max_bytes=None):
    with open(path, "r", encoding="utf-8") as f:
        if max_bytes is None:
            return f.read()
        return f.read(max_bytes)


def file_size(path):
    try:
        data = file_read_text(path)
        # Annahme: 1 Zeichen ~ 1 Byte in UTF-8 für grobe Anzeige (Debug)
        return len(data.encode("utf-8"))
    except Exception:
        return 0


def backup_copy_file(src_path):
    if not file_exists(src_path):
        return None
    try:
        with open(src_path, "rb") as fsrc:
            data = fsrc.read()
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        bak = f"{src_path}.bak-{ts}"
        with open(bak, "wb") as fdst:
            fdst.write(data)
        print(f"Datei gesichert als: {bak}")
        return bak
    except Exception as e:
        print("Konnte Backup nicht erstellen:", e)
        return None


# ===================== CSV-Load/Save =====================
def _normalize_for_csv(task):

    return {
        "id": str(task["id"]),
        "description": task["description"],
        "priority": task["priority"],
        "due_date": task["due_date"] or "",
        "status": task["status"],
        "created_at": task["created_at"],
    }


def _parse_from_csv(row):
    return {
        "id": int(row.get("id", "0") or "0"),
        "description": row.get("description", ""),
        "priority": row.get("priority", PRIO_MED),
        "due_date": row.get("due_date") or None,
        "status": row.get("status", STATUS_OPEN),
        "created_at": row.get("created_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def load_todos(path):
    print(f"[Speicherort] {path}")
    if not file_exists(path):
        todos = seed_tasks()
        save_todos(path, todos)
        return todos

    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            # Header prüfen
            if reader.fieldnames is None or any(h not in reader.fieldnames for h in CSV_FIELDS):
                backup_copy_file(path)
                todos = seed_tasks()
                save_todos(path, todos)
                return todos
            rows = list(reader)
        todos = [_parse_from_csv(r) for r in rows]
        if len(todos) == 0:
            todos = seed_tasks()
            save_todos(path, todos)
        return todos
    except Exception as e:
        print("CSV konnte nicht gelesen werden – Backup + Neuinitialisierung.")
        print("   Details:", e)
        backup_copy_file(path)
        todos = seed_tasks()
        save_todos(path, todos)
        return todos


def save_todos(path, todos):
    payload = [_normalize_for_csv(t) for t in todos]
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in payload:
            w.writerow(r)
    print(f"[gespeichert] {path}  (Anzahl: {len(todos)})")


# ===================== Seed & Datenmodell (Dict-basiert) =====================
def seed_tasks():
    today = datetime.now().date()
    return [
        make_task(1, "README der Aufgabe lesen", PRIO_HIGH, (today + timedelta(days=2)).strftime(DATE_FMT)),
        make_task(2, "Funktionen add/edit/delete implementieren", PRIO_MED, (today + timedelta(days=5)).strftime(DATE_FMT)),
        make_task(3, "Tests & Doku schreiben", PRIO_LOW, (today + timedelta(days=7)).strftime(DATE_FMT)),
    ]


def make_task(tid, description, priority, due_date, status=STATUS_OPEN):
    return {
        "id": int(tid),
        "description": description,
        "priority": priority,
        "due_date": due_date,  # YYYY-MM-DD oder None
        "status": status,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def next_id(todos):
    max_id = 0
    for t in todos:
        if t["id"] > max_id:
            max_id = t["id"]
    return max_id + 1


# ===================== Input-Validierung =====================
def input_nonempty(prompt):
    text = input(prompt).strip()
    while text == "":
        print("Eingabe darf nicht leer sein.")
        text = input(prompt).strip()
    return text




def is_valid_date(s):
    # Prüft, ob Datum im Format YYYY-MM-DD ist.
    try:
        datetime.strptime(s, DATE_FMT)
        return True
    except Exception:
        return False


def input_date(allow_empty=True):
    raw = input("Fälligkeitsdatum (YYYY-MM-DD, leer = kein Datum): ").strip()
    if raw == "" and allow_empty:
        return None
    while not is_valid_date(raw):
        print("Bitte Datum als YYYY-MM-DD eingeben (z. B. 2025-10-31).")
        raw = input("Fälligkeitsdatum (YYYY-MM-DD, leer = kein Datum): ").strip()
        if raw == "" and allow_empty:
            return None
    return raw


def input_int(prompt):
    raw = input(prompt).strip()
    while not raw.isdigit():
        print("Bitte eine gültige ganze Zahl eingeben.")
        raw = input(prompt).strip()
    return int(raw)


# ===================== MENU =====================
def add_task(todos):
    print("\n--- Aufgabe hinzufügen ---")
    desc = input_nonempty("Beschreibung: ")
    due = input_date(allow_empty=True)
    tid = next_id(todos)
    todos.append(make_task(tid, desc, PRIO_MED, due))
    save_todos(STORE_PATH, todos)
    print(f"Aufgabe #{tid} hinzugefügt.")


def find_task_by_id(todos, tid):
    # Sucht Aufgabe mit bestimmter ID (lineare Suche).
    for t in todos:
        if t["id"] == tid:
            return t
    return None


def edit_task(todos):
    print("\n--- Aufgabe bearbeiten ---")
    tid = input_int("ID der Aufgabe: ")
    t = find_task_by_id(todos, tid)
    if t is None:
        print("Keine Aufgabe mit dieser ID gefunden.")
        return

    print("Leerlassen, um Feld unverändert zu lassen.")
    new_desc = input(f"Neue Beschreibung [{t['description']}]: ").strip()
    if new_desc != "":
        t["description"] = new_desc

    new_prio = input(f"Neue Priorität [{PRIO_LOW}/{PRIO_MED}/{PRIO_HIGH}] (Enter=unverändert): ").strip().lower()
    if new_prio != "":
        if new_prio == PRIO_LOW or new_prio == PRIO_MED or new_prio == PRIO_HIGH:
            t["priority"] = new_prio
        else:
            print("Ungültige Priorität – unverändert belassen.")

    new_due_raw = input("Neues Fälligkeitsdatum (YYYY-MM-DD, leer=unverändert, '-'=entfernen): ").strip()
    if new_due_raw == "-":
        t["due_date"] = None
    elif new_due_raw != "":
        if is_valid_date(new_due_raw):
            t["due_date"] = new_due_raw
        else:
            print("Ungültiges Datum – unverändert belassen.")

    save_todos(STORE_PATH, todos)
    print("Aufgabe aktualisiert.")


def toggle_status(todos):
    print("\n--- Status umschalten (open/done) ---")
    tid = input_int("ID der Aufgabe: ")
    t = find_task_by_id(todos, tid)
    if t is None:
        print("Keine Aufgabe mit dieser ID gefunden.")
        return
    if t["status"] == STATUS_OPEN:
        t["status"] = STATUS_DONE
    else:
        t["status"] = STATUS_OPEN
    save_todos(STORE_PATH, todos)
    print(f"Status geändert zu '{t['status']}'.")


def delete_task(todos):
    print("\n--- Aufgabe löschen ---")
    tid = input_int("ID der Aufgabe: ")
    new_list = []
    deleted = False
    for t in todos:
        if t["id"] == tid:
            deleted = True
        else:
            new_list.append(t)
    if deleted:
        save_todos(STORE_PATH, new_list)
        todos[:] = new_list  # in-place aktualisieren
        print("Aufgabe gelöscht.")
    else:
        print("Keine Aufgabe mit dieser ID gefunden.")


# ===================== Filter/Sortierung & Anzeige =====================
def sort_key_due_then_priority(task):
    # Sortierschlüssel: Fälligkeit (None -> hinten), dann Priorität (high<med<low), dann ID.
    if task["due_date"] is None:
        due_tuple = (datetime.max.date(),)
    else:
        due_tuple = (datetime.strptime(task["due_date"], DATE_FMT).date(),)
    if task["priority"] == PRIO_HIGH:
        pr = 0
    elif task["priority"] == PRIO_MED:
        pr = 1
    else:
        pr = 2
    return due_tuple + (pr, task["id"])


def list_tasks(todos, search=None, status=None, priority=None, sort_by_due=True):
    # Filtert und sortiert Aufgaben (if/and/or).
    result = []
    for t in todos:
        ok = True
        if search is not None and search != "":
            if search.lower() not in t["description"].lower():
                ok = False
        if ok and status is not None and status != "":
            if t["status"] != status:
                ok = False
        if ok and priority is not None and priority != "":
            if t["priority"] != priority:
                ok = False
        if ok:
            result.append(t)
    if sort_by_due:
        result = sorted(result, key=sort_key_due_then_priority)
    return result


def print_tasks(tasks):
    """Tabellarische Konsolen-Ausgabe."""
    if len(tasks) == 0:
        print("Keine Aufgaben gefunden.")
        return
    print("-" * 78)
    print(f"{'ID':<4} {'Beschreibung':<40} {'Prio':<7} {'Fällig':<12} {'Status':<6}")
    print("-" * 78)
    for t in tasks:
        due = t["due_date"] if t["due_date"] is not None else "-"
        desc = t["description"][:40]
        print(f"{t['id']:<4} {desc:<40} {t['priority']:<7} {due:<12} {t['status']:<6}")
    print("-" * 78)


def reset_storage():
    print("\n--- Speicher zurücksetzen ---")
    if file_exists(STORE_PATH):
        backup_copy_file(STORE_PATH)  # erstellt Kopie
    todos = seed_tasks()
    save_todos(STORE_PATH, todos)
    print("Speicher neu initialisiert.")


# ===================== Menü & Main =====================
def show_menu():
    print("""
================= To-Do Manager (CSV) =================
1) Aufgaben anzeigen
2) Aufgabe hinzufügen
3) Aufgabe bearbeiten
4) Aufgabe als erledigt/unerledigt markieren
""")


def main():
    todos = load_todos(STORE_PATH)

    print("Beispiel-To-Dos:")
    print_tasks(list_tasks(todos, sort_by_due=True))

    choice = ""
    while choice != MENU_EXIT:
        show_menu()
        choice = input("Auswahl: ").strip()

        if choice == MENU_SHOW:
            print_tasks(list_tasks(todos, sort_by_due=True))
        elif choice == MENU_ADD:
            add_task(todos)
        elif choice == MENU_EDIT:
            edit_task(todos)
        elif choice == MENU_TOGGLE:
            toggle_status(todos)
        else:
            print("Bitte 0–8 eingeben.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAbbruch durch Benutzer.")
