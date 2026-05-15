from datetime import date, datetime
from pathlib import Path
from uuid import uuid4

from nicegui import app, ui
from sqlmodel import Session

from app.database.database import engine
from app.models.todo import Priority, Status, Todo
from app.services.TodoHandler import TodoHandler
from app.ui.layout import get_label_filter
import app.ui.draganddrop as dnd


UPLOAD_DIR = Path(__file__).resolve().parents[3] / "uploads" / "todos"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.add_static_files("/todo-uploads", UPLOAD_DIR)

PRIORITY_OPTIONS = {
    "high": "High",
    "medium": "Middle",
    "low": "Low",
}

STATUS_OPTIONS = {
    Status.BACKLOG.value: "Backlog",
    Status.TODO.value: "To-Do",
    Status.IN_PROGRESS.value: "In Progress",
    Status.DONE.value: "Done",
}

COLUMNS = [
    ("Backlog", (Status.BACKLOG,)),
    ("To-Do", (Status.TODO,)),
    ("In Progress", (Status.IN_PROGRESS,)),
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
    link: str = "",
    attachment_path: str = "",
    attachment_name: str = "",
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
                link=link,
                attachment_path=attachment_path,
                attachment_name=attachment_name,
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


def delete_todo(todo_id: int) -> bool:
    with Session(engine) as session:
        return TodoHandler(session).delete(todo_id)


def update_todo_details(
    todo_id: int,
    title: str,
    description: str,
    link: str,
    attachment_path: str,
    attachment_name: str,
    priority: str,
    status: str,
    progress: int,
    start_date: date | None,
    due_date: date | None,
    labels: str,
) -> None:
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            return

        todo.title = title
        todo.description = description
        todo.link = link
        todo.attachment_path = attachment_path
        todo.attachment_name = attachment_name
        todo.priority = Priority(priority)
        todo.status = Status(status)
        todo.progress = progress
        todo.start_date = start_date
        todo.due_date = due_date
        todo.labels = labels
        session.commit()


def _date_value(value: date | None) -> str | None:
    return value.isoformat() if value else None


def _public_upload_path(filename: str) -> str:
    return f"/todo-uploads/{filename}"


def render_todo_dialog(todo_list_id: int, on_saved):
    title_input = description_input = link_input = start_date_input = due_date_input = labels_select = None
    priority_select = status_select = progress_slider = None
    dialog_title = progress_percent_label = attachment_label = clear_attachment_button = upload_input = None
    open_attachment_link = download_attachment_link = None
    save_button = None
    editing_todo_id: int | None = None
    attachment_path = ""
    attachment_name = ""
    upload_in_progress = False

    def update_progress_display(value: int | float | str | None) -> None:
        progress_percent_label.set_text(f"{int(float(value or 0))}%")

    def update_attachment_display() -> None:
        if attachment_name:
            attachment_label.set_text(f"Uploaded document: {attachment_name}")
            clear_attachment_button.set_visibility(True)
            open_attachment_link._props["href"] = attachment_path
            download_attachment_link._props["href"] = attachment_path
            download_attachment_link._props["download"] = attachment_name
            open_attachment_link.set_visibility(True)
            download_attachment_link.set_visibility(True)
        else:
            attachment_label.set_text("No document uploaded")
            clear_attachment_button.set_visibility(False)
            open_attachment_link._props["href"] = "#"
            download_attachment_link._props["href"] = "#"
            download_attachment_link._props.pop("download", None)
            open_attachment_link.set_visibility(False)
            download_attachment_link.set_visibility(False)

        open_attachment_link.update()
        download_attachment_link.update()

    def clear_attachment() -> None:
        nonlocal attachment_path, attachment_name
        attachment_path = ""
        attachment_name = ""
        upload_input.reset()
        update_attachment_display()

    def begin_upload() -> None:
        nonlocal upload_in_progress
        upload_in_progress = True
        attachment_label.set_text("Uploading document...")
        clear_attachment_button.set_visibility(False)
        save_button.disable()

    async def handle_upload(event) -> None:
        nonlocal attachment_path, attachment_name, upload_in_progress

        file_extension = Path(event.file.name).suffix.lower()
        if file_extension not in {".jpg", ".jpeg", ".pdf"}:
            ui.notify("Bitte lade nur JPG- oder PDF-Dateien hoch.", color="warning")
            upload_in_progress = False
            save_button.enable()
            update_attachment_display()
            return

        saved_filename = f"{uuid4().hex}{file_extension}"
        saved_path = UPLOAD_DIR / saved_filename
        try:
            await event.file.save(saved_path)
        except Exception:
            upload_in_progress = False
            save_button.enable()
            update_attachment_display()
            ui.notify("Dokument konnte nicht gespeichert werden.", color="negative")
            raise

        attachment_path = _public_upload_path(saved_filename)
        attachment_name = event.file.name
        upload_in_progress = False
        save_button.enable()
        update_attachment_display()
        ui.notify("Dokument hochgeladen.", color="positive")

    def default_label() -> str:
        label_filter = get_label_filter()
        if label_filter in {"arbeit", "private"}:
            return label_filter
        return "arbeit"

    def reset_form() -> None:
        nonlocal editing_todo_id, attachment_path, attachment_name, upload_in_progress
        editing_todo_id = None
        attachment_path = ""
        attachment_name = ""
        upload_in_progress = False
        title_input.value = ""
        description_input.value = ""
        link_input.value = ""
        priority_select.value = "low"
        status_select.value = Status.BACKLOG.value
        progress_slider.value = 0
        progress_slider.disable()
        update_progress_display(0)
        start_date_input.value = None
        due_date_input.value = date.today().isoformat()
        labels_select.value = default_label()
        upload_input.reset()
        save_button.enable()
        update_attachment_display()

    def fill_form(todo: Todo) -> None:
        nonlocal editing_todo_id, attachment_path, attachment_name
        editing_todo_id = todo.id
        attachment_path = todo.attachment_path or ""
        attachment_name = todo.attachment_name or ""
        title_input.value = todo.title
        description_input.value = todo.description
        link_input.value = todo.link
        priority_select.value = todo.priority.value
        status_select.value = todo.status.value
        progress_slider.value = todo.progress
        progress_slider.enable()
        update_progress_display(todo.progress)
        start_date_input.value = _date_value(todo.start_date)
        due_date_input.value = _date_value(todo.due_date)
        labels_select.value = todo.labels or default_label()
        update_attachment_display()

    def save_todo() -> None:
        title = (title_input.value or "").strip()
        description = (description_input.value or "").strip()
        link = (link_input.value or "").strip()
        start_date = parse_due_date(start_date_input.value)
        due_date = parse_due_date(due_date_input.value)
        priority = priority_select.value or "low"
        status = status_select.value or Status.BACKLOG.value
        progress = 0 if editing_todo_id is None else int(progress_slider.value or 0)
        labels = labels_select.value or ""

        if upload_in_progress:
            ui.notify("Bitte warte, bis das Dokument fertig hochgeladen ist.", color="warning")
            return

        if not title:
            ui.notify("Bitte gib einen Todo-Titel ein.", color="warning")
            return

        if editing_todo_id is None:
            create_todo(
                todo_list_id=todo_list_id,
                title=title,
                description=description,
                link=link,
                attachment_path=attachment_path,
                attachment_name=attachment_name,
                priority=priority,
                status=status,
                progress=progress,
                start_date=start_date,
                due_date=due_date,
                labels=labels,
            )
            ui.notify("Todo erstellt.", color="positive")
        else:
            update_todo_details(
                todo_id=editing_todo_id,
                title=title,
                description=description,
                link=link,
                attachment_path=attachment_path,
                attachment_name=attachment_name,
                priority=priority,
                status=status,
                progress=progress,
                start_date=start_date,
                due_date=due_date,
                labels=labels,
            )
            ui.notify("Todo gespeichert.", color="positive")

        dialog.close()
        reset_form()
        on_saved()

    def open_create_dialog() -> None:
        reset_form()
        dialog_title.set_text("Neue Todo erfassen")
        dialog.open()

    def open_edit_dialog(todo: Todo) -> None:
        fill_form(todo)
        dialog_title.set_text("Todo bearbeiten")
        dialog.open()

    with ui.dialog() as dialog, ui.card().classes("w-full max-w-2xl p-6"):
        dialog_title = ui.label("Neue Todo erfassen").classes("text-2xl font-bold")

        with ui.grid(columns=2).classes("w-full gap-4"):
            title_input = ui.input("Title").props("outlined").classes("w-full")
            with ui.grid(columns=2).classes("w-full col-span-2 gap-4"):
                description_input = ui.textarea("Description").props("outlined").classes("w-full")
                with ui.column().classes("w-full gap-2"):
                    ui.label("Document").classes("text-sm font-medium text-gray-700")
                    upload_input = ui.upload(
                        label="Upload JPG or PDF",
                        auto_upload=True,
                        on_begin_upload=begin_upload,
                        on_upload=handle_upload,
                    ).props("accept=.jpg,.jpeg,.pdf").classes("w-full")
                    with ui.row().classes("w-full items-center justify-between"):
                        attachment_label = ui.label("No document uploaded").classes("text-sm text-gray-600")
                    with ui.row().classes("w-full items-center gap-2"):
                        open_attachment_link = ui.link("Open", "#", new_tab=True).classes("text-sm")
                        download_attachment_link = ui.link("Download", "#").classes("text-sm")
                        clear_attachment_button = ui.button(
                            "Remove",
                            icon="delete",
                            on_click=clear_attachment,
                        ).props("flat dense color=negative")
                        open_attachment_link.set_visibility(False)
                        download_attachment_link.set_visibility(False)
                        clear_attachment_button.set_visibility(False)
            link_input = ui.input("Links", placeholder="https://example.com").props("outlined").classes(
                "w-full col-span-2"
            )
            priority_select = ui.select(PRIORITY_OPTIONS, label="Priority", value="low").props("outlined").classes(
                "w-full"
            )
            status_select = ui.select(STATUS_OPTIONS, label="Status", value=Status.BACKLOG.value).props(
                "outlined"
            ).classes("w-full")
            with ui.column().classes("w-full col-span-2 gap-1"):
                with ui.row().classes("w-full items-center justify-between"):
                    ui.label("Progress").classes("text-sm font-medium text-gray-700")
                    progress_percent_label = ui.label("0%").classes("text-sm font-bold text-gray-700")
                progress_slider = ui.slider(min=0, max=100, value=0).props("label-always").classes("w-full")
                progress_slider.on_value_change(lambda event: update_progress_display(event.value))
                progress_slider.disable()
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
            save_button = ui.button("Speichern", icon="save", on_click=save_todo).classes("bg-yellow-400 text-black")

    ui.button("Neue Todo erfassen", icon="add", on_click=open_create_dialog).classes("bg-yellow-400 text-black")
    return open_edit_dialog


def render_todo_board(todo_list_id: int) -> None:
    def refresh_board() -> None:
        board.refresh()

    def remove_todo(todo: Todo) -> None:
        if todo.id is None:
            return

        if delete_todo(todo.id):
            ui.notify("Todo gelöscht.", color="positive")
        else:
            ui.notify("Todo konnte nicht gelöscht werden.", color="warning")
        board.refresh()

    def handle_drop(todo: Todo, column_name: str) -> None:
        status = next(statuses[0] for name, statuses in COLUMNS if name == column_name)
        if todo.id is not None:
            update_todo_status(todo.id, status)
        board.refresh()

    open_edit_dialog = None

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
                        with dnd.card(todo):
                            ui.button(
                                icon="edit",
                                on_click=lambda todo=todo: open_edit_dialog(todo),
                            ).props("flat round dense").tooltip("Todo bearbeiten")
                            ui.button(
                                icon="delete",
                                on_click=lambda todo=todo: remove_todo(todo),
                            ).props("flat round dense color=negative").tooltip("Todo löschen")

    open_edit_dialog = render_todo_dialog(todo_list_id, refresh_board)
    board()
