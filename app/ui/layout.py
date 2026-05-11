from nicegui import app, ui
from sqlmodel import Session

from app.database.database import engine
from app.services.TodoListHandler import TodoListHandler


NAVIGATION_ITEMS = [
    {"label": "Todos", "icon": "checklist", "path": "/todos"},
    {"label": "Listen", "icon": "view_list", "path": "/lists"},
    {"label": "Kalender", "icon": "calendar_month", "path": "/calendar"},
    {"label": "Einstellungen", "icon": "settings", "path": "/settings"},
]


THEMES = {
    "dark": {
        "name": "Dunkel",
        "page": "bg-gray-50 text-gray-900",
        "header": "bg-white text-gray-900 border-b border-gray-200",
        "drawer": "bg-gray-900 text-white",
        "drawer_separator": "bg-gray-700",
        "active_button": "bg-yellow-400 text-black",
        "inactive_button": "text-white",
        "accent_button": "bg-yellow-400 text-black",
    },
    "light": {
        "name": "Hell",
        "page": "bg-slate-50 text-slate-900",
        "header": "bg-sky-700 text-white",
        "drawer": "bg-white text-slate-900",
        "drawer_separator": "bg-slate-200",
        "active_button": "bg-sky-100 text-sky-900",
        "inactive_button": "text-slate-700",
        "accent_button": "bg-sky-600 text-white",
    },
}


def get_theme_key() -> str:
    theme_key = app.storage.user.get("theme", "dark")
    if theme_key not in THEMES:
        return "dark"
    return theme_key


def get_theme() -> dict[str, str]:
    return THEMES[get_theme_key()]


def set_theme(theme_key: str) -> None:
    if theme_key in THEMES:
        app.storage.user["theme"] = theme_key


def get_current_user_id() -> int | None:
    return app.storage.user.get("user_id")


def require_login() -> int | None:
    user_id = get_current_user_id()
    if not user_id:
        ui.navigate.to("/login")
        return None
    return user_id


def get_or_create_default_todo_list(user_id: int) -> int:
    with Session(engine) as session:
        handler = TodoListHandler(session)
        todo_lists = handler.get_lists_for_user(user_id)

        if todo_lists:
            return todo_lists[0].id

        todo_list = handler.create_list(user_id, "Meine Todos")
        return todo_list.id


def logout() -> None:
    app.storage.user.clear()
    ui.navigate.to("/login")


def create_app_layout(title: str, active_path: str) -> None:
    user_name = app.storage.user.get("user_name") or "Benutzer"
    theme = get_theme()

    ui.query(".nicegui-content").classes(theme["page"])

    with ui.header(elevated=True).classes(theme["header"]):
        ui.button(icon="menu", on_click=lambda: drawer.toggle()).props("flat round dense")
        ui.label(title).classes("text-lg font-semibold")
        ui.space()
        ui.label(user_name).classes("text-sm")

    with ui.left_drawer(value=True).props("width=260 bordered").classes(theme["drawer"]) as drawer:
        with ui.column().classes("w-full h-full p-4 gap-2"):
            ui.label("ToDoList").classes("text-2xl font-bold mb-4")

            for item in NAVIGATION_ITEMS:
                is_active = item["path"] == active_path
                button_color = theme["active_button"] if is_active else theme["inactive_button"]

                ui.button(
                    item["label"],
                    icon=item["icon"],
                    on_click=lambda path=item["path"]: ui.navigate.to(path),
                ).props("flat align=left").classes(f"w-full justify-start text-left {button_color}")

            ui.space()
            ui.separator().classes(theme["drawer_separator"])
            ui.button("Abmelden", icon="logout", on_click=logout).props("flat align=left").classes(
                f"w-full justify-start {theme['inactive_button']}"
            )
