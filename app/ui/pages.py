from nicegui import ui, app
from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from app.database.database import engine
from app.services.UserHandler import UserHandler
from app.services.TodoListHandler import TodoListHandler
from app.services.TodoHandler import TodoHandler
from app.models.user import User
from app.models.todo import Todo

from app.ui.session import _get_user_id, _create_session, _destroy_session
from app.ui.ui import TodoBoardPage

# ─── NiceGUI Pages ────────────────────────────────────────────────────────────
def _redirect_to_login():
    ui.open('/login')


@ui.page('/')
def index_page():
    ui.run_javascript("window.location.href = '/login';")


@ui.page('/login')
def login_page():
       # JavaScript code for handling login form submission
        login_js = """(async function() {
            const email = document.getElementById('login-email').value.trim();
            const password = document.getElementById('login-password').value;
            const btn = document.getElementById('login-btn');
            const err = document.getElementById('login-error');
            err.style.display = 'none';
            if (!email || !password) { err.textContent = 'Bitte E-Mail und Passwort eingeben.'; err.style.display = 'block'; return; }
            btn.disabled = true; btn.textContent = 'Einloggen…';
            try {
                const resp = await fetch('/api/auth/login', {
                    method: 'POST', headers: {'Content-Type':'application/json'},
                    body: JSON.stringify({email, password})
                });
                const data = await resp.json();
                if (data.success) {
                    const id = data.user_id || '';
                    window.location.href = `/todos/${id}`;
                } else {
                    err.textContent = data.error || 'Fehler beim Einloggen'; err.style.display = 'block';
                }
            } catch(e) {
                err.textContent = 'Verbindungsfehler. Bitte erneut versuchen.'; err.style.display = 'block';
            }
            btn.disabled = false; btn.textContent = 'Einloggen';
        })();"""

        with ui.column().classes('items-center justify-center h-screen'):
                ui.label('ToDoList').classes('text-2xl font-bold')
                with ui.card().classes('w-96 p-6'):
                        ui.input('E-Mail').props('id=login-email placeholder=name@beispiel.ch')
                        ui.input('Passwort').props('id=login-password type=password placeholder=••••••••')
                        ui.label('').props('id=login-error').classes('text-negative').style('display:none')
                        ui.button('Einloggen', on_click=lambda: ui.run_javascript(login_js)).props('id=login-btn').classes('w-full bg-yellow-400 text-black')
                        ui.link('Registrieren', '/register')


@ui.page('/register')
def register_page():
        register_js = """(async function() {
            const firstname = document.getElementById('reg-firstname').value.trim();
            const lastname  = document.getElementById('reg-lastname').value.trim();
            const email     = document.getElementById('reg-email').value.trim();
            const password  = document.getElementById('reg-password').value;
            const password2 = document.getElementById('reg-password2').value;
            const btn = document.getElementById('reg-btn');
            const err = document.getElementById('reg-error');
            err.style.display = 'none';
            if (!firstname || !lastname || !email || !password) { err.textContent = 'Bitte alle Felder ausfüllen.'; err.style.display = 'block'; return; }
            if (password.length < 8) { err.textContent = 'Das Passwort muss mindestens 8 Zeichen lang sein.'; err.style.display = 'block'; return; }
            if (password !== password2) { err.textContent = 'Die Passwörter stimmen nicht überein.'; err.style.display = 'block'; return; }
            btn.disabled = true; btn.textContent = 'Registrieren…';
            try {
                const resp = await fetch('/api/auth/register', {
                    method: 'POST', headers: {'Content-Type':'application/json'},
                    body: JSON.stringify({firstname, lastname, email, password})
                });
                const data = await resp.json();
                if (data.success) {
                    const id = data.user_id || '';
                    window.location.href = `/todos/${id}`;
                } else {
                    err.textContent = data.error || 'Fehler bei der Registrierung'; err.style.display = 'block';
                }
            } catch(e) {
                err.textContent = 'Verbindungsfehler. Bitte erneut versuchen.'; err.style.display = 'block';
            }
            btn.disabled = false; btn.textContent = 'Registrieren';
        })();"""

        with ui.column().classes('items-center justify-center h-screen'):
                ui.label('Registrierung').classes('text-2xl font-bold')
                with ui.card().classes('w-96 p-6'):
                        ui.input('Vorname').props('id=reg-firstname placeholder=Max')
                        ui.input('Nachname').props('id=reg-lastname placeholder=Muster')
                        ui.input('E-Mail').props('id=reg-email placeholder=name@beispiel.ch')
                        ui.input('Passwort').props('id=reg-password type=password placeholder=Mindestens 8 Zeichen')
                        ui.input('Passwort wiederholen').props('id=reg-password2 type=password placeholder=Passwort bestätigen')
                        ui.label('').props('id=reg-error').classes('text-negative').style('display:none')
                        ui.button('Registrieren', on_click=lambda: ui.run_javascript(register_js)).props('id=reg-btn').classes('w-full bg-yellow-400 text-black')
                        ui.link('Einloggen', '/login')


@ui.page('/todos')
def todos_page(request=None):
    # Use FastAPI request to get session cookie (injected by NiceGUI/FastAPI)
    # If request not provided by NiceGUI, fall back to redirect to login.
    try:
        # fastapi.Request may be passed in by NiceGUI
        user_id = None
        if request is not None:
            # request may be a starlette.requests.Request
            user = request
            from app.ui.session import _get_user_id as _get
            user_id = _get(request)
    except Exception:
        user_id = None

    if not user_id:
        ui.run_javascript("window.location.href = '/login';")
        return

    page = TodoBoardPage(user_id)
    page.render()
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