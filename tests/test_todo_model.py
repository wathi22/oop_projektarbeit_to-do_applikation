from datetime import date, timedelta
from app.services.TodoHandler import TodoHandler
import pytest

from app.models.todo import (
    Todo,
    Status,
    Priority
)

# Edge Case: Ungültiger Priority-Wert wird abgelehnt
def test_update_with_invalid_priority_raises_value_error(session, sample_todo):
    handler = TodoHandler(session)
    with pytest.raises(ValueError):
        handler.update(sample_todo.id, priority="banane")

# Toggle Status zusammengefügt
@pytest.mark.parametrize("initial_status, expected_status", [
    (Status.BACKLOG, Status.TODO),
    (Status.TODO, Status.IN_PROGRESS),
    (Status.IN_PROGRESS, Status.DONE),
    (Status.DONE, Status.BACKLOG),
])

# Happy Path: toggle_status wechselt den Status in der richtigen Reihenfolge
def test_toggle_status_cycles_through_all_statuses(initial_status, expected_status):
    # Arrange
    todo = Todo(
        title="ORM lernen",
        status=initial_status,
        priority=Priority.HIGH,
    )
    # Act
    todo.toggle_status()
    # Assert
    assert todo.status == expected_status

# Progress Update zusammengefügt
@pytest.mark.parametrize("valid_value", [0, 25, 50, 100])

# Happy Path: Fortschritt wird mit gültigem Wert aktualisiert
def test_update_progress_with_valid_values(valid_value):
    # Arrange
    todo = Todo(
        title="ORM lernen",
        progress=0,
        priority=Priority.LOW,
    )

    # Act
    todo.update_progress(valid_value)

    # Assert
    assert todo.progress == valid_value

# Edge Case: Ungültige Fortschrittswerte werden ignoriert
@pytest.mark.parametrize("invalid_value", [-1, -5, 101, 150])
def test_update_progress_ignores_invalid_values(invalid_value):
    # Arrange
    todo = Todo(title="ORM lernen", progress=10, priority=Priority.LOW)
    
    # Act
    todo.update_progress(invalid_value)
    
    # Assert
    assert todo.progress == 10

@pytest.mark.parametrize("status, due_date, expected", [
    (Status.BACKLOG, None, False),
    (Status.TODO, date.today() - timedelta(days=1), True),
    (Status.TODO, date.today() + timedelta(days=3), False),
    (Status.DONE, date.today() - timedelta(days=1), False),
])

def test_is_overdue(status, due_date, expected):
    # Arrange
    todo = Todo(
        title="ORM lernen",
        status=status,
        due_date=due_date,
        priority=Priority.HIGH,
    )

    # Act
    result = todo.is_overdue()

    # Assert
    assert result == expected

# Magic-Method Happy Path __str__ gibt Titel und Status zurück
def test_str_returns_title_and_status():
    # Arrange
    todo = Todo(
        title="ORM lernen",
        status=Status.BACKLOG,
    )

    # Act
    result = str(todo)
    
    # Assert
    assert result == "ORM lernen [Backlog]"

# Magic-Method Happy Path __repr__ gibt alle wichtigen Felder zurück
def test_repr_contains_key_fields():
    # Arrange
    todo = Todo(
        id=1,
        title="ORM lernen",
        priority=Priority.HIGH,
        status=Status.TODO,
    )

    # Act
    result = repr(todo)

    # Assert
    assert result.startswith("Todo(")
    assert "id=1" in result
    assert "title='ORM lernen'" in result
    assert "status=" in result

# Magic-Method Happy Path __eq__  gleiche ID und unterschiedliche Attribute => trotzdem gleich
def test_eq_returns_true_for_same_id():
    # Arrange
    todo1 = Todo(
        id=1,
        title="ORM lernen",
        priority=Priority.HIGH,
        status=Status.TODO,
    )
    todo2 = Todo(
        id=1,
        title="Math lernen",
        priority=Priority.LOW,
        status=Status.BACKLOG,
    )

    # Act
    result = (todo1 == todo2)

    # Assert
    assert result is True

# Magic-Method Happy Path __eq__ unterschiedliche ID und gleiche Attribute => trotzdem ungleich
def test_eq_returns_false_for_different_id():
    # Arrange
    todo1 = Todo(
        id=1,
        title="ORM lernen",
        priority=Priority.HIGH,
        status=Status.TODO,
    )
    todo2 = Todo(
        id=2,
        title="ORM lernen",
        priority=Priority.HIGH,
        status=Status.TODO,
    )

    # Act
    result = (todo1 == todo2)

    # Assert
    assert result is False

# Magic-Method Edge Case: Vergleich mit einem Objekt eines anderen Typs soll False zurückgeben
def test_eq_returns_false_when_comparing_with_different_type():
    # Arrange
    todo = Todo(
        id=1,
        title="Mathe Lernen",
        description="Angwandte Mathematik lernen",
        priority=Priority.HIGH,
        status=Status.TODO,
        progress=50,
        start_date=date(2024, 6, 1),
        due_date=date(2024, 6, 30),
    )
    not_a_todo = "Ich bin kein Todo-Objekt"
    # Act
    result = (todo == not_a_todo)
    # Assert
    assert result is False

# __lt__ Happy Path: zwei Todos mit Datum
def test_lt_compares_due_dates():
    # Arrange
    todo1 = Todo(
        title="Mathematik lernen",
        due_date=date(2024, 6, 10),
    )
    todo2 = Todo(
        title="Programmieren lernen",
        due_date=date(2024, 6, 15),
    )

    # Act
    result = (todo1 < todo2)

    # Assert
    assert result is True

# __lt__ Edge Case: Test 2 — Edge Case: self mit due_date, other ohne due_date → self ist "kleiner" → True
def test_lt_with_one_due_date():
    # Arrange
    todo_with_due_date = Todo(
        title="Mathematik lernen",
        due_date=date(2024, 6, 10),
    )
    todo_without_due_date = Todo(
        title="Programmieren lernen",
        due_date=None,
    )

    # Act
    result = (todo_with_due_date < todo_without_due_date)

    # Assert
    assert result is True

# __lt__ Edge Case: Anderer Typ soll NotImplemented zurückgeben
def test_lt_with_different_type_returns_not_implemented():
    # Arrange
    todo = Todo(
        title="Mathematik lernen",
        due_date=date(2024, 6, 10),
    )
    not_a_todo = "Ich bin kein Todo-Objekt"

    # Assert and Act
    with pytest.raises(TypeError):
        result = (todo < not_a_todo)

# Happy Path: from_dict erstellt ein Todo-Objekt mit den richtigen Attributen
def test_from_dict_creates_todo_with_correct_attributes():
    # Arrange
    data = {
        "title": "Mathematik lernen",
        "description": "Angwandte Mathematik lernen",
        "priority": "high",
        "status": "To-Do",
        "progress": 50,
        "start_date": "2024-06-01",
        "due_date": "2024-06-30",
    }

    # Act
    todo = Todo.from_dict(data)

    # Assert
    assert todo.title == "Mathematik lernen"
    assert todo.description == "Angwandte Mathematik lernen"
    assert todo.priority == Priority.HIGH
    assert todo.status == Status.TODO
    assert todo.progress == 50
    assert todo.start_date == date(2024, 6, 1)
    assert todo.due_date == date(2024, 6, 30)

# Happy Path: from_dict mit minimalen Daten (nur Titel) erstellt ein Todo-Objekt mit Standardwerten
def test_from_dict_with_minimal_data():
    # Arrange
    data = {
        "title": "Mathematik lernen",
    }

    # Act
    todo = Todo.from_dict(data)

    # Assert
    assert todo.title == "Mathematik lernen"
    assert todo.description == ""
    assert todo.priority == Priority.LOW
    assert todo.status == Status.BACKLOG
    assert todo.progress == 0
    assert todo.start_date is None
    assert todo.due_date is None

# Edge Case: Fehlendes Pflichtfeld "title" soll einen error auslösen
def test_from_dict_missing_title_error():
    # Arrange
    data = {
        "description": "Angwandte Mathematik lernen",
    }

    # Act and Assert
    with pytest.raises(KeyError):
        todo = Todo.from_dict(data)