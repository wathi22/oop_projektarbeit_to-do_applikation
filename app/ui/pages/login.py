from nicegui import ui, app
from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from app.database.database import engine
from app.services.UserHandler import UserHandler
from app.services.TodoListHandler import TodoListHandler
from app.services.TodoHandler import TodoHandler
from app.models.user import User
from app.models.todo import Todo
from dataclasses import dataclass
from app.ui.session import _get_user_id, _create_session, _destroy_session
from app.ui.ui import TodoBoardPage
import app.ui.draganddrop as dnd

def _redirect_to_login():
    ui.open('/login')

@ui.page('/')
def index_page():
    if app.storage.user.get('user_id'):
        ui.navigate.to('/todos')
    else:
        ui.navigate.to('/login')


@ui.page("/login")
def login_page():
    ui.query(".nicegui-content").classes(
        "w-full h-screen flex items-center justify-center bg-gray-50"
    )

    with ui.card().classes("w-96 p-8"):
        ui.label("ToDoList Login").classes("text-2xl font-bold mb-4")

        email_input = ui.input("E-Mail").props("outlined").classes("w-full")
        password_input = ui.input("Passwort", password=True).props("outlined").classes("w-full")

        def login():
            print("LOGIN BUTTON WURDE GEKLICKT")

            email = (email_input.value or "").strip()
            password = password_input.value or ""

            print("E-Mail:", email)

            if not email or not password:
                ui.notify("Bitte E-Mail und Passwort eingeben.", color="negative")
                return

            with Session(engine) as session:
                user = UserHandler(session).get_by_email(email)

            if not user:
                ui.notify("User nicht gefunden.", color="negative")
                return

            if not user.check_password(password):
                ui.notify("Passwort falsch.", color="negative")
                return

            app.storage.user["user_id"] = user.id
            app.storage.user["user_name"] = user.full_name()

            ui.notify("Login erfolgreich.", color="positive")
            ui.navigate.to("/todos")

        ui.button("Einloggen", on_click=login).classes(
            "w-full bg-yellow-400 text-black font-bold mt-4"
        )

    def do_login():
        error_label.set_visibility(False)            
        if not email_input.value.strip() or not password_input.value:
            error_label.set_text('Bitte E-Mail und Passwort eingeben.')
            error_label.set_visibility(True)
            return
        with Session(engine) as session:
            user = UserHandler(session).get_by_email(email_input.value.strip())
            if user and user.check_password(password_input.value):
                app.storage.user['user_id'] = user.id  # Speichere user_id in NiceGUI's globalem Storage
                ui.navigate.to('/todos')
            else:
                error_label.set_text('Ungültige E-Mail oder Passwort.')
                error_label.set_visibility(True)
                

    with ui.column().classes('absolute-center items-center'):
        ui.label('ToDoList').classes('text-2xl font-bold')
        with ui.card().classes('w-96 p-6'):
            email_input = ui.input('E-Mail', placeholder='name@beispiel.ch')
            password_input = ui.input('Passwort', placeholder='Passwort',).props('type=password') 
            error_label = ui.label('').classes('text-negative')
            error_label.set_visibility(False)
            ui.button ('Einloggen', on_click=do_login).classes('w-full bg-yellow-400 text-black')
            ui.link('Registrieren', '/register')
   