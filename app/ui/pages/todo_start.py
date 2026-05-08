from dataclasses import dataclass

from nicegui import ui

import app.ui.draganddrop as dnd

@dataclass
class ToDo:
    title: str


def handle_drop(todo: ToDo, location: str) -> None:
    ui.notify(f'"{todo.title}" is now in {location}')


@ui.page("/dnd-demo")
def draganddrop_demo_page() -> None:
    with ui.row():
        with dnd.column("Next", on_drop=handle_drop):
            dnd.card(ToDo("Simplify Layouting"))
            dnd.card(ToDo("Provide Deployment"))
        with dnd.column("Doing", on_drop=handle_drop):
            dnd.card(ToDo("Improve Documentation"))
        with dnd.column("Done", on_drop=handle_drop):
            dnd.card(ToDo("Invent NiceGUI"))
            dnd.card(ToDo("Test in own Projects"))
            dnd.card(ToDo("Publish as Open Source"))
            dnd.card(ToDo("Release Native-Mode"))
