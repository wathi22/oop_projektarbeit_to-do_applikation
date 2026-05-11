from datetime import date, datetime

from nicegui import ui
from sqlmodel import Session

from app.database.database import engine
from app.models.todo import Status, Todo
from app.services.TodoHandler import TodoHandler
from app.ui.layout import get_label_filter
import app.ui.draganddrop as dnd


PRIORITY_OPTIONS = {
    "high": "High",
    "medium": "Middle",
    "low": "Low",
}

STATUS_OPTIONS = {
    Status.BACKLOG.value: "Backlog",
    Status.IN_PROGRESS.value: "Doing",
    Status.DONE.value: "Done",
}

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


def create_todo(
    todo_list_id: int,
    title: str,
    due_date: date | None = None,
    description: str = "",
    priority: str = "low",
    status: str = Status.BACKLOG.value,
    progress: int = 0,
    start_date: date | None = None,
    labels: str = "",
) -> None:
    with Session(engine) as session:
        TodoHandler(session).save(
            Todo(
                title=title,
                description=description,
                priority=priority,
                status=status,
                progress=progress,
                start_date=start_date,
                due_date=due_date,
                labels=labels,
                todo_list_id=todo_list_id,
            )
        )


def load_todos(todo_list_id: int, apply_label_filter: bool = True) -> list[Todo]:
    with Session(engine) as session:
        todos = TodoHandler(session).get_todos_for_list(todo_list_id)

    if not apply_label_filter:
        return todos

    label_filter = get_label_filter()
    if label_filter == "all":
        return todos

    return [todo for todo in todos if todo.labels == label_filter]


def update_todo_status(todo_id: int, status: Status) -> None:
    with Session(engine) as session:
        progress = 100 if status == Status.DONE else 0
        TodoHandler(session).update(todo_id, status=status.value, progress=progress)


def render_create_todo_dialog(todo_list_id: int, on_created) -> None:
    title_input = description_input = start_date_input = due_date_input = labels_select = None
    priority_select = status_select = progress_slider = None

    def default_label() -> str:
        label_filter = get_label_filter()
        if label_filter in {"arbeit", "private"}:
            return label_filter
        return "arbeit"

    def reset_form() -> None:
        title_input.value = ""
        description_input.value = ""
        priority_select.value = "low"
        status_select.value = Status.BACKLOG.value
        progress_slider.value = 0
        start_date_input.value = None
        due_date_input.value = date.today().isoformat()
        labels_select.value = default_label()

    def save_todo() -> None:
        title = (title_input.value or "").strip()
        description = (description_input.value or "").strip()
        start_date = parse_due_date(start_date_input.value)
        due_date = parse_due_date(due_date_input.value)
        priority = priority_select.value or "low"
        status = status_select.value or Status.BACKLOG.value
        progress = int(progress_slider.value or 0)
        labels = labels_select.value or ""

        if not title:
            ui.notify("Bitte gib einen Todo-Titel ein.", color="warning")
            return

        create_todo(
            todo_list_id=todo_list_id,
            title=title,
            description=description,
            priority=priority,
            status=status,
            progress=progress,
            start_date=start_date,
            due_date=due_date,
            labels=labels,
        )

        ui.notify("Todo erstellt.", color="positive")
        dialog.close()
        reset_form()
        on_created()

    with ui.dialog() as dialog, ui.card().classes("w-full max-w-2xl p-6"):
        ui.label("Neue Todo erfassen").classes("text-2xl font-bold")

        with ui.grid(columns=2).classes("w-full gap-4"):
            ui.input("ID", value="wird automatisch erstellt").props("outlined readonly").classes("w-full")
            title_input = ui.input("Title").props("outlined").classes("w-full")
            description_input = ui.textarea("Description").props("outlined").classes("w-full col-span-2")
            priority_select = ui.select(PRIORITY_OPTIONS, label="Priority", value="low").props("outlined").classes(
                "w-full"
            )
            status_select = ui.select(STATUS_OPTIONS, label="Status", value=Status.BACKLOG.value).props(
                "outlined"
            ).classes("w-full")
            progress_slider = ui.slider(min=0, max=100, value=0).props("label-always").classes("w-full col-span-2")
            start_date_input = ui.input("Start Date").props("type=date outlined").classes("w-full")
            due_date_input = ui.input("Due Date", value=date.today().isoformat()).props("type=date outlined").classes(
                "w-full"
            )
            labels_select = ui.select(
                {"arbeit": "Arbeit", "private": "Private"},
                label="Labels",
                value=default_label(),
            ).props("outlined").classes("w-full")

        with ui.row().classes("w-full justify-end gap-2"):
            ui.button("Abbrechen", on_click=dialog.close).props("flat")
            ui.button("Speichern", icon="save", on_click=save_todo).classes("bg-yellow-400 text-black")

    ui.button("Neue Todo erfassen", icon="add", on_click=dialog.open).classes("bg-yellow-400 text-black")


def render_todo_board(todo_list_id: int) -> None:
    def refresh_board() -> None:
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

    render_create_todo_dialog(todo_list_id, refresh_board)
    board()
