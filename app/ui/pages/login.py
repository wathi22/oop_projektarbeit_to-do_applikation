from pathlib import Path

from nicegui import app, ui
from sqlmodel import Session

from app.database.database import engine
from app.services.UserHandler import UserHandler


LOGIN_ASSETS_PATH = Path(__file__).parent
LOGIN_BACKGROUND_IMAGE = "Hintergrundbild_Todo_Manager.jpg"
LOGIN_BACKGROUND_IMAGE_URL = f"/login-assets/{LOGIN_BACKGROUND_IMAGE}"

app.add_static_files("/login-assets", LOGIN_ASSETS_PATH)


def render_login_background() -> None:
    ui.add_head_html(
        """
        <style>
            .login-page {
                min-height: 100vh;
                overflow: hidden;
                position: relative;
            }

            .login-background-image {
                background-image: url('/login-assets/Hintergrundbild_Todo_Manager.jpg');
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover;
                inset: 0;
                position: fixed;
                z-index: 0;
            }

            .login-background-overlay {
                background: rgba(0, 0, 0, 0.55);
                inset: 0;
                position: fixed;
                z-index: 1;
            }

            .login-content {
                inset: 0;
                position: fixed;
                z-index: 2;
            }

            .login-card {
                backdrop-filter: blur(10px);
                background: rgba(255, 255, 255, 0.92);
                box-shadow: 0 18px 60px rgba(0, 0, 0, 0.35);
            }
        </style>
        """
    )

    ui.html(
        f"""
        <div
            class="login-background-image"
            style="background-image: url('{LOGIN_BACKGROUND_IMAGE_URL}');"
            aria-hidden="true"
        ></div>
        <div class="login-background-overlay" aria-hidden="true"></div>
        """
    )


@ui.page("/login")
def login_page():
    def do_login():
        error_label.set_visibility(False)

        email = (email_input.value or "").strip()
        password = password_input.value or ""

        if not email or not password:
            error_label.set_text("Bitte E-Mail und Passwort eingeben.")
            error_label.set_visibility(True)
            return

        with Session(engine) as session:
            user = UserHandler(session).get_by_email(email)

        if user and user.check_password(password):
            app.storage.user["user_id"] = user.id
            app.storage.user["user_name"] = user.full_name()
            ui.navigate.to("/todos")
            return

        error_label.set_text("Ungültige E-Mail oder Passwort.")
        error_label.set_visibility(True)

    render_login_background()

    with ui.element("main").classes("login-page"):
        with ui.column().classes("login-content w-full h-screen items-center justify-center"):
            ui.label("ToDoList").classes("text-3xl font-bold text-white drop-shadow")
            with ui.card().classes("login-card w-96 p-6"):
                email_input = ui.input("E-Mail", placeholder="name@beispiel.ch").props("outlined").classes("w-full")
                password_input = ui.input(
                    "Passwort", placeholder="Passwort", password=True
                ).props("outlined").classes("w-full")
                password_input.on("keydown.enter", lambda event: do_login())
                error_label = ui.label("").classes("text-negative mb-4")
                error_label.set_visibility(False)
                ui.button("Einloggen", on_click=do_login).classes("w-full bg-yellow-400 text-black")
                ui.link("Registrieren", "/register")


@ui.page("/register")
def register_page():
    render_login_background()

    with ui.element("main").classes("login-page"):
        with ui.column().classes("login-content w-full h-screen items-center justify-center"):
            ui.label("Registrierung").classes("text-3xl font-bold text-white drop-shadow")
            with ui.card().classes("login-card w-96 p-6 flex flex-col gap-4"):
                ui.input("Vorname").props("id=reg-firstname placeholder=Max outlined").classes("w-full")
                ui.input("Nachname").props("id=reg-lastname placeholder=Muster outlined").classes("w-full")
                ui.input("E-Mail").props("id=reg-email placeholder=name@beispiel.ch outlined").classes("w-full")
                ui.input(
                    "Passwort",
                ).props("id=reg-password type=password placeholder='Mindestens 8 Zeichen' outlined").classes("w-full")
                ui.input("Passwort wiederholen").props(
                    "id=reg-password2 type=password placeholder='Passwort bestätigen' outlined"
                ).classes("w-full")
                ui.label("").props("id=reg-error").classes("text-negative").style("display:none")
                ui.link("Einloggen", "/login").classes("mt-4")
