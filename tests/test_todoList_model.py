from app.models.todo_list import TodoList
from app.models.todo import Todo, Status, Priority
import pytest


# Happy Path: Ein Todo wird einer TodoList hinzugefuegt
def test_add_todo_appends_todo():
    # Arrange
    todo_list = TodoList(name="Studium")
    todo_list.todos = []
    todo = Todo(id=1, title="ORM lernen", status=Status.BACKLOG, priority=Priority.HIGH)

    # Act
    todo_list.add_todo(todo)

    # Assert
    assert todo_list.todos == [todo]


# Happy Path: Ein Todo wird anhand der ID aus der TodoList entfernt
def test_remove_todo_removes_matching_todo_id():
    # Arrange
    todo1 = Todo(id=1, title="Task 1", status=Status.BACKLOG, priority=Priority.HIGH)
    todo2 = Todo(id=2, title="Task 2", status=Status.TODO, priority=Priority.LOW)
    todo_list = TodoList(name="Studium")
    todo_list.todos = [todo1, todo2]

    # Act
    todo_list.remove_todo(1)

    # Assert
    assert todo_list.todos == [todo2]


# Happy Path: Alle Todos einer TodoList werden korrekt zurückgegeben
def test_get_all_todos_returns_all_todos():
    # Arrange
    todo1 = Todo(title="Task 1", status=Status.BACKLOG, priority=Priority.HIGH)
    todo2 = Todo(title="Task 2", status=Status.BACKLOG, priority=Priority.LOW)

    todo_list = TodoList(name="Studium")
    todo_list.todos = [todo1, todo2]

    # Act
    todos = todo_list.get_all_todos()

    # Assert
    assert len(todos) == 2
    assert todos[0].title == "Task 1"
    assert todos[1].title == "Task 2"


# Edge Case: Eine leere TodoList soll eine leere Liste zurückgeben
def test_get_all_todos_returns_empty_list_when_no_todos_exist():
    # Arrange
    todo_list = TodoList(name="Leere Liste")
    todo_list.todos = []

    # Act
    todos = todo_list.get_all_todos()

    # Assert
    assert todos == []

@pytest.mark.parametrize("filter_status, expected_count", [
    (Status.BACKLOG, 2),
    (Status.TODO, 1),
    (Status.DONE, 0),
])

def test_filter_todos_by_status(filter_status, expected_count):
    # Arrange
    todo_list = TodoList(name="Studium")
    todo_list.todos = [
        Todo(title="Task 1", status=Status.BACKLOG, priority=Priority.HIGH),
        Todo(title="Task 2", status=Status.IN_PROGRESS, priority=Priority.LOW),
        Todo(title="Task 3", status=Status.BACKLOG, priority=Priority.LOW),
        Todo(title="Task 4", status=Status.TODO, priority=Priority.HIGH),
    ]

    # Act
    result = todo_list.filter_todos(status=filter_status)

    # Assert
    assert len(result) == expected_count

# Happy Path: Todos koennen nach Prioritaet gefiltert werden
def test_filter_todos_by_priority():
    # Arrange
    todo_list = TodoList(name="Studium")
    todo_list.todos = [
        Todo(title="Task 1", status=Status.BACKLOG, priority=Priority.HIGH),
        Todo(title="Task 2", status=Status.IN_PROGRESS, priority=Priority.LOW),
        Todo(title="Task 3", status=Status.TODO, priority=Priority.HIGH),
    ]

    # Act
    result = todo_list.filter_todos(priority=Priority.HIGH)

    # Assert
    assert len(result) == 2
    assert all(todo.priority == Priority.HIGH for todo in result)


# Happy Path: Status und Prioritaet koennen kombiniert gefiltert werden
def test_filter_todos_by_status_and_priority():
    # Arrange
    todo_list = TodoList(name="Studium")
    todo_list.todos = [
        Todo(title="Task 1", status=Status.BACKLOG, priority=Priority.HIGH),
        Todo(title="Task 2", status=Status.BACKLOG, priority=Priority.LOW),
        Todo(title="Task 3", status=Status.TODO, priority=Priority.HIGH),
    ]

    # Act
    result = todo_list.filter_todos(status=Status.BACKLOG, priority=Priority.HIGH)

    # Assert
    assert len(result) == 1
    assert result[0].title == "Task 1"


# Magic-Method Happy Path: __str__ gibt den Namen der TodoList zurück
def test_str_returns_todo_list_name():
    # Arrange
    todo_list = TodoList(name="Studium")

    # Act
    result = str(todo_list)

    # Assert
    assert result == "TodoList Name: Studium"

# Magic-Method Happy Path: __repr__ gibt eine detaillierte Darstellung der TodoList zurück
def test_repr_returns_detailed_representation():
    # Arrange
    todo_list = TodoList(id=1, name="Studium", owner_id=42)

    # Act
    result = repr(todo_list)

    # Assert
    assert result == "TodoList(id=1, name='Studium', owner_id=42)"

# Magic-Method Happy Path: __eq__ vergleicht zwei TodoList-Objekte basierend auf ihrer ID
def test_eq_returns_true_for_same_id():
    # Arrange
    todo_list1 = TodoList(id=1, name="Studium", owner_id=42)
    todo_list2 = TodoList(id=1, name="Freizeit", owner_id=99)

    # Act
    result = (todo_list1 == todo_list2)

    # Assert
    assert result is True

# Magic-Method Happy Path: __eq__ vergleicht zwei TodoList-Objekte mit unterschiedlichen IDs als ungleich und gleiche Attribute als gleich
def test_eq_returns_false_for_different_id():
    # Arrange
    todo_list1 = TodoList(id=1, name="Studium", owner_id=42)
    todo_list2 = TodoList(id=2, name="Studium", owner_id=42)

    # Act
    result = (todo_list1 == todo_list2)

    # Assert
    assert result is False

# Magic-Method Edge Case: __eq__ vergleicht ein TodoList-Objekt mit einem Objekt eines anderen Typs und gibt false zurück
def test_eq_returns_false_for_different_type():
    # Arrange
    todo_list = TodoList(id=1, name="Studium", owner_id=42)
    not_a_todo_list = "Ich bin kein TodoList-Objekt"

    # Act
    result = (todo_list == not_a_todo_list)

    # Assert
    assert result is False
