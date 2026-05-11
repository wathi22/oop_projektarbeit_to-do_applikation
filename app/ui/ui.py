from nicegui import ui

from app.ui.layout import get_current_user_id
import app.ui.pages


@ui.page("/")
def index_page():
    if get_current_user_id():
        ui.navigate.to("/todos")
    else:
        ui.navigate.to("/login")
