from calendar import monthrange
from datetime import date, timedelta

from nicegui import ui

from app.models.todo import Status, Todo
from app.ui.layout import create_app_layout, get_or_create_default_todo_list, require_login
from app.ui.pages.todo_board import load_todos, render_create_todo_dialog, update_todo_status


def _month_days(month: date) -> list[date | None]:
    first_day = month.replace(day=1)
    days_in_month = monthrange(first_day.year, first_day.month)[1]
    leading_empty_days = first_day.weekday()

    days: list[date | None] = [None] * leading_empty_days
    days.extend(first_day + timedelta(days=day_offset) for day_offset in range(days_in_month))

    while len(days) % 7 != 0:
        days.append(None)

    return days


def _status_color(status: Status) -> str:
    if status == Status.DONE:
        return "positive"
    if status == Status.IN_PROGRESS:
        return "warning"
    return "grey"


def render_calendar_view(todo_list_id: int) -> None:
    current_month = date.today().replace(day=1)

    def change_month(month_delta: int) -> None:
        nonlocal current_month

        year = current_month.year + (current_month.month + month_delta - 1) // 12
        month = (current_month.month + month_delta - 1) % 12 + 1
        current_month = date(year, month, 1)
        calendar.refresh()

    def mark_done(todo: Todo) -> None:
        if todo.id is None:
            return

        update_todo_status(todo.id, Status.DONE)
        calendar.refresh()

    @ui.refreshable
    def calendar() -> None:
        todos = load_todos(todo_list_id)
        todos_with_date = [todo for todo in todos if todo.due_date is not None]
        todos_without_date = [todo for todo in todos if todo.due_date is None]

        with ui.row().classes("w-full max-w-5xl items-center"):
            ui.button(icon="chevron_left", on_click=lambda: change_month(-1)).props("flat round")
            ui.label(current_month.strftime("%B %Y")).classes("text-xl font-bold")
            ui.button(icon="chevron_right", on_click=lambda: change_month(1)).props("flat round")

        with ui.grid(columns=7).classes("w-full max-w-5xl gap-2"):
            for weekday in ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]:
                ui.label(weekday).classes("text-center text-sm font-bold text-gray-500")

            for day in _month_days(current_month):
                with ui.card().classes("min-h-32 p-2"):
                    if day is None:
                        ui.label("")
                        continue

                    day_classes = "text-sm font-bold"
                    if day == date.today():
                        day_classes += " text-yellow-700"
                    ui.label(str(day.day)).classes(day_classes)

                    day_todos = [todo for todo in todos_with_date if todo.due_date == day]
                    if not day_todos:
                        ui.label("Keine Todos").classes("text-xs text-gray-400")

                    for todo in day_todos:
                        with ui.row().classes("w-full items-center gap-1"):
                            title_classes = "text-xs grow"
                            if todo.status == Status.DONE:
                                title_classes += " line-through text-gray-400"
                            ui.label(todo.title).classes(title_classes)
                            ui.badge(todo.status.value).props(f"color={_status_color(todo.status)}")
                            if todo.priority:
                                ui.badge(todo.priority.value).props("color=grey")
                            if todo.status != Status.DONE:
                                ui.button(icon="check", on_click=lambda todo=todo: mark_done(todo)).props(
                                    "flat round dense"
                                ).tooltip("Als erledigt markieren")

        if todos_without_date:
            ui.label("Ohne Erledigungsdatum").classes("text-lg font-bold mt-4")
            with ui.list().props("bordered separator").classes("w-full max-w-5xl bg-white"):
                for todo in todos_without_date:
                    with ui.item():
                        with ui.item_section():
                            ui.item_label(todo.title)
                            ui.item_label(f"ID {todo.id} | {todo.status.value} | Fortschritt {todo.progress}%").props(
                                "caption"
                            )

    render_create_todo_dialog(todo_list_id, calendar.refresh)
    calendar()


@ui.page("/calendar")
def calendar_page():
    user_id = require_login()
    if not user_id:
        return

    create_app_layout("Kalender", "/calendar")
    todo_list_id = get_or_create_default_todo_list(user_id)

    with ui.column().classes("w-full p-6 gap-4"):
        ui.label("Todo-Kalender").classes("text-3xl font-bold")
        ui.label("Todos werden anhand ihres Erledigungsdatums angezeigt.").classes("text-gray-600")
        render_calendar_view(todo_list_id)
