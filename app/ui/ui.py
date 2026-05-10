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


NAVIGATION_ITEMS = [
    {"label": "Todos", "icon": "checklist", "path": "/todos"},
    {"label": "Listen", "icon": "view_list", "path": "/lists"},
    {"label": "Einstellungen", "icon": "settings", "path": "/settings"},
]


@dataclass
class ToDo:
    title: str


def handle_drop(todo: ToDo, location: str) -> None:
    ui.notify(f'"{todo.title}" is now in {location}')


def get_current_user_id() -> int | None:
    return app.storage.user.get("user_id")


def require_login() -> int | None:
    user_id = get_current_user_id()
    if not user_id:
        ui.navigate.to("/login")
        return None
    return user_id


def get_or_create_default_todo_list(user_id: int) -> int:
    with Session(engine) as session:
        handler = TodoListHandler(session)
        todo_lists = handler.get_lists_for_user(user_id)

        if todo_lists:
            return todo_lists[0].id

        todo_list = handler.create_list(user_id, "Meine Todos")
        return todo_list.id


def logout():
    app.storage.user.clear()
    ui.navigate.to("/login")


def create_app_layout(title: str, active_path: str) -> None:
    user_name = app.storage.user.get("user_name") or "Benutzer"

    with ui.header(elevated=True).classes("bg-white text-gray-900 border-b border-gray-200"):
        ui.button(icon="menu", on_click=lambda: drawer.toggle()).props("flat round dense")
        ui.label(title).classes("text-lg font-semibold")
        ui.space()
        ui.label(user_name).classes("text-sm text-gray-600")

    with ui.left_drawer(value=True).props("width=260 bordered").classes("bg-gray-900 text-white") as drawer:
        with ui.column().classes("w-full h-full p-4 gap-2"):
            ui.label("ToDoList").classes("text-2xl font-bold mb-4")

            for item in NAVIGATION_ITEMS:
                is_active = item["path"] == active_path
                button_classes = "w-full justify-start text-left"
                button_color = "bg-yellow-400 text-black" if is_active else "text-white"

                ui.button(
                    item["label"],
                    icon=item["icon"],
                    on_click=lambda path=item["path"]: ui.navigate.to(path),
                ).props("flat align=left").classes(f"{button_classes} {button_color}")

            ui.space()
            ui.separator().classes("bg-gray-700")
            ui.button("Abmelden", icon="logout", on_click=logout).props("flat align=left").classes(
                "w-full justify-start text-white"
            )


@ui.page("/")
def index_page():
    if get_current_user_id():
        ui.navigate.to("/todos")
    else:
        ui.navigate.to("/login")


@ui.page("/todos")
def todos_page():
    user_id = require_login()
    if not user_id:
        return

    create_app_layout("Todos", "/todos")

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("Willkommen auf deiner Todo-Seite!").classes("text-3xl font-bold")
        ui.label(f"Eingeloggt als User-ID: {user_id}").classes("text-gray-600")

        with ui.row().classes("w-full gap-4"):
            with dnd.column("Backlog", on_drop=handle_drop):
                dnd.card(ToDo("Präsentation erstellen"))
                dnd.card(ToDo("Dokumentation schreiben"))
            with dnd.column("Doing", on_drop=handle_drop):
                dnd.card(ToDo("NiceGUI design erstellen"))
            with dnd.column("Done", on_drop=handle_drop):
                dnd.card(ToDo("Datenbank anbinden"))
                dnd.card(ToDo("models erstellen"))
                dnd.card(ToDo("services erstellen"))


@ui.page("/lists")
def lists_page():
    user_id = require_login()
    if not user_id:
        return

    create_app_layout("Listen", "/lists")
    todo_list_id = get_or_create_default_todo_list(user_id)

    title_input = None

    def create_todo():
        title = (title_input.value or "").strip()
        if not title:
            ui.notify("Bitte gib einen Todo-Titel ein.", color="warning")
            return

        with Session(engine) as session:
            TodoHandler(session).save(
                Todo(
                    title=title,
                    status=Status.BACKLOG,
                    progress=0,
                    todo_list_id=todo_list_id,
                )
            )

        title_input.value = ""
        ui.notify("Todo erstellt.", color="positive")
        todo_list_view.refresh()

    def set_todo_done(todo_id: int, is_done: bool):
        with Session(engine) as session:
            status = Status.DONE.value if is_done else Status.BACKLOG.value
            progress = 100 if is_done else 0
            TodoHandler(session).update(todo_id, status=status, progress=progress)

        todo_list_view.refresh()

    @ui.refreshable
    def todo_list_view():
        with Session(engine) as session:
            todos = TodoHandler(session).get_todos_for_list(todo_list_id)

        if not todos:
            ui.label("Noch keine Todos vorhanden. Erstelle oben dein erstes Todo.").classes("text-gray-500")
            return

        with ui.list().props("bordered separator").classes("w-full max-w-3xl bg-white"):
            for todo in todos:
                is_done = todo.status == Status.DONE
                with ui.item().classes("items-center"):
                    ui.checkbox(
                        value=is_done,
                        on_change=lambda event, todo_id=todo.id: set_todo_done(todo_id, event.value),
                    )
                    with ui.item_section():
                        title_classes = "text-base"
                        if is_done:
                            title_classes += " line-through text-gray-400"
                        ui.item_label(todo.title).classes(title_classes)
                        ui.item_label(todo.status.value).props("caption").classes("text-gray-500")
                    ui.space()
                    ui.badge("Erledigt" if is_done else "Offen").props(
                        "color=positive" if is_done else "color=grey"
                    )

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("Todo-Listen").classes("text-3xl font-bold")
        ui.label("Einfache Übersicht deiner Todos.").classes("text-gray-600")

        with ui.row().classes("w-full max-w-3xl items-end gap-3"):
            title_input = ui.input("Neues Todo", placeholder="z.B. Dokumentation fertigstellen").props(
                "outlined"
            ).classes("grow")
            title_input.on("keydown.enter", lambda event: create_todo())
            ui.button("Hinzufügen", icon="add", on_click=create_todo).classes("bg-yellow-400 text-black")

        todo_list_view()


@ui.page("/settings")
def settings_page():
    if not require_login():
        return

    create_app_layout("Einstellungen", "/settings")

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("Einstellungen").classes("text-3xl font-bold")
        ui.label("Hier ist Platz fuer zukuenftige Benutzer- und App-Einstellungen.").classes("text-gray-600")
