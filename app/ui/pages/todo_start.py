from nicegui import ui

from app.ui.layout import create_app_layout, get_or_create_default_todo_list, require_login
from app.ui.pages.todo_board import render_todo_board


@ui.page("/todos")
def todos_page():
    user_id = require_login()
    if not user_id:
        return

    create_app_layout("Todos", "/todos")
    todo_list_id = get_or_create_default_todo_list(user_id)

    with ui.column().classes("w-full p-6 gap-4 items-center"):
        with ui.column().classes("w-full max-w-6xl gap-1"):
            ui.label("Willkommen auf deiner Todo-Seite!").classes("text-3xl font-bold")
            ui.label("Todos sind in Backlog, To-Do, In Progress und Done unterteilt.").classes("text-gray-600")
        render_todo_board(todo_list_id)
