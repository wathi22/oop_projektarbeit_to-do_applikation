# conftest.py – Projektstamm
#
# Diese Datei wird von pytest automatisch erkannt und erfüllt zwei Aufgaben:
#
# 1. Markiert den Projektstamm für pytest (rootdir)
#    → pytest weiss wo das Projekt beginnt und sucht Tests ab hier
#
# 2. Zusammen mit pytest.ini (pythonpath = .) wird der Projektstamm
#    automatisch zum Python-Suchpfad hinzugefügt
#    → alle Imports wie "from app.src.todo import Todo" funktionieren
#    → keine manuellen sys.path Anpassungen nötig
#
# Resultat: Jeder der das Repo klont kann direkt "pytest" ausführen
#           ohne irgendwelche Pfade manuell konfigurieren zu müssen.
import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy import event
from app.models import User, TodoList, Todo
from app.models.todo import Priority, Status

@pytest.fixture
def engine():
    engine = create_engine("sqlite:///:memory:", echo=False)

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    SQLModel.metadata.create_all(engine)
    return engine

@pytest.fixture
def session(engine):
    with Session(engine) as session:
        yield session

@pytest.fixture
def sample_user(session):
    user = User(
        firstname="Wathanak",
        lastname="Deng",
        email="wathanak.deng@example.com",
        password_hash = User.hash_password("password123"),
    )
    session.add(user)
    session.commit() 
    session.refresh(user)
    return user

@pytest.fixture
def sample_todo_list(session, sample_user):
    todo_list = TodoList(
        name="Studium",
        owner_id=sample_user.id,
    )
    session.add(todo_list)
    session.commit()
    session.refresh(todo_list)
    return todo_list

@pytest.fixture
def sample_todo_list_with_todos(session, sample_user):
    todo_List = TodoList(
        name="Studium", 
        owner_id=sample_user.id,
    )
    session.add(todo_List)
    session.commit()
    session.refresh(todo_List)

    todos = [
        Todo(
            title="ORM lernen",
            description="SQLModel und Handler verstehen",
            priority=Priority.HIGH,
            status=Status.BACKLOG,
            progress=0,
            labels="studium,python",
            todo_list_id=todo_List.id,
        ),
        Todo(
            title="Python üben",
            description="Übungsaufgaben lösen",
            priority=Priority.HIGH,
            status=Status.BACKLOG,
            progress=0,
            labels="studium,python",
            todo_list_id=todo_List.id,
        ),
        Todo(
            title="Docker kennenlernen",
            description="Docker Grundlagen verstehen",
            priority=Priority.HIGH,
            status=Status.BACKLOG,
            progress=0,
            labels="studium,docker",
            todo_list_id=todo_List.id,
        ),
    ]

    for todo in todos:
        session.add(todo)

    session.commit()
    return todo_List


@pytest.fixture
def sample_todo(session, sample_todo_list):
    todo = Todo(
        title="ORM lernen",
        description="SQLModel und Handler verstehen",
        priority=Priority.HIGH,
        status=Status.BACKLOG,
        progress=0,
        labels="studium,python",
        todo_list_id=sample_todo_list.id,
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo