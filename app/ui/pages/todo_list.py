from nicegui import ui
from sqlmodel import Session

from app.database.database import engine
from app.models.todo import Status, Todo
from app.services.TodoHandler import TodoHandler
from app.ui.layout import create_app_layout, get_or_create_default_todo_list, require_login


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
