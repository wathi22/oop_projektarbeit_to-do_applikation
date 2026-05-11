from nicegui import ui

from app.models.todo import Status, Todo
from app.ui.layout import create_app_layout, get_or_create_default_todo_list, require_login
from app.ui.pages.todo_board import COLUMNS, load_todos, render_todo_dialog, update_todo_status


def render_todo_list_view(todo_list_id: int) -> None:
    def refresh_list() -> None:
        todo_groups.refresh()

    def change_status(todo: Todo, status: Status) -> None:
        if todo.id is None:
            return

        update_todo_status(todo.id, status)
        todo_groups.refresh()

    open_edit_dialog = None

    @ui.refreshable
    def todo_groups() -> None:
        todos = load_todos(todo_list_id)

        with ui.column().classes("w-full max-w-4xl gap-4"):
            for group_name, statuses in COLUMNS:
                group_todos = [todo for todo in todos if todo.status in statuses]

                with ui.card().classes("w-full p-0"):
                    with ui.row().classes("w-full items-center px-4 py-3 bg-gray-100"):
                        ui.label(group_name).classes("text-lg font-bold")
                        ui.badge(str(len(group_todos))).props("color=grey")

                    if not group_todos:
                        ui.label("Keine Todos").classes("text-gray-500 px-4 py-3")
                        continue

                    with ui.list().props("separator").classes("w-full"):
                        for todo in group_todos:
                            with ui.item().classes("items-center"):
                                with ui.item_section():
                                    title_classes = "text-base"
                                    if todo.status == Status.DONE:
                                        title_classes += " line-through text-gray-400"
                                    ui.item_label(todo.title).classes(title_classes)
                                    caption = todo.status.value
                                    if todo.priority:
                                        caption += f" | Priorität {todo.priority.value}"
                                    caption += f" | Fortschritt {todo.progress}%"
                                    if todo.due_date:
                                        caption += f" | Erledigen bis {todo.due_date.strftime('%d.%m.%Y')}"
                                    if todo.labels:
                                        caption += f" | {todo.labels}"
                                    ui.item_label(caption).props("caption").classes("text-gray-500")

                                ui.badge(todo.status.value).props(
                                    "color=positive" if todo.status == Status.DONE else "color=grey"
                                )
                                ui.button(
                                    icon="edit",
                                    on_click=lambda todo=todo: open_edit_dialog(todo),
                                ).props("flat round dense").tooltip("Todo bearbeiten")
                                ui.button(
                                    icon="undo",
                                    on_click=lambda todo=todo: change_status(todo, Status.BACKLOG),
                                ).props("flat round dense").tooltip("Nach Backlog")
                                ui.button(
                                    icon="radio_button_unchecked",
                                    on_click=lambda todo=todo: change_status(todo, Status.TODO),
                                ).props("flat round dense").tooltip("Nach To-Do")
                                ui.button(
                                    icon="play_arrow",
                                    on_click=lambda todo=todo: change_status(todo, Status.IN_PROGRESS),
                                ).props("flat round dense").tooltip("Nach In Progress")
                                ui.button(
                                    icon="check",
                                    on_click=lambda todo=todo: change_status(todo, Status.DONE),
                                ).props("flat round dense").tooltip("Als erledigt markieren")

    open_edit_dialog = render_todo_dialog(todo_list_id, refresh_list)
    todo_groups()


@ui.page("/lists")
def lists_page():
    user_id = require_login()
    if not user_id:
        return

    create_app_layout("Listen", "/lists")
    todo_list_id = get_or_create_default_todo_list(user_id)

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("Todo-Listen").classes("text-3xl font-bold")
        ui.label("Deine Todos in der Listenansicht.").classes("text-gray-600")
        render_todo_list_view(todo_list_id)
