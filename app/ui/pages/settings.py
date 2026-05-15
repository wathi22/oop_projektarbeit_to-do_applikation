import csv
from datetime import date, datetime
from io import StringIO

from nicegui import ui
from sqlmodel import Session

from app.database.database import engine
from app.models.todo import Priority, Status, Todo
from app.ui.layout import (
    THEMES,
    create_app_layout,
    get_or_create_default_todo_list,
    get_theme,
    get_theme_key,
    require_login,
    set_theme,
)
from app.ui.pages.todo_board import load_todos


CSV_COLUMNS = [
    "id",
    "title",
    "description",
    "link",
    "attachment_path",
    "attachment_name",
    "priority",
    "status",
    "progress",
    "start_date",
    "due_date",
    "labels",
    "created_at",
]

REQUIRED_IMPORT_COLUMNS = {"title", "priority", "status", "progress"}


def _parse_optional_date(value: str, field_name: str, row_number: int, errors: list[str]) -> date | None:
    if not value:
        return None

    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"Zeile {row_number}: {field_name} muss im Format YYYY-MM-DD sein.")
        return None


def _parse_optional_datetime(value: str, row_number: int, errors: list[str]) -> datetime | None:
    if not value:
        return None

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        errors.append(f"Zeile {row_number}: created_at ist kein gültiger ISO-Zeitstempel.")
        return None


def _parse_todos_csv(csv_text: str, todo_list_id: int) -> tuple[list[Todo], list[str]]:
    errors: list[str] = []

    try:
        reader = csv.DictReader(StringIO(csv_text), strict=True)
        fieldnames = set(reader.fieldnames or [])
        missing_columns = REQUIRED_IMPORT_COLUMNS - fieldnames
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            return [], [f"CSV kann nicht importiert werden. Fehlende Spalten: {missing}."]

        todos: list[Todo] = []
        for row_number, row in enumerate(reader, start=2):
            if not any((value or "").strip() for value in row.values()):
                continue

            title = (row.get("title") or "").strip()
            if not title:
                errors.append(f"Zeile {row_number}: title darf nicht leer sein.")

            try:
                priority = Priority((row.get("priority") or "").strip())
            except ValueError:
                allowed = ", ".join(priority.value for priority in Priority)
                errors.append(f"Zeile {row_number}: priority muss einer dieser Werte sein: {allowed}.")
                priority = Priority.LOW

            try:
                status = Status((row.get("status") or "").strip())
            except ValueError:
                allowed = ", ".join(status.value for status in Status)
                errors.append(f"Zeile {row_number}: status muss einer dieser Werte sein: {allowed}.")
                status = Status.BACKLOG

            try:
                progress = int((row.get("progress") or "0").strip())
                if not 0 <= progress <= 100:
                    raise ValueError
            except ValueError:
                errors.append(f"Zeile {row_number}: progress muss eine Zahl zwischen 0 und 100 sein.")
                progress = 0

            start_date = _parse_optional_date((row.get("start_date") or "").strip(), "start_date", row_number, errors)
            due_date = _parse_optional_date((row.get("due_date") or "").strip(), "due_date", row_number, errors)
            created_at = _parse_optional_datetime((row.get("created_at") or "").strip(), row_number, errors)

            todos.append(
                Todo(
                    title=title,
                    description=(row.get("description") or "").strip(),
                    link=(row.get("link") or "").strip(),
                    attachment_path=(row.get("attachment_path") or "").strip(),
                    attachment_name=(row.get("attachment_name") or "").strip(),
                    priority=priority,
                    status=status,
                    progress=progress,
                    start_date=start_date,
                    due_date=due_date,
                    labels=(row.get("labels") or "").strip(),
                    created_at=created_at or datetime.now(),
                    todo_list_id=todo_list_id,
                )
            )
    except csv.Error as error:
        return [], [f"CSV kann nicht gelesen werden: {error}."]

    if not todos and not errors:
        errors.append("CSV enthält keine Todos.")

    return todos, errors


@ui.page("/settings")
def settings_page():
    user_id = require_login()
    if not user_id:
        return

    create_app_layout("Einstellungen", "/settings")
    todo_list_id = get_or_create_default_todo_list(user_id)
    import_upload = None

    def change_theme(theme_key: str) -> None:
        set_theme(theme_key)
        ui.notify(f"Farblayout gewechselt: {THEMES[theme_key]['name']}", color="positive")
        ui.navigate.reload()

    def delete_all_todos() -> None:
        todos = load_todos(todo_list_id, apply_label_filter=False)

        with Session(engine) as session:
            for todo in todos:
                db_todo = session.get(Todo, todo.id)
                if db_todo:
                    session.delete(db_todo)
            session.commit()

        ui.notify("Alle Todos wurden gelöscht.", color="positive")
        stats.refresh()
        confirm_dialog.close()

    def export_todos_csv() -> None:
        todos = load_todos(todo_list_id, apply_label_filter=False)
        output = StringIO()
        writer = csv.writer(output)

        writer.writerow(
            CSV_COLUMNS
        )

        for todo in todos:
            writer.writerow(
                [
                    todo.id,
                    todo.title,
                    todo.description,
                    todo.link,
                    todo.attachment_path,
                    todo.attachment_name,
                    todo.priority.value,
                    todo.status.value,
                    todo.progress,
                    todo.start_date.isoformat() if todo.start_date else "",
                    todo.due_date.isoformat() if todo.due_date else "",
                    todo.labels,
                    todo.created_at.isoformat(timespec="seconds"),
                ]
            )

        ui.download(
            output.getvalue().encode("utf-8-sig"),
            filename="todos_export.csv",
            media_type="text/csv",
        )
        ui.notify("Todos wurden als CSV exportiert.", color="positive")

    def show_import_errors(errors: list[str]) -> None:
        with ui.dialog() as error_dialog, ui.card().classes("w-full max-w-2xl p-5"):
            ui.label("CSV konnte nicht importiert werden").classes("text-xl font-bold")
            ui.label("Bitte korrigiere die Datei und versuche den Import erneut.").classes("text-gray-600")
            with ui.list().props("bordered separator").classes("w-full max-h-96 overflow-auto"):
                for error in errors[:20]:
                    with ui.item():
                        ui.item_label(error)
                if len(errors) > 20:
                    with ui.item():
                        ui.item_label(f"... und {len(errors) - 20} weitere Fehler.")
            with ui.row().classes("w-full justify-end"):
                ui.button("Schliessen", on_click=error_dialog.close).props("flat")
        error_dialog.open()

    async def import_todos_csv(event) -> None:
        try:
            csv_text = await event.file.text()
        except UnicodeDecodeError:
            show_import_errors(["CSV kann nicht gelesen werden. Bitte speichere die Datei als UTF-8 CSV."])
            import_upload.reset()
            return

        todos, errors = _parse_todos_csv(csv_text, todo_list_id)
        if errors:
            show_import_errors(errors)
            import_upload.reset()
            return

        with Session(engine) as session:
            for todo in todos:
                session.add(todo)
            session.commit()

        ui.notify(f"{len(todos)} Todos wurden importiert.", color="positive")
        stats.refresh()
        import_upload.reset()

    @ui.refreshable
    def stats() -> None:
        todo_count = len(load_todos(todo_list_id, apply_label_filter=False))
        ui.label(f"Aktuell gespeicherte Todos: {todo_count}").classes("text-gray-600")

    with ui.dialog() as confirm_dialog, ui.card().classes("w-96"):
        ui.label("Alle Todos löschen?").classes("text-xl font-bold")
        ui.label("Diese Aktion entfernt alle Todos deiner aktuellen Liste und kann nicht rückgängig gemacht werden.")
        with ui.row().classes("w-full justify-end gap-2"):
            ui.button("Abbrechen", on_click=confirm_dialog.close).props("flat")
            ui.button("Löschen", icon="delete", on_click=delete_all_todos).props("color=negative")

    with ui.column().classes("w-full p-6 gap-4 items-center"):
        with ui.column().classes("w-full max-w-3xl gap-1"):
            ui.label("Einstellungen").classes("text-3xl font-bold")
            ui.label("App-Verhalten und Darstellung verwalten.").classes("text-gray-600")

        with ui.card().classes("w-full max-w-3xl p-5"):
            ui.label("Farblayout").classes("text-xl font-bold")
            ui.label("Wähle aus, wie die Navigation und die App-Flächen dargestellt werden.").classes("text-gray-600")
            ui.toggle(
                {theme_key: theme["name"] for theme_key, theme in THEMES.items()},
                value=get_theme_key(),
                on_change=lambda event: change_theme(event.value),
            ).props("unelevated").classes("mt-2")
            ui.label(f"Aktuell aktiv: {get_theme()['name']}").classes("text-sm text-gray-500")

        with ui.card().classes("w-full max-w-3xl p-5"):
            ui.label("Todos exportieren").classes("text-xl font-bold")
            ui.label("Lädt alle Todos deiner aktuellen Liste als CSV-Datei herunter.").classes("text-gray-600")
            ui.button("Todos als CSV exportieren", icon="download", on_click=export_todos_csv).classes(
                "bg-yellow-400 text-black"
            )

        with ui.card().classes("w-full max-w-3xl p-5"):
            ui.label("Todos importieren").classes("text-xl font-bold")
            ui.label(
                "Importiert eine CSV-Datei im gleichen Format wie der Export. IDs werden ignoriert und neue Todos erstellt."
            ).classes("text-gray-600")
            import_upload = ui.upload(
                label="CSV-Datei auswählen",
                auto_upload=True,
                on_upload=import_todos_csv,
            ).props("accept=.csv").classes("w-full mt-2")

        with ui.card().classes("w-full max-w-3xl p-5"):
            ui.label("Todos zurücksetzen").classes("text-xl font-bold")
            ui.label("Löscht alle Todos, die auf Todo-, Listen- und Kalenderseite angezeigt werden.").classes(
                "text-gray-600"
            )
            stats()
            ui.button("Alle Todos löschen", icon="delete", on_click=confirm_dialog.open).props("color=negative")
