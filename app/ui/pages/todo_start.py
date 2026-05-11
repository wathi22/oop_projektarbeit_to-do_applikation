from dataclasses import dataclass

from nicegui import ui

from app.ui.layout import create_app_layout, require_login
import app.ui.draganddrop as dnd


@dataclass
class ToDo:
    title: str


def handle_drop(todo: ToDo, location: str) -> None:
    ui.notify(f'"{todo.title}" is now in {location}')


@ui.page("/todos")
def todos_page():
    user_id = require_login()
    if not user_id:
        return

    create_app_layout("Todos", "/todos")
    backlog_todos = [
        ToDo("Präsentation erstellen"),
        ToDo("Dokumentation schreiben"),
    ]
    title_input = None

    def create_todo():
        title = (title_input.value or "").strip()
        if not title:
            ui.notify("Bitte gib einen Todo-Titel ein.", color="warning")
            return

        backlog_todos.append(ToDo(title))
        title_input.value = ""
        board.refresh()

    @ui.refreshable
    def board():
        with ui.row().classes("w-full gap-4"):
            with dnd.column("Backlog", on_drop=handle_drop):
                for todo in backlog_todos:
                    dnd.card(todo)
            with dnd.column("Doing", on_drop=handle_drop):
                dnd.card(ToDo("NiceGUI design erstellen"))
            with dnd.column("Done", on_drop=handle_drop):
                dnd.card(ToDo("Datenbank anbinden"))
                dnd.card(ToDo("models erstellen"))
                dnd.card(ToDo("services erstellen"))

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("Willkommen auf deiner Todo-Seite!").classes("text-3xl font-bold")

        with ui.row().classes("w-full gap-4"):
            title_input = ui.input(placeholder="Neue Todo hinzufügen...").props("outlined").classes("w-full max-w-md")
            title_input.on("keydown.enter", lambda event: create_todo())
            ui.button("Hinzufügen", on_click=create_todo).props("icon=add")

        board()
