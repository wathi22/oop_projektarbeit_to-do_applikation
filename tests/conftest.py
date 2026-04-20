import pytest
from sqlmodel import SQLModel, create_engine, Session
from app.models.user import User
from app.models.todo_list import TodoList
from app.models.todo import (
    Todo,
    PRIORITY_HIGH,
    STATUS_BACKLOG,
)

@pytest.fixture
def engine():
    engine = create_engine("sqlite:///:memory:", echo=True)
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
def sample_todo(session, sample_todo_list):
    todo = Todo(
        title="ORM lernen",
        description="SQLModel und Handler verstehen",
        priority=PRIORITY_HIGH,
        status=STATUS_BACKLOG,
        progress=0,
        labels="studium,python",
        todo_list_id=sample_todo_list.id,
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo