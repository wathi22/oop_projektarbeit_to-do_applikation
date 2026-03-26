import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nicegui import ui
from app.database.database import init_db
from app.ui.ui import todo_page

if __name__ in {"__main__", "__mp_main__"}:
    init_db()
    todo_page()
    ui.run()