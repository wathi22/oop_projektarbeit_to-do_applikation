#dummy-files_for_ui

from nicegui import ui
from app.services.TodoListHandler import TodoListHandler
from app.models.models import Todo

def todo_page():
    handler = TodoListHandler()

    with ui.column().classes("items-center gap-4"):
        ui.label("To-Do List").classes("text-2xl font-bold")
        with ui.row().classes("gap-2"):
            description_input = ui.input("Description").classes("w-full")
            priority_input = ui.select(["Low", "Medium", "High"], label="Priority").classes("w-full")
            due_date_input = ui.input("Due Date (YYYY-MM-DD)").classes("w-full")
            add_button = ui.button("Add").classes("w-full")

        todo_list_container = ui.column().classes("w-full gap-2")

    def refresh_todo_list():
        todo_list_container.clear()
        todos = handler.get_all()
        for todo in todos:
            with todo_list_container:
                with ui.row().classes("gap-2 items-center"):
                    ui.label(todo.description).classes("flex-1")
                    ui.label(todo.priority).classes("w-24 text-center")
                    ui.label(todo.due_date).classes("w-32 text-center")
                    delete_button = ui.button("Delete").classes("w-20")
                    delete_button.on_click(lambda id=todo.id: delete_todo(id))

    def add_todo():
        description = description_input.value
        priority = priority_input.value
        due_date = due_date_input.value
        if description and priority and due_date:
            new_todo = Todo(description=description, priority=priority, due_date=due_date)
            handler.save(new_todo)
            refresh_todo_list()
            description_input.value = ""
            priority_input.value = None
            due_date_input.value = ""

    def delete_todo(todo_id: int):
        handler.delete(todo_id)
        refresh_todo_list()

    add_button.on_click(add_todo)
    refresh_todo_list()