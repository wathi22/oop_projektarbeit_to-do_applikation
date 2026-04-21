import uuid
import json
from datetime import date

from fastapi import Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from nicegui import app
from sqlmodel import Session

from app.database.database import engine
from app.services.UserHandler import UserHandler
from app.services.TodoListHandler import TodoListHandler
from app.services.TodoHandler import TodoHandler
from app.models.user import User
from app.models.todo import Todo

from app.ui.styles import HEAD_HTML
from app.ui.templates import (
    LOGIN_HTML, LOGIN_JS,
    REGISTER_HTML, REGISTER_JS,
    TODO_APP_HTML, TODO_APP_JS,
)


# ─── Session store ─────────────────────────────────────────────────────────────

_sessions: dict[str, int] = {}


def _get_user_id(request: Request) -> int | None:
    token = request.cookies.get("tf_session")
    return _sessions.get(token) if token else None


def _create_session(response: Response, user_id: int) -> None:
    token = str(uuid.uuid4())
    _sessions[token] = user_id
    response.set_cookie("tf_session", token, httponly=True, samesite="lax", max_age=86400 * 7)


def _destroy_session(request: Request, response: Response) -> None:
    token = request.cookies.get("tf_session")
    if token:
        _sessions.pop(token, None)
    response.delete_cookie("tf_session")


# ─── HTML page builder ─────────────────────────────────────────────────────────

def _auth_page(title: str, body_html: str, body_js: str) -> str:
    parts = [
        '<!DOCTYPE html><html lang="de"><head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f'<title>{title}</title>',
        HEAD_HTML,
        '<style>html,body{margin:0;padding:0;min-height:100%;background:var(--bg)}</style>',
        '</head><body>',
        body_html,
        '<script>', body_js, '</script>',
        '</body></html>',
    ]
    return ''.join(parts)


def _todos_page(user_name: str, lists_json: str, todos_json: str) -> str:
    parts = [
        '<!DOCTYPE html><html lang="de"><head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<title>TaskFlow</title>',
        HEAD_HTML,
        '<style>html,body{height:100%;overflow:hidden;margin:0;padding:0;background:var(--bg)}</style>',
        '</head><body style="margin:0;padding:0">',
        TODO_APP_HTML,
        '<script>',
        f'window.__USER__ = {json.dumps(user_name)};',
        f'window.__LISTS__ = {lists_json};',
        f'window.__TODOS__ = {todos_json};',
        TODO_APP_JS,
        '</script>',
        '</body></html>',
    ]
    return ''.join(parts)


# ─── Data helpers ───────────────────────────────────────────────────────────────

def _todo_to_js(todo: Todo) -> dict:
    return {
        "id": todo.id,
        "title": todo.title,
        "desc": todo.description or "",
        "bucket": todo.status,
        "priority": todo.priority,
        "progress": todo.progress,
        "startDate": todo.start_date.isoformat() if todo.start_date else "",
        "dueDate": todo.due_date.isoformat() if todo.due_date else "",
        "labels": [l.strip() for l in (todo.labels or "").split(",") if l.strip()],
        "assignees": [],
        "listId": todo.todo_list_id,
    }


def _apply_js_data(todo: Todo, data: dict) -> None:
    todo.title = data.get("title", "") or "Aufgabe"
    todo.description = data.get("desc", "")
    todo.status = data.get("bucket", "Backlog")
    todo.priority = data.get("priority", "medium")
    todo.progress = int(data.get("progress", 0))
    todo.labels = ",".join(data.get("labels", []))
    start = data.get("startDate")
    todo.start_date = date.fromisoformat(start) if start else None
    due = data.get("dueDate")
    todo.due_date = date.fromisoformat(due) if due else None


# ─── Pydantic models ────────────────────────────────────────────────────────────

class LoginData(BaseModel):
    email: str
    password: str


class RegisterData(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str


class ListData(BaseModel):
    name: str


class TodoData(BaseModel):
    title: str = ""
    desc: str = ""
    bucket: str = "Backlog"
    priority: str = "medium"
    progress: int = 0
    startDate: str = ""
    dueDate: str = ""
    labels: list[str] = []
    assignees: list[str] = []
    listId: int | None = None


# ─── Page routes ────────────────────────────────────────────────────────────────

@app.get("/")
async def route_index(request: Request):
    return RedirectResponse("/login")


@app.get("/login")
async def route_login(request: Request):
    if _get_user_id(request):
        return RedirectResponse("/todos")
    return HTMLResponse(_auth_page("TaskFlow — Login", LOGIN_HTML, LOGIN_JS))


@app.get("/register")
async def route_register(request: Request):
    if _get_user_id(request):
        return RedirectResponse("/todos")
    return HTMLResponse(_auth_page("TaskFlow — Registrieren", REGISTER_HTML, REGISTER_JS))


@app.get("/todos")
async def route_todos(request: Request):
    user_id = _get_user_id(request)
    if not user_id:
        return RedirectResponse("/login")

    with Session(engine) as session:
        lists = TodoListHandler(session).get_lists_for_user(user_id)
        user = UserHandler(session).get_by_id(user_id)
        all_todos: list[Todo] = []
        for lst in lists:
            all_todos.extend(TodoHandler(session).get_todos_for_list(lst.id))

    user_name = user.full_name() if user else "User"
    lists_json = json.dumps([{"id": l.id, "name": l.name} for l in lists])
    todos_json = json.dumps([_todo_to_js(t) for t in all_todos])

    return HTMLResponse(_todos_page(user_name, lists_json, todos_json))


# ─── Auth API ───────────────────────────────────────────────────────────────────

@app.post("/api/auth/login")
async def api_login(data: LoginData, response: Response):
    with Session(engine) as session:
        user = UserHandler(session).get_by_email(data.email.strip())
    if not user or not user.check_password(data.password):
        return {"success": False, "error": "E-Mail oder Passwort falsch"}
    _create_session(response, user.id)
    return {"success": True}


@app.post("/api/auth/register")
async def api_register(data: RegisterData, response: Response):
    with Session(engine) as session:
        handler = UserHandler(session)
        if handler.get_by_email(data.email.strip()):
            return {"success": False, "error": "Diese E-Mail ist bereits registriert"}
        user = User(
            firstname=data.firstname.strip(),
            lastname=data.lastname.strip(),
            email=data.email.strip(),
            password_hash=User.hash_password(data.password),
        )
        handler.save(user)
        user_id = user.id
    _create_session(response, user_id)
    return {"success": True}


@app.post("/api/auth/logout")
async def api_logout(request: Request, response: Response):
    _destroy_session(request, response)
    return {"success": True}


# ─── Lists API ──────────────────────────────────────────────────────────────────

@app.get("/api/lists")
async def api_get_lists(request: Request):
    user_id = _get_user_id(request)
    if not user_id:
        return []
    with Session(engine) as session:
        lists = TodoListHandler(session).get_lists_for_user(user_id)
    return [{"id": l.id, "name": l.name} for l in lists]


@app.post("/api/lists")
async def api_create_list(data: ListData, request: Request):
    user_id = _get_user_id(request)
    if not user_id:
        return {"error": "Nicht autorisiert"}
    with Session(engine) as session:
        lst = TodoListHandler(session).create_list(user_id, data.name.strip())
        return {"id": lst.id, "name": lst.name}


@app.delete("/api/lists/{list_id}")
async def api_delete_list(list_id: int, request: Request):
    user_id = _get_user_id(request)
    if not user_id:
        return {"error": "Nicht autorisiert"}
    with Session(engine) as session:
        TodoListHandler(session).delete(list_id)
    return {"success": True}


# ─── Todos API ──────────────────────────────────────────────────────────────────

@app.get("/api/todos")
async def api_get_todos(request: Request, list_id: int | None = None):
    user_id = _get_user_id(request)
    if not user_id:
        return []
    with Session(engine) as session:
        handler = TodoHandler(session)
        if list_id:
            todos = handler.get_todos_for_list(list_id)
        else:
            lists = TodoListHandler(session).get_lists_for_user(user_id)
            todos = []
            for lst in lists:
                todos.extend(handler.get_todos_for_list(lst.id))
    return [_todo_to_js(t) for t in todos]


@app.post("/api/todos")
async def api_create_todo(data: TodoData, request: Request):
    user_id = _get_user_id(request)
    if not user_id:
        return {"error": "Nicht autorisiert"}
    list_id = data.listId
    if not list_id:
        with Session(engine) as session:
            lists = TodoListHandler(session).get_lists_for_user(user_id)
            if lists:
                list_id = lists[0].id
            else:
                lst = TodoListHandler(session).create_list(user_id, "Meine Liste")
                list_id = lst.id
    todo = Todo(todo_list_id=list_id)
    _apply_js_data(todo, data.model_dump())
    with Session(engine) as session:
        saved = TodoHandler(session).save(todo)
        return _todo_to_js(saved)


@app.put("/api/todos/{todo_id}")
async def api_update_todo(todo_id: int, data: TodoData, request: Request):
    user_id = _get_user_id(request)
    if not user_id:
        return {"error": "Nicht autorisiert"}
    with Session(engine) as session:
        handler = TodoHandler(session)
        todo = handler.get_by_id(todo_id)
        if not todo:
            return {"error": "Nicht gefunden"}
        _apply_js_data(todo, data.model_dump())
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return _todo_to_js(todo)


@app.delete("/api/todos/{todo_id}")
async def api_delete_todo(todo_id: int, request: Request):
    user_id = _get_user_id(request)
    if not user_id:
        return {"error": "Nicht autorisiert"}
    with Session(engine) as session:
        TodoHandler(session).delete(todo_id)
    return {"success": True}
