from datetime import date

from nicegui import ui, app
from sqlmodel import Session

from app.database.database import engine
from app.services.UserHandler import UserHandler
from app.services.TodoListHandler import TodoListHandler
from app.services.TodoHandler import TodoHandler
from app.models.todo import Todo, Status, Priority


def get_current_user_id() -> int | None:
    return app.storage.user.get("user_id")


def require_login() -> int | None:
    user_id = get_current_user_id()
    if not user_id:
        ui.navigate.to("/login")
        return None
    return user_id


@ui.page("/")
def index_page():
    if get_current_user_id():
        ui.navigate.to("/todos")
    else:
        ui.navigate.to("/login")


@ui.page("/login")
def login_page():
    ui.query(".nicegui-content").classes(
        "w-full h-screen flex items-center justify-center bg-gray-50"
    )

    with ui.card().classes("w-96 p-8 shadow-lg"):
        ui.label("ToDoList").classes("text-3xl font-bold")
        ui.label("Objektorientierte Programmierung").classes("text-gray-500 mb-4")

        email_input = ui.input("E-Mail").props("outlined").classes("w-full")
        password_input = ui.input("Passwort", password=True).props("outlined").classes("w-full")

        def login():
            email = email_input.value.strip()
            password = password_input.value

            if not email or not password:
                ui.notify("Bitte E-Mail und Passwort eingeben.", color="negative")
                return

            with Session(engine) as session:
                user = UserHandler(session).get_by_email(email)

            if not user or not user.check_password(password):
                ui.notify("E-Mail oder Passwort falsch.", color="negative")
                return

            app.storage.user["user_id"] = user.id
            app.storage.user["user_name"] = user.full_name()

            ui.notify(f"Willkommen, {user.full_name()}!", color="positive")
            ui.navigate.to("/todos")

        ui.button("Einloggen", on_click=login).classes(
            "w-full bg-yellow-400 text-black font-bold"
        )

        ui.separator()

        ui.label("Test-Login:").classes("text-sm text-gray-500 mt-2")
        ui.label("wathanak.deng@example.com / password123").classes("text-xs text-gray-400")


@ui.page("/todos")
def todos_page():
    user_id = require_login()
    if user_id is None:
        return

    ui.query(".nicegui-content").classes("p-0")

    selected_list_id: int | None = None
    board_container = ui.column()

    def load_lists():
        with Session(engine) as session:
            return TodoListHandler(session).get_lists_for_user(user_id)

    def ensure_first_list() -> int:
        lists = load_lists()

        if lists:
            return lists[0].id

        with Session(engine) as session:
            new_list = TodoListHandler(session).create_list(user_id, "Meine Liste")
            return new_list.id

    selected_list_id = ensure_first_list()

    def load_todos():
        with Session(engine) as session:
            return TodoHandler(session).get_todos_for_list(selected_list_id)

    def refresh_board():
        board_container.clear()
        todos = load_todos()

        columns = [
            Status.BACKLOG,
            Status.TODO,
            Status.IN_PROGRESS,
            Status.DONE,
        ]

        with board_container:
            with ui.row().classes("w-full gap-4 items-start overflow-x-auto"):
                for status in columns:
                    status_todos = [todo for todo in todos if todo.status == status]
                    render_column(status, status_todos)

    def render_column(status: Status, todos: list[Todo]):
        color_map = {
            Status.BACKLOG: "bg-gray-400",
            Status.TODO: "bg-blue-500",
            Status.IN_PROGRESS: "bg-orange-500",
            Status.DONE: "bg-green-500",
        }

        with ui.card().classes("w-80 min-h-96 shadow-none border"):
            with ui.row().classes("w-full items-center"):
                ui.element("div").classes(f"w-3 h-3 rounded-full {color_map[status]}")
                ui.label(status.value).classes("font-bold text-lg")
                ui.space()
                ui.label(str(len(todos))).classes(
                    "bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-sm"
                )

            ui.separator()

            for todo in todos:
                render_todo_card(todo)

            ui.button(
                "+ Aufgabe hinzufügen",
                on_click=lambda s=status: open_create_todo_dialog(s),
            ).props("flat").classes("w-full justify-start text-gray-500")

    def render_todo_card(todo: Todo):
        priority_classes = {
            Priority.LOW: "bg-green-100 text-green-700",
            Priority.MEDIUM: "bg-yellow-100 text-yellow-700",
            Priority.HIGH: "bg-orange-100 text-orange-700",
            Priority.CRITICAL: "bg-red-100 text-red-700",
        }

        with ui.card().classes("w-full shadow-none border cursor-pointer"):
            ui.label(todo.title).classes("font-semibold")

            if todo.description:
                ui.label(todo.description).classes("text-sm text-gray-500")

            with ui.row().classes("w-full items-center gap-2"):
                ui.label(todo.priority.value).classes(
                    f"text-xs px-2 py-1 rounded font-semibold {priority_classes[todo.priority]}"
                )

                if todo.due_date:
                    ui.space()
                    ui.label(todo.due_date.strftime("%d.%m.%Y")).classes(
                        "text-xs text-gray-500"
                    )

            ui.linear_progress(value=todo.progress / 100).classes("mt-2")

            with ui.row().classes("w-full gap-2 mt-2"):
                ui.button(
                    "Status weiter",
                    on_click=lambda t=todo: toggle_todo_status(t.id),
                ).props("outline size=sm")

                ui.button(
                    "Löschen",
                    on_click=lambda t=todo: delete_todo(t.id),
                ).props("outline size=sm color=red")

    def open_create_todo_dialog(default_status: Status):
        with ui.dialog() as dialog, ui.card().classes("w-[500px]"):
            ui.label("Neue Aufgabe").classes("text-xl font-bold")

            title = ui.input("Titel").classes("w-full")
            description = ui.textarea("Beschreibung").classes("w-full")

            priority = ui.select(
                [p.value for p in Priority],
                label="Priorität",
                value=Priority.MEDIUM.value,
            ).classes("w-full")

            progress = ui.slider(min=0, max=100, value=0).classes("w-full")
            progress_label = ui.label("Fortschritt: 0 %")

            progress.on(
                "update:model-value",
                lambda e: progress_label.set_text(f"Fortschritt: {int(e.args)} %"),
            )

            labels = ui.input("Labels, kommagetrennt").classes("w-full")

            with ui.row().classes("w-full justify-end gap-2"):
                ui.button("Abbrechen", on_click=dialog.close).props("outline")

                def save():
                    if not title.value.strip():
                        ui.notify("Bitte einen Titel eingeben.", color="negative")
                        return

                    todo = Todo(
                        title=title.value.strip(),
                        description=description.value or "",
                        status=default_status,
                        priority=Priority(priority.value),
                        progress=int(progress.value),
                        labels=labels.value or "",
                        todo_list_id=selected_list_id,
                        start_date=date.today(),
                    )

                    with Session(engine) as session:
                        TodoHandler(session).save(todo)

                    dialog.close()
                    refresh_board()
                    ui.notify("Aufgabe erstellt.", color="positive")

                ui.button("Speichern", on_click=save).classes(
                    "bg-yellow-400 text-black font-bold"
                )

        dialog.open()

    def toggle_todo_status(todo_id: int):
        with Session(engine) as session:
            TodoHandler(session).toggle_status(todo_id)

        refresh_board()

    def delete_todo(todo_id: int):
        with Session(engine) as session:
            TodoHandler(session).delete(todo_id)

        refresh_board()
        ui.notify("Aufgabe gelöscht.")

    def logout():
        app.storage.user.clear()
        ui.navigate.to("/login")

    with ui.row().classes("w-full h-screen no-wrap"):
        with ui.column().classes("w-72 h-full border-r bg-white p-4 no-wrap"):
            ui.label("ToDoList").classes("text-2xl font-bold")
            ui.label(app.storage.user.get("user_name", "User")).classes("text-gray-500")

            ui.separator()

            ui.label("PROJEKTLISTEN").classes(
                "text-xs font-bold text-gray-500 tracking-widest mt-4"
            )

            for todo_list in load_lists():
                active = todo_list.id == selected_list_id

                def select_list(list_id=todo_list.id):
                    nonlocal selected_list_id
                    selected_list_id = list_id
                    refresh_board()

                ui.button(todo_list.name, on_click=select_list).props("flat").classes(
                    "w-full justify-start "
                    + ("bg-yellow-100 text-black font-bold" if active else "text-gray-600")
                )

            ui.space()

            ui.button("Abmelden", on_click=logout).props("outline").classes("w-full")

        with ui.column().classes("flex-1 h-full bg-gray-50 no-wrap"):
            with ui.row().classes("w-full items-center bg-white border-b px-6 py-4"):
                ui.label("Meine Aufgaben").classes("text-2xl font-bold")
                ui.space()
                ui.button(
                    "Neue Aufgabe",
                    icon="add",
                    on_click=lambda: open_create_todo_dialog(Status.TODO),
                ).classes("bg-yellow-400 text-black font-bold")

            board_container.classes("flex-1 p-6 overflow-auto")
            refresh_board()