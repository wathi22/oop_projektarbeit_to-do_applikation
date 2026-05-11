from nicegui import ui
from sqlmodel import Session

from app.database.database import engine
from app.models.todo import Todo
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


@ui.page("/settings")
def settings_page():
    user_id = require_login()
    if not user_id:
        return

    create_app_layout("Einstellungen", "/settings")
    todo_list_id = get_or_create_default_todo_list(user_id)

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

    with ui.column().classes("w-full p-6 gap-4"):
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
            ui.label("Todos zurücksetzen").classes("text-xl font-bold")
            ui.label("Löscht alle Todos, die auf Todo-, Listen- und Kalenderseite angezeigt werden.").classes(
                "text-gray-600"
            )
            stats()
            ui.button("Alle Todos löschen", icon="delete", on_click=confirm_dialog.open).props("color=negative")
