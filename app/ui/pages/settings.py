from nicegui import ui

from app.ui.layout import create_app_layout, require_login


@ui.page("/settings")
def settings_page():
    if not require_login():
        return

    create_app_layout("Einstellungen", "/settings")

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("Einstellungen").classes("text-3xl font-bold")
        ui.label("Hier ist Platz fuer zukuenftige Benutzer- und App-Einstellungen.").classes("text-gray-600")
