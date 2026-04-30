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

# Happy Path: Status wechselt von Backlog zu To-Do
def test_toggle_status_changes_backlog_to_todo():
    # Arrange
    todo = Todo(
        title="ORM lernen",
        status=Status.BACKLOG,
        priority=Priority.HIGH,
    )

    # Act
    todo.toggle_status()

    # Assert
    assert todo.status == Status.TODO


# Happy Path: Status wechselt von To-Do zu In Progress
def test_toggle_status_changes_todo_to_in_progress():
    # Arrange
    todo = Todo(
        title="ORM lernen",
        status=Status.TODO,
        priority=Priority.HIGH,
    )

    # Act
    todo.toggle_status()

    # Assert
    assert todo.status == Status.IN_PROGRESS


# Happy Path: Status wechselt von In Progress zu Done
def test_toggle_status_changes_in_progress_to_done():
    # Arrange
    todo = Todo(
        title="ORM lernen",
        status=Status.IN_PROGRESS,
        priority=Priority.HIGH,
    )

    # Act
    todo.toggle_status()

    # Assert
    assert todo.status == Status.DONE


# Edge Case: Status Done springt wieder auf Backlog zurück
def test_toggle_status_cycles_done_back_to_backlog():
    # Arrange
    todo = Todo(
        title="ORM lernen",
        status=Status.DONE,
        priority=Priority.HIGH,
    )

    # Act
    todo.toggle_status()

    # Assert
    assert todo.status == Status.BACKLOG


# Happy Path: Fortschritt wird mit gültigem Wert aktualisiert
def test_update_progress_sets_valid_value():
    # Arrange
    todo = Todo(
        title="ORM lernen",
        progress=0,
        priority=Priority.LOW,
    )

    # Act
    todo.update_progress(75)

    # Assert
    assert todo.progress == 75


# Edge Case: Fortschritt 0 ist ein gültiger Grenzwert
def test_update_progress_allows_zero():
    # Arrange
    todo = Todo(
        title="ORM lernen",
        progress=50,
        priority=Priority.LOW,
    )

    # Act
    todo.update_progress(0)

    # Assert
    assert todo.progress == 0


# Edge Case: Fortschritt 100 ist ein gültiger Grenzwert
def test_update_progress_allows_hundred():
    # Arrange
    todo = Todo(
        title="ORM lernen",
        progress=50,
        priority=Priority.LOW,
    )

    # Act
    todo.update_progress(100)

    # Assert
    assert todo.progress == 100

# Edge Case: Fortschritt unter 0 soll ignoriert werden
def test_update_progress_ignores_minus_one():
    todo = Todo(title="Test", progress=50, priority=Priority.LOW)

    # Act
    todo.update_progress(-1)

    # Assert
    assert todo.progress == 50


# Edge Case: Fortschritt über 100 soll ignoriert werden
def test_update_progress_ignores_hundred_one():
    todo = Todo(title="Test", progress=50, priority=Priority.LOW)

    # Act
    todo.update_progress(101)

    # Assert
    assert todo.progress == 50


# Edge Case: Negativer Fortschritt soll ignoriert werden
def test_update_progress_ignores_negative_value():
    # Arrange
    todo = Todo(
        title="ORM lernen",
        progress=10,
        priority=Priority.LOW,
    )

    # Act
    todo.update_progress(-5)

    # Assert
    assert todo.progress == 10


# Edge Case: Fortschritt über 100 soll ignoriert werden
def test_update_progress_ignores_value_above_100():
    # Arrange
    todo = Todo(
        title="ORM lernen",
        progress=10,
        priority=Priority.LOW,
    )

    # Act
    todo.update_progress(150)

    # Assert
    assert todo.progress == 10


# Edge Case: Ohne Due Date ist ein Todo nie überfällig
def test_is_overdue_returns_false_when_due_date_is_none():
    # Arrange
    todo = Todo(
        title="ORM lernen",
        status=Status.BACKLOG,
        due_date=None,
        priority=Priority.HIGH,
    )

    # Act
    result = todo.is_overdue()

    # Assert
    assert result is False


# Happy Path: Vergangenes Due Date und nicht Done => überfällig
def test_is_overdue_returns_true_for_past_due_date_and_open_status():
    # Arrange
    todo = Todo(
        title="ORM lernen",
        status=Status.TODO,
        due_date=date.today() - timedelta(days=1),
        priority=Priority.HIGH,
    )

    # Act
    result = todo.is_overdue()

    # Assert
    assert result is True


# Happy Path: Zukünftiges Due Date => nicht überfällig
def test_is_overdue_returns_false_for_future_due_date():
    # Arrange
    todo = Todo(
        title="ORM lernen",
        status=Status.TODO,
        due_date=date.today() + timedelta(days=3),
        priority=Priority.HIGH,
    )

    # Act
    result = todo.is_overdue()

    # Assert
    assert result is False


# Edge Case: Vergangenes Due Date, aber Status Done => nicht überfällig
def test_is_overdue_returns_false_when_todo_is_done():
    # Arrange
    todo = Todo(
        title="ORM lernen",
        status=Status.DONE,
        due_date=date.today() - timedelta(days=1),
        priority=Priority.HIGH,
    )

    # Act
    result = todo.is_overdue()

    # Assert
    assert result is False

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
