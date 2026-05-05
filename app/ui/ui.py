from dataclasses import dataclass

from nicegui import ui, app
from sqlmodel import Session

from app.database.database import engine
from app.services.TodoHandler import TodoHandler
from app.services.TodoListHandler import TodoListHandler
from app.services.UserHandler import UserHandler
from app.models.todo import Todo, Status, Priority
import app.ui.draganddrop as dnd
import datetime


@dataclass
class ToDo:
    title: str


def handle_drop(todo: ToDo, location: str) -> None:
    ui.notify(f'"{todo.title}" is now in {location}')


def get_current_user_id() -> int | None:
    return app.storage.user.get("user_id")


@ui.page("/")
def index_page():
    if get_current_user_id():
        ui.navigate.to("/todos")
    else:
        ui.navigate.to("/login")


@ui.page("/todos")
def todos_page():
    user_id = get_current_user_id()

    if not user_id:
        ui.navigate.to("/login")
        return

    ui.label("Willkommen auf deiner Todo-Seite!").classes("text-3xl font-bold")
    ui.label(f"Eingeloggt als User-ID: {user_id}")

    with ui.row():
        with dnd.column("Backlog", on_drop=handle_drop):
            dnd.card(ToDo("Präsentation erstellen"))
            dnd.card(ToDo("Dokumentation schreiben"))
        with dnd.column("Doing", on_drop=handle_drop):
            dnd.card(ToDo("NiceGUI design erstellen"))
        with dnd.column("Done", on_drop=handle_drop):
            dnd.card(ToDo("Datenbank anbinden"))
            dnd.card(ToDo("models erstellen"))
            dnd.card(ToDo("services erstellen"))

    ui.button(
        "Abmelden",
        on_click=lambda: logout(),
    )


def logout():
    app.storage.user.clear()
    ui.navigate.to("/login")
