from datetime import date, timedelta

from app.models.todo import (
    Todo,
    Status,
    Priority
)

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

# Happy Path
def test_string_representation():
    # Arrange
    todo = Todo(
        title="ORM lernen",
        status=Status.BACKLOG,
        priority=Priority.HIGH,
    )

    # Act
    result = str(todo)

    # Assert
    assert result == "ORM lernen [Backlog]"