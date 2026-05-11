import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nicegui import ui
from app.database.database import init_db
from app.database.seeder.seed_users import run_seed
import app.ui.ui  # wichtig: nur importieren, damit die @ui.page-Routen registriert werden

if __name__ in {"__main__", "__mp_main__"}:
    init_db()
    run_seed()
    ui.run(storage_secret="mein-geheimes-passwort")
