from nicegui import ui, app
from sqlmodel import Session

from app.database.database import engine
from app.services.TodoHandler import TodoHandler
from app.services.TodoListHandler import TodoListHandler
from app.services.UserHandler import UserHandler
from app.models.todo import Todo, Status, Priority

def get_current_user_id() -> int | None:
    return app.storage.user.get("user_id")


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

    with ui.card().classes("w-96 p-8"):
        ui.label("ToDoList Login").classes("text-2xl font-bold mb-4")

        email_input = ui.input("E-Mail").props("outlined").classes("w-full")
        password_input = ui.input("Passwort", password=True).props("outlined").classes("w-full")

        def login():
            print("LOGIN BUTTON WURDE GEKLICKT")

            email = (email_input.value or "").strip()
            password = password_input.value or ""

            print("E-Mail:", email)

            if not email or not password:
                ui.notify("Bitte E-Mail und Passwort eingeben.", color="negative")
                return

            with Session(engine) as session:
                user = UserHandler(session).get_by_email(email)

            if not user:
                ui.notify("User nicht gefunden.", color="negative")
                return

            if not user.check_password(password):
                ui.notify("Passwort falsch.", color="negative")
                return

            app.storage.user["user_id"] = user.id
            app.storage.user["user_name"] = user.full_name()

            ui.notify("Login erfolgreich.", color="positive")
            ui.navigate.to("/todos")

        ui.button("Einloggen", on_click=login).classes(
            "w-full bg-yellow-400 text-black font-bold mt-4"
        )


@ui.page("/todos")
def todos_page():
    user_id = get_current_user_id()

    if not user_id:
        ui.navigate.to("/login")
        return

    ui.label("Todo-Seite funktioniert").classes("text-3xl font-bold")
    ui.label(f"Eingeloggt als User-ID: {user_id}")

    ui.button(
        "Abmelden",
        on_click=lambda: logout(),
    )


def logout():
    app.storage.user.clear()
    ui.navigate.to("/login")


class TodoBoardPage:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.selected_list_id: int | None = None
        self.search_text = ""
        self.priority_filter = "all"

        self.board_container = None
        self.list_container = None
        self.title_label = None

    def load_lists(self):
        with Session(engine) as session:
            return TodoListHandler(session).get_lists_for_user(self.user_id)

    def load_todos(self):
        if self.selected_list_id is None:
            return []

        with Session(engine) as session:
            todos = TodoHandler(session).get_todos_for_list(self.selected_list_id)

        if self.search_text:
            todos = [
                todo for todo in todos
                if self.search_text.lower() in todo.title.lower()
                or self.search_text.lower() in todo.labels.lower()
            ]

        if self.priority_filter != "all":
            todos = [
                todo for todo in todos
                if todo.priority == self.priority_filter
            ]

        return todos

    def render(self):
        ui.query(".nicegui-content").classes("p-0")

        with ui.row().classes("w-full h-screen no-wrap bg-white"):
            self.render_sidebar()

            with ui.column().classes("flex-1 h-full no-wrap"):
                self.render_topbar()
                self.render_tabs()
                self.board_container = ui.row().classes(
                    "w-full flex-1 items-start gap-5 p-6 overflow-x-auto bg-white"
                )

        self.refresh_board()

    def render_sidebar(self):
        with ui.column().classes(
            "w-80 h-full border-r border-gray-200 bg-white p-0 no-wrap"
        ):
            with ui.row().classes("w-full items-center gap-3 px-5 py-4 border-b border-gray-200"):
                ui.label("n|w").classes(
                    "bg-yellow-400 text-black font-black px-3 py-2 rounded text-xl"
                )
                ui.label("ToDoList").classes("font-bold text-lg")

            ui.label("ARBEITSBEREICH").classes(
                "text-xs font-bold text-gray-500 tracking-widest px-5 pt-6"
            )

            self.sidebar_item("Board", active=True)
            self.sidebar_item("Liste")
            self.sidebar_item("Zeitplan")
            self.sidebar_item("Kalender")
            self.sidebar_item("Projektstatus")

            ui.label("PROJEKTLISTEN").classes(
                "text-xs font-bold text-gray-500 tracking-widest px-5 pt-8"
            )

            self.list_container = ui.column().classes("w-full gap-1 px-2")
            self.refresh_lists()

            ui.space()

            ui.button(
                "+ Neue Liste",
                on_click=self.open_create_list_dialog,
            ).props("flat").classes("mx-3 mb-4 text-yellow-600 justify-start")

    def sidebar_item(self, text: str, active: bool = False):
        classes = "w-full justify-start px-5 py-3 rounded-lg"
        if active:
            classes += " bg-yellow-100 text-black font-semibold"
        else:
            classes += " text-gray-600"

        ui.button(text).props("flat").classes(classes)

    def refresh_lists(self):
        self.list_container.clear()

        lists = self.load_lists()

        if lists and self.selected_list_id is None:
            self.selected_list_id = lists[0].id

        with self.list_container:
            for todo_list in lists:
                active = todo_list.id == self.selected_list_id

                def select_list(list_id=todo_list.id):
                    self.selected_list_id = list_id
                    self.refresh_lists()
                    self.refresh_board()
                    if self.title_label:
                        self.title_label.set_text(todo_list.name)

                ui.button(
                    todo_list.name,
                    on_click=select_list,
                ).props("flat").classes(
                    "w-full justify-start rounded-lg "
                    + ("bg-yellow-100 text-yellow-700 font-semibold" if active else "text-gray-600")
                )

    def render_topbar(self):
        with ui.row().classes(
            "w-full items-center gap-4 px-6 py-4 border-b border-gray-200 bg-white"
        ):
            with ui.column().classes("gap-0"):
                ui.label("PROTOTYP · TESTUMGEBUNG").classes(
                    "text-xs text-gray-500 tracking-widest"
                )
                self.title_label = ui.label("Arbeit").classes("text-xl font-bold")

            ui.space()

            ui.input(
                placeholder="Aufgaben suchen...",
                on_change=lambda e: self.set_search(e.value),
            ).props("outlined dense").classes("w-64")

            ui.select(
                {
                    "all": "Alle Prioritäten",
                    "low": "Niedrig",
                    "medium": "Mittel",
                    "high": "Hoch",
                    "critical": "Kritisch",
                },
                value="all",
                on_change=lambda e: self.set_priority_filter(e.value),
            ).props("outlined dense").classes("w-52")

            ui.button(
                "KI",
                icon="help_outline",
            ).props("outline").classes("text-black")

            ui.button(
                "Neue Aufgabe",
                icon="add",
                on_click=self.open_create_todo_dialog,
            ).classes("bg-yellow-400 text-black font-semibold")

    def render_tabs(self):
        with ui.row().classes("w-full gap-8 px-6 py-3 border-b border-gray-200"):
            for tab in ["Board", "Liste", "Zeitplan", "Kalender", "Projektstatus"]:
                if tab == "Board":
                    ui.label(tab).classes(
                        "font-bold text-black border-b-2 border-yellow-400 pb-2"
                    )
                else:
                    ui.label(tab).classes("text-gray-600 pb-2")

    def set_search(self, value: str):
        self.search_text = value or ""
        self.refresh_board()

    def set_priority_filter(self, value: str):
        self.priority_filter = value
        self.refresh_board()

    def refresh_board(self):
        self.board_container.clear()

        todos = self.load_todos()

        columns = [
            Status.BACKLOG,
            Status.TODO,
            Status.IN_PROGRESS,
            Status.DONE,
        ]

        with self.board_container:
            for status in columns:
                status_todos = [todo for todo in todos if todo.status == status]
                self.render_column(status, status_todos)

    def render_column(self, status: Status, todos: list[Todo]):
        color_map = {
            Status.BACKLOG: "bg-gray-400",
            Status.TODO: "bg-blue-500",
            Status.IN_PROGRESS: "bg-orange-500",
            Status.DONE: "bg-emerald-500",
        }

        with ui.card().classes(
            "w-80 min-h-56 rounded-xl border border-gray-200 shadow-none"
        ):
            with ui.row().classes("w-full items-center gap-3 border-b border-gray-200 pb-3"):
                ui.element("div").classes(f"w-3 h-3 rounded-full {color_map[status]}")
                ui.label(status.value).classes("font-bold text-lg")
                ui.space()
                ui.label(str(len(todos))).classes(
                    "px-3 py-1 rounded-full bg-gray-100 text-gray-600 text-sm"
                )

            with ui.column().classes("w-full gap-3 min-h-24"):
                for todo in todos:
                    self.render_todo_card(todo)

            ui.button(
                "+ Aufgabe hinzufügen",
                on_click=lambda s=status: self.open_create_todo_dialog(default_status=s),
            ).props("flat").classes("w-full justify-start text-gray-500")

    def render_todo_card(self, todo: Todo):
        priority_classes = {
            Priority.LOW: "bg-green-100 text-green-700",
            Priority.MEDIUM: "bg-yellow-100 text-yellow-700",
            Priority.HIGH: "bg-orange-100 text-orange-700",
            Priority.CRITICAL: "bg-red-100 text-red-700",
        }

        with ui.card().classes(
            "w-full rounded-lg border border-gray-200 shadow-none cursor-pointer"
        ).on("click", lambda t=todo: self.open_edit_todo_dialog(t)):
            ui.label(todo.title).classes("font-semibold text-base")

            if todo.description:
                ui.label(todo.description).classes("text-sm text-gray-500 line-clamp-2")

            with ui.row().classes("w-full items-center gap-2 mt-2"):
                ui.label(todo.priority.value).classes(
                    f"text-xs font-semibold px-2 py-1 rounded {priority_classes[todo.priority]}"
                )

                if todo.due_date:
                    ui.space()
                    ui.label(todo.due_date.strftime("%d.%m.")).classes(
                        "text-xs text-gray-500"
                    )

            if todo.progress > 0:
                ui.linear_progress(value=todo.progress / 100).classes("mt-2")

    def open_create_todo_dialog(self, default_status: Status = Status.TODO):
        self.open_todo_dialog(todo=None, default_status=default_status)

    def open_edit_todo_dialog(self, todo: Todo):
        self.open_todo_dialog(todo=todo, default_status=todo.status)

    def open_todo_dialog(self, todo: Todo | None, default_status: Status):
        is_new = todo is None

        with ui.dialog() as dialog, ui.card().classes("w-[500px]"):
            ui.label("Neue Aufgabe" if is_new else "Aufgabe bearbeiten").classes(
                "text-xl font-bold"
            )

            title = ui.input(
                "Titel",
                value="" if is_new else todo.title,
            ).classes("w-full")

            description = ui.textarea(
                "Beschreibung",
                value="" if is_new else todo.description,
            ).classes("w-full")

            status = ui.select(
                [s.value for s in Status],
                label="Status",
                value=default_status.value,
            ).classes("w-full")

            priority = ui.select(
                [p.value for p in Priority],
                label="Priorität",
                value=Priority.MEDIUM.value if is_new else todo.priority.value,
            ).classes("w-full")

            progress = ui.slider(
                min=0,
                max=100,
                value=0 if is_new else todo.progress,
            ).classes("w-full")

            labels = ui.input(
                "Labels, kommagetrennt",
                value="" if is_new else todo.labels,
            ).classes("w-full")

            with ui.row().classes("w-full justify-end gap-2 mt-4"):
                ui.button("Abbrechen", on_click=dialog.close).props("outline")

                if not is_new:
                    ui.button(
                        "Löschen",
                        color="red",
                        on_click=lambda: self.delete_todo(todo.id, dialog),
                    )

                ui.button(
                    "Speichern",
                    on_click=lambda: self.save_todo(
                        todo_id=None if is_new else todo.id,
                        title=title.value,
                        description=description.value,
                        status=status.value,
                        priority=priority.value,
                        progress=int(progress.value),
                        labels=labels.value,
                        dialog=dialog,
                    ),
                ).classes("bg-yellow-400 text-black")

        dialog.open()

    def save_todo(
        self,
        todo_id: int | None,
        title: str,
        description: str,
        status: str,
        priority: str,
        progress: int,
        labels: str,
        dialog,
    ):
        with Session(engine) as session:
            handler = TodoHandler(session)

            if todo_id is None:
                todo = Todo(
                    title=title,
                    description=description,
                    status=Status(status),
                    priority=Priority(priority),
                    progress=progress,
                    labels=labels,
                    todo_list_id=self.selected_list_id,
                )
                handler.save(todo)
            else:
                handler.update(
                    todo_id,
                    title=title,
                    description=description,
                    status=status,
                    priority=priority,
                    progress=progress,
                    labels=labels,
                )

        dialog.close()
        self.refresh_board()

    def delete_todo(self, todo_id: int, dialog):
        with Session(engine) as session:
            TodoHandler(session).delete(todo_id)

        dialog.close()
        self.refresh_board()

    def open_create_list_dialog(self):
        with ui.dialog() as dialog, ui.card().classes("w-96"):
            ui.label("Neue Liste erstellen").classes("text-xl font-bold")
            name = ui.input("Listenname").classes("w-full")

            with ui.row().classes("w-full justify-end gap-2"):
                ui.button("Abbrechen", on_click=dialog.close).props("outline")
                ui.button(
                    "Erstellen",
                    on_click=lambda: self.create_list(name.value, dialog),
                ).classes("bg-yellow-400 text-black")

        dialog.open()

    def create_list(self, name: str, dialog):
        if not name.strip():
            ui.notify("Bitte einen Namen eingeben.", color="negative")
            return

        with Session(engine) as session:
            new_list = TodoListHandler(session).create_list(self.user_id, name)

        self.selected_list_id = new_list.id
        dialog.close()
        self.refresh_lists()
        self.refresh_board()

