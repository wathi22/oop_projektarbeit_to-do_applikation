from datetime import date
from nicegui import ui, app
from sqlmodel import Session

from app.database.database import engine
from app.services.UserHandler import UserHandler
from app.services.TodoListHandler import TodoListHandler
from app.services.TodoHandler import TodoHandler

from app.models.todo import (
    Todo,
    STATUS_BACKLOG,
    STATUS_DONE,
    PRIORITY_LOW,
    PRIORITY_MEDIUM,
    PRIORITY_HIGH,
    PRIORITY_CRITICAL,
)


def get_current_user_id() -> int | None:
    return app.storage.user.get("user_id")


def logout() -> None:
    app.storage.user.clear()
    ui.navigate.to("/login")


@ui.page("/")
def index_page():
    ui.navigate.to("/login")


@ui.page("/login")
def login_page():
    if get_current_user_id() is not None:
        ui.navigate.to("/todos")
        return

    with ui.column().classes("w-full items-center justify-center mt-20 gap-4"):
        ui.label("Login").classes("text-3xl font-bold")

        email_input = ui.input("E-Mail").classes("w-96")
        password_input = ui.input(
            "Passwort",
            password=True,
            password_toggle_button=True,
        ).classes("w-96")

        def login():
            email = (email_input.value or "").strip()
            password = password_input.value or ""

            if not email or not password:
                ui.notify("Bitte E-Mail und Passwort eingeben", color="warning")
                return

            with Session(engine) as session:
                user_handler = UserHandler(session)
                user = user_handler.get_by_email(email)

            if user is None:
                ui.notify("Benutzer nicht gefunden", color="negative")
                return

            if not user.check_password(password):
                ui.notify("Falsches Passwort", color="negative")
                return

            app.storage.user["user_id"] = user.id
            ui.notify("Login erfolgreich", color="positive")
            ui.navigate.to("/todos")

        ui.button("Einloggen", on_click=login).classes("w-96")


@ui.page("/todos")
def todo_page():
    user_id = get_current_user_id()
    if user_id is None:
        ui.navigate.to("/login")
        return

    ui.add_head_html(
        """
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
        """
    )

    selected_list_id = {"value": None}
    todo_list_column = ui.column()
    todo_column = ui.column()
    dashboard_column = ui.column().classes("w-full")

    def refresh_js_dashboard(todos: list[Todo]):
        done_count = len([todo for todo in todos if todo.status == STATUS_DONE])
        open_count = len(todos) - done_count
        avg_progress = round(sum(todo.progress for todo in todos) / len(todos)) if todos else 0

        dashboard_column.clear()
        with dashboard_column:
            ui.html(
                f"""
                <div class="w-full max-w-5xl rounded-2xl p-6 bg-gradient-to-r from-slate-900 to-slate-700 text-white shadow-xl"
                     x-data="{{ expanded: true }}">
                  <div class="flex items-center justify-between">
                    <div>
                      <h2 class="text-2xl font-semibold">To-Do Dashboard</h2>
                      <p class="text-slate-200">JS-Design direkt in eurer Hauptansicht integriert.</p>
                    </div>
                    <button class="px-4 py-2 rounded-xl bg-cyan-500 text-slate-900 font-semibold hover:bg-cyan-400 transition"
                            @click="expanded = !expanded">
                      Details umschalten
                    </button>
                  </div>
                  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6" x-show="expanded" x-transition>
                    <div class="rounded-xl p-4 bg-white/10">
                      <p class="text-sm uppercase tracking-wide text-cyan-200">Gesamt</p>
                      <p class="text-3xl font-bold">{len(todos)}</p>
                    </div>
                    <div class="rounded-xl p-4 bg-white/10">
                      <p class="text-sm uppercase tracking-wide text-cyan-200">Offen</p>
                      <p class="text-3xl font-bold">{open_count}</p>
                    </div>
                    <div class="rounded-xl p-4 bg-white/10">
                      <p class="text-sm uppercase tracking-wide text-cyan-200">Erledigt / Ø Fortschritt</p>
                      <p class="text-3xl font-bold">{done_count} / {avg_progress}%</p>
                    </div>
                  </div>
                </div>
                """
            )

    def refresh_lists():
        todo_list_column.clear()

        with Session(engine) as session:
            todo_list_handler = TodoListHandler(session)
            todo_lists = todo_list_handler.get_lists_for_user(user_id)

        with todo_list_column:
            ui.label("Meine Listen").classes("text-xl font-bold")

            for todo_list in todo_lists:
                with ui.row().classes("w-full items-center gap-2"):
                    ui.button(
                        todo_list.name,
                        on_click=lambda todo_list_id=todo_list.id: select_list(todo_list_id),
                    ).classes("flex-1")

                    ui.button(
                        "Löschen",
                        on_click=lambda todo_list_id=todo_list.id: delete_list(todo_list_id),
                    ).props("color=negative")

    def refresh_todos():
        todo_column.clear()

        if selected_list_id["value"] is None:
            refresh_js_dashboard([])
            with todo_column:
                ui.label("Bitte zuerst eine Liste auswählen.").classes("text-gray-500")
            return

        with Session(engine) as session:
            todo_handler = TodoHandler(session)
            todos = todo_handler.get_todos_for_list(selected_list_id["value"])

        refresh_js_dashboard(todos)

        with todo_column:
            ui.label("Todos").classes("text-xl font-bold")

            for todo in todos:
                is_done = todo.status == STATUS_DONE

                with ui.card().classes("w-full"):
                    with ui.row().classes("w-full items-center justify-between"):
                        with ui.column().classes("flex-1"):
                            ui.label(todo.title).classes(
                                "text-lg font-semibold line-through text-gray-400"
                                if is_done else "text-lg font-semibold"
                            )
                            ui.label(todo.description or "-").classes("text-sm text-gray-500")
                            ui.label(f"Priorität: {todo.priority}")
                            ui.label(f"Fällig: {todo.due_date or '-'}")
                            ui.label(f"Status: {todo.status}")
                            ui.label(f"Fortschritt: {todo.progress}%")

                        with ui.column().classes("gap-2"):
                            ui.button(
                                "Status wechseln",
                                on_click=lambda todo_id=todo.id: toggle_status(todo_id),
                            )
                            ui.button(
                                "Löschen",
                                on_click=lambda todo_id=todo.id: delete_todo(todo_id),
                            ).props("color=negative")

    def select_list(todo_list_id: int):
        selected_list_id["value"] = todo_list_id
        refresh_todos()

    def add_list(name_input):
        name = (name_input.value or "").strip()

        if not name:
            ui.notify("Bitte einen Listennamen eingeben", color="warning")
            return

        with Session(engine) as session:
            todo_list_handler = TodoListHandler(session)
            todo_list_handler.create_list(user_id, name)

        name_input.value = ""
        refresh_lists()

    def delete_list(todo_list_id: int):
        with Session(engine) as session:
            todo_list_handler = TodoListHandler(session)
            todo_list_handler.delete(todo_list_id)

        if selected_list_id["value"] == todo_list_id:
            selected_list_id["value"] = None

        refresh_lists()
        refresh_todos()

    def add_todo(title_input, description_input, priority_input, due_date_input):
        if selected_list_id["value"] is None:
            ui.notify("Bitte zuerst eine Liste auswählen", color="warning")
            return

        title = (title_input.value or "").strip()
        description = (description_input.value or "").strip()
        priority = priority_input.value
        due_date_raw = (due_date_input.value or "").strip()

        if not title:
            ui.notify("Bitte einen Titel eingeben", color="warning")
            return

        parsed_due_date = None
        if due_date_raw:
            try:
                parsed_due_date = date.fromisoformat(due_date_raw)
            except ValueError:
                ui.notify("Datum muss im Format YYYY-MM-DD sein", color="negative")
                return

        new_todo = Todo(
            title=title,
            description=description,
            priority=priority or PRIORITY_MEDIUM,
            status=STATUS_BACKLOG,
            progress=0,
            due_date=parsed_due_date,
            todo_list_id=selected_list_id["value"],
        )

        with Session(engine) as session:
            todo_handler = TodoHandler(session)
            todo_handler.save(new_todo)

        title_input.value = ""
        description_input.value = ""
        priority_input.value = PRIORITY_MEDIUM
        due_date_input.value = ""
        refresh_todos()

    def toggle_status(todo_id: int):
        with Session(engine) as session:
            todo_handler = TodoHandler(session)
            todo_handler.toggle_status(todo_id)

        refresh_todos()

    def delete_todo(todo_id: int):
        with Session(engine) as session:
            todo_handler = TodoHandler(session)
            todo_handler.delete(todo_id)

        refresh_todos()

    with ui.column().classes("w-full p-6 gap-6"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label("To-Do App").classes("text-3xl font-bold")
            ui.button("Logout", on_click=logout).props("color=negative")

        dashboard_column.classes("w-full")

        with ui.row().classes("w-full gap-6 items-start"):
            with ui.card().classes("w-80"):
                new_list_input = ui.input("Neue Liste").classes("w-full")
                ui.button(
                    "Liste hinzufügen",
                    on_click=lambda: add_list(new_list_input),
                ).classes("w-full")
                todo_list_column.classes("w-full gap-2")

            with ui.card().classes("flex-1"):
                title_input = ui.input("Titel").classes("w-full")
                description_input = ui.input("Beschreibung").classes("w-full")
                priority_input = ui.select(
                    [PRIORITY_LOW, PRIORITY_MEDIUM, PRIORITY_HIGH, PRIORITY_CRITICAL],
                    label="Priorität",
                    value=PRIORITY_MEDIUM,
                ).classes("w-full")
                due_date_input = ui.input("Fälligkeitsdatum (YYYY-MM-DD)").classes("w-full")

                ui.button(
                    "Todo hinzufügen",
                    on_click=lambda: add_todo(
                        title_input,
                        description_input,
                        priority_input,
                        due_date_input,
                    ),
                ).classes("w-full")

                todo_column.classes("w-full gap-3 mt-4")

    refresh_lists()
    refresh_todos()
