from datetime import date, datetime

from nicegui import ui
from sqlmodel import Session

from app.database.database import engine
from app.models.todo import Status, Todo
from app.services.TodoHandler import TodoHandler
import app.ui.draganddrop as dnd


COLUMNS = [
    ("Backlog", (Status.BACKLOG, Status.TODO)),
    ("Doing", (Status.IN_PROGRESS,)),
    ("Done", (Status.DONE,)),
]


def parse_due_date(value: str | None) -> date | None:
    if not value:
        return None

    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def create_todo(todo_list_id: int, title: str, due_date: date | None = None) -> None:
    with Session(engine) as session:
        TodoHandler(session).save(
            Todo(
                title=title,
                status=Status.BACKLOG,
                progress=0,
                due_date=due_date,
                todo_list_id=todo_list_id,
            )
        )


def load_todos(todo_list_id: int) -> list[Todo]:
    with Session(engine) as session:
        return TodoHandler(session).get_todos_for_list(todo_list_id)


def update_todo_status(todo_id: int, status: Status) -> None:
    with Session(engine) as session:
        progress = 100 if status == Status.DONE else 0
        TodoHandler(session).update(todo_id, status=status.value, progress=progress)


def render_todo_board(todo_list_id: int) -> None:
    title_input = None
    due_date_input = None

    def add_todo() -> None:
        title = (title_input.value or "").strip()
        due_date = parse_due_date(due_date_input.value)
        if not title:
            ui.notify("Bitte gib einen Todo-Titel ein.", color="warning")
            return

        create_todo(todo_list_id, title, due_date)
        title_input.value = ""
        due_date_input.value = None
        ui.notify("Todo erstellt.", color="positive")
        board.refresh()

    def handle_drop(todo: Todo, column_name: str) -> None:
        status = next(statuses[0] for name, statuses in COLUMNS if name == column_name)
        if todo.id is not None:
            update_todo_status(todo.id, status)
        board.refresh()

    @ui.refreshable
    def board() -> None:
        todos = load_todos(todo_list_id)

        with ui.row().classes("w-full gap-4"):
            for column_name, statuses in COLUMNS:
                column_todos = [todo for todo in todos if todo.status in statuses]
                with dnd.column(column_name, on_drop=handle_drop):
                    if not column_todos:
                        ui.label("Keine Todos").classes("text-gray-500 text-sm")
                    for todo in column_todos:
                        dnd.card(todo)

    with ui.row().classes("w-full max-w-3xl items-end gap-3"):
        title_input = ui.input("Neues Todo", placeholder="z.B. Dokumentation fertigstellen").props(
            "outlined"
        ).classes("grow")
        due_date_input = ui.input("Erledigungsdatum", value=date.today().isoformat()).props("type=date outlined")
        title_input.on("keydown.enter", lambda event: add_todo())
        ui.button("Hinzufügen", icon="add", on_click=add_todo).classes("bg-yellow-400 text-black")

    board()
