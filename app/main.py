import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nicegui import ui
from app.database.database import init_db
import app.ui.ui  # wichtig: nur importieren, damit die @ui.page-Routen registriert werden

import app.ui.pages  # NiceGUI-based pages (login/register/todos)

if __name__ in {"__main__", "__mp_main__"}:
    init_db()
    from app.database.seeder.seed_users import seed_users, run_seed
    seed_users()  # Füge Test-User zur Datenbank hinzu
    run_seed()
    ui.run(storage_secret="mein-geheimes-passwort")
