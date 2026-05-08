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
import app.ui.draganddrop as dnd


# ─── NiceGUI Pages ────────────────────────────────────────────────────────────
def _redirect_to_login():
    ui.open('/login')


@ui.page('/')
def index_page():
    if app.storage.user.get('user_id'):
        ui.navigate.to('/todos')
    else:
        ui.navigate.to('/login')


@ui.page('/login')
def login_page():
    def do_login():
        error_label.set_visibility(False)
        if not email_input.value.strip() or not password_input.value:
            error_label.set_text('Bitte E-Mail und Passwort eingeben.')
            error_label.set_visibility(True)
            return

        with Session(engine) as session:
            user = UserHandler(session).get_by_email(email_input.value.strip())

        if user and user.check_password(password_input.value):
            app.storage.user['user_id'] = user.id
            app.storage.user['user_name'] = user.full_name()
            ui.navigate.to('/todos')
            return

        error_label.set_text('Ungültige E-Mail oder Passwort.')
        error_label.set_visibility(True)

    with ui.column().classes('absolute-center items-center'):
        ui.label('ToDoList').classes('text-2xl font-bold')
        with ui.card().classes('w-96 p-6'):
            email_input = ui.input('E-Mail', placeholder='name@beispiel.ch').props('outlined').classes('w-full')
            password_input = ui.input('Passwort', placeholder='Passwort').props('type=password').props('outlined').classes('w-full')
            password_input.on('keydown.enter', lambda e: do_login())
            error_label = ui.label('').classes('text-negative' + 'mb-4').style('display:none')
            error_label.set_visibility(False)
            ui.button('Einloggen', on_click=do_login).classes('w-full bg-yellow-400 text-black')
            ui.link('Registrieren', '/register')

@ui.page('/register')
def register_page():
        with ui.column().classes('absolute-center items-center justify-center h-screen'):
                ui.label('Registrierung').classes('text-2xl font-bold')
                with ui.card().classes('w-96 p-6 flex flex-col gap-4'):
                        ui.input('Vorname').props('id=reg-firstname placeholder=Max' + ' outlined').classes('w-full')
                        ui.input('Nachname').props('id=reg-lastname placeholder=Muster' + ' outlined').classes('w-full')
                        ui.input('E-Mail').props('id=reg-email placeholder=name@beispiel.ch' + ' outlined').classes('w-full')
                        ui.input('Passwort').props('id=reg-password type=password placeholder=Mindestens 8 Zeichen' + ' outlined').classes('w-full')
                        ui.input('Passwort wiederholen').props('id=reg-password2 type=password placeholder=Passwort bestätigen' + ' outlined').classes('w-full')
                        ui.label('').props('id=reg-error').classes('text-negative').style('display:none')   
                        ui.link('Einloggen', '/login' ).classes('mt-4')
