from nicegui import ui

ui.label('Unsere To-Do Applikation')

ui.button("Klick mich", on_click=lambda: ui.notify('Test'))

ui.run()