from dataclasses import dataclass

from nicegui import ui

import app.ui.draganddrop as dnd

with ui.header().classes(replace='row items-center') as header:
    ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
    with ui.tabs() as tabs:
        ui.tab('A')
        ui.tab('B')
        ui.tab('C')

with ui.left_drawer().classes('bg-blue-100') as left_drawer:
    ui.label('Side menu')

with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

with ui.tab_panels(tabs, value='A').classes('w-full'):
    with ui.tab_panel('A'):
        ui.label('Content of A')
    with ui.tab_panel('B'):
        ui.label('Content of B')
    with ui.tab_panel('C'):
        ui.label('Content of C')

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
