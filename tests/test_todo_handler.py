from datetime import date
import pytest
from app.services.TodoHandler import TodoHandler
from app.models.todo import (
    Todo,
    Status,
    Priority
)


# Happy Path: Ein Todo wird erfolgreich gespeichert
def test_save_todo_sets_id(session, sample_todo_list):
    # Arrange
    todo_handler = TodoHandler(session)
    todo = Todo(
        title="SQLModel lernen",
        description="ORM und Handler verstehen",
        priority=Priority.HIGH,
        status=Status.BACKLOG,
        progress=0,
        labels="studium,python",
        todo_list_id=sample_todo_list.id,
    )

    # Act
    saved_todo = todo_handler.save(todo)

    # Assert
    assert saved_todo.id is not None
    assert saved_todo.title == "SQLModel lernen"


# Happy Path: Ein Todo wird erfolgreich gelöscht
def test_delete_todo_removes_it_from_database(session, sample_todo):
    # Arrange
    todo_handler = TodoHandler(session)

    # Act
    result = todo_handler.delete(sample_todo.id)

    # Assert
    assert result is True
    assert todo_handler.get_by_id(sample_todo.id) is None


# Edge Case: Löschen mit unbekannter ID soll False zurückgeben
def test_delete_returns_false_for_unknown_todo(session):
    # Arrange
    todo_handler = TodoHandler(session)

    # Act
    result = todo_handler.delete(9999)

    # Assert
    assert result is False


# Happy Path: Todo kann über ID gefunden werden
def test_get_by_id_returns_saved_todo(session, sample_todo):
    # Arrange
    todo_handler = TodoHandler(session)

    # Act
    retrieved_todo = todo_handler.get_by_id(sample_todo.id)

    # Assert
    assert retrieved_todo is not None
    assert retrieved_todo.id == sample_todo.id
    assert retrieved_todo.title == sample_todo.title


# Edge Case: Unbekannte ID soll None zurückgeben
def test_get_by_id_returns_none_for_unknown_todo(session):
    # Arrange
    todo_handler = TodoHandler(session)

    # Act
    result = todo_handler.get_by_id(9999)

    # Assert
    assert result is None


# Happy Path: Alle Todos werden korrekt zurückgegeben
def test_get_all_returns_all_todos(session, sample_todo_list):
    # Arrange
    todo_handler = TodoHandler(session)

    todo1 = Todo(
        title="Task 1",
        description="Beschreibung 1",
        priority=Priority.HIGH,
        status=Status.BACKLOG,
        progress=0,
        todo_list_id=sample_todo_list.id,
    )
    todo2 = Todo(
        title="Task 2",
        description="Beschreibung 2",
        priority=Priority.LOW,
        status=Status.BACKLOG,
        progress=0,
        todo_list_id=sample_todo_list.id,
    )

    todo_handler.save(todo1)
    todo_handler.save(todo2)

    # Act
    todos = todo_handler.get_all()

    # Assert
    assert len(todos) == 2
    todo_ids = [todo.id for todo in todos]
    assert todo1.id in todo_ids
    assert todo2.id in todo_ids


# Edge Case: Wenn keine Todos existieren, soll leere Liste zurückgegeben werden
def test_get_all_returns_empty_list_when_no_todos_exist(session):
    # Arrange
    todo_handler = TodoHandler(session)

    # Act
    todos = todo_handler.get_all()

    # Assert
    assert todos == []


# Happy Path: Titel, Beschreibung, Priorität und Status werden erfolgreich aktualisiert
def test_update_changes_todo_fields(session, sample_todo):
    # Arrange
    todo_handler = TodoHandler(session)

    # Act
    updated_todo = todo_handler.update(
        sample_todo.id,
        title="Updated Task",
        description="Neue Beschreibung",
        priority=Priority.CRITICAL,
        status=Status.IN_PROGRESS,
        progress=50,
        labels="updated,important",
    )

    # Assert
    assert updated_todo is not None
    assert updated_todo.title == "Updated Task"
    assert updated_todo.description == "Neue Beschreibung"
    assert updated_todo.priority == Priority.CRITICAL
    assert updated_todo.status == Status.IN_PROGRESS
    assert updated_todo.progress == 50
    assert updated_todo.labels == "updated,important"


def test_update_changes_todo_link_and_attachment(session, sample_todo):
    # Arrange
    todo_handler = TodoHandler(session)

    # Act
    updated_todo = todo_handler.update(
        sample_todo.id,
        link="https://example.com/spec",
        attachment_path="/todo-uploads/spec.pdf",
        attachment_name="spec.pdf",
    )

    # Assert
    assert updated_todo is not None
    assert updated_todo.link == "https://example.com/spec"
    assert updated_todo.attachment_path == "/todo-uploads/spec.pdf"
    assert updated_todo.attachment_name == "spec.pdf"


# Happy Path: Start- und Due-Date werden erfolgreich aktualisiert
def test_update_changes_todo_dates(session, sample_todo):
    # Arrange
    todo_handler = TodoHandler(session)

    # Act
    updated_todo = todo_handler.update(
        sample_todo.id,
        start_date=date(2026, 4, 20),
        due_date=date(2026, 4, 30),
    )

    # Assert
    assert updated_todo is not None
    assert updated_todo.start_date == date(2026, 4, 20)
    assert updated_todo.due_date == date(2026, 4, 30)


# Edge Case: Update mit unbekannter ID soll None zurückgeben
def test_update_returns_none_for_unknown_todo(session):
    # Arrange
    todo_handler = TodoHandler(session)

    # Act
    result = todo_handler.update(
        9999,
        title="Unknown",
    )

    # Assert
    assert result is None


# Happy Path: Todos einer bestimmten Liste werden korrekt zurückgegeben
def test_get_todos_for_list_returns_matching_todos(session, sample_todo_list):
    # Arrange
    todo_handler = TodoHandler(session)

    todo1 = Todo(
        title="Task 1",
        priority=Priority.HIGH,
        status=Status.BACKLOG,
        todo_list_id=sample_todo_list.id,
    )
    todo2 = Todo(
        title="Task 2",
        priority=Priority.LOW,
        status=Status.BACKLOG,
        todo_list_id=sample_todo_list.id,
    )

    todo_handler.save(todo1)
    todo_handler.save(todo2)

    # Act
    result = todo_handler.get_todos_for_list(sample_todo_list.id)

    # Assert
    assert len(result) == 2
    assert all(todo.todo_list_id == sample_todo_list.id for todo in result)


# Edge Case: Für eine Liste ohne Todos soll leere Liste zurückgegeben werden
def test_get_todos_for_list_returns_empty_list_when_no_todos_exist(session, sample_todo_list):
    # Arrange
    todo_handler = TodoHandler(session)

    # Act
    result = todo_handler.get_todos_for_list(sample_todo_list.id)

    # Assert
    assert result == []


# Happy Path: Todos einer Liste koennen nach Status gefiltert werden
def test_get_todos_for_list_filters_by_status(session, sample_todo_list):
    # Arrange
    todo_handler = TodoHandler(session)
    todo_handler.save(Todo(
        title="Task 1",
        priority=Priority.HIGH,
        status=Status.BACKLOG,
        todo_list_id=sample_todo_list.id,
    ))
    todo_handler.save(Todo(
        title="Task 2",
        priority=Priority.LOW,
        status=Status.DONE,
        todo_list_id=sample_todo_list.id,
    ))

    # Act
    result = todo_handler.get_todos_for_list(
        sample_todo_list.id,
        status_filter=Status.DONE,
    )

    # Assert
    assert len(result) == 1
    assert result[0].status == Status.DONE


# Happy Path: Todos einer Liste koennen nach Prioritaet gefiltert werden
def test_get_todos_for_list_filters_by_priority(session, sample_todo_list):
    # Arrange
    todo_handler = TodoHandler(session)
    todo_handler.save(Todo(
        title="Task 1",
        priority=Priority.HIGH,
        status=Status.BACKLOG,
        todo_list_id=sample_todo_list.id,
    ))
    todo_handler.save(Todo(
        title="Task 2",
        priority=Priority.LOW,
        status=Status.BACKLOG,
        todo_list_id=sample_todo_list.id,
    ))

    # Act
    result = todo_handler.get_todos_for_list(
        sample_todo_list.id,
        priority_filter=Priority.HIGH,
    )

    # Assert
    assert len(result) == 1
    assert result[0].priority == Priority.HIGH


# Happy Path: Der Status eines Todos wird erfolgreich weitergeschaltet
def test_toggle_status_changes_todo_status(session, sample_todo):
    # Arrange
    todo_handler = TodoHandler(session)
    old_status = sample_todo.status

    # Act
    updated_todo = todo_handler.toggle_status(sample_todo.id)

    # Assert
    assert updated_todo is not None
    assert updated_todo.status != old_status


# Edge Case: toggle_status mit unbekannter ID soll None zurückgeben
def test_toggle_status_returns_none_for_unknown_todo(session):
    # Arrange
    todo_handler = TodoHandler(session)

    # Act
    result = todo_handler.toggle_status(9999)

    # Assert
    assert result is None


# Happy Path: Der Fortschritt eines Todos wird erfolgreich aktualisiert
def test_update_progress_changes_progress(session, sample_todo):
    # Arrange
    todo_handler = TodoHandler(session)

    # Act
    updated_todo = todo_handler.update_progress(sample_todo.id, 80)

    # Assert
    assert updated_todo is not None
    assert updated_todo.progress == 80


# Edge Case: update_progress mit unbekannter ID soll None zurückgeben
def test_update_progress_returns_none_for_unknown_todo(session):
    # Arrange
    todo_handler = TodoHandler(session)

    # Act
    result = todo_handler.update_progress(9999, 80)

    # Assert
    assert result is None


# Edge Case: Ungültiger Fortschritt über 100 soll den alten Wert beibehalten
def test_update_progress_keeps_old_value_for_invalid_progress(session, sample_todo):
    # Arrange
    todo_handler = TodoHandler(session)
    old_progress = sample_todo.progress

    # Act
    updated_todo = todo_handler.update_progress(sample_todo.id, 150)

    # Assert
    assert updated_todo is not None
    assert updated_todo.progress == old_progress


# Edge Case: Ungültiger Fortschritt soll ValueError auslösen
@pytest.mark.parametrize("invalid_progress", [-10, 150])
def test_update_raises_value_error_for_invalid_progress(session, sample_todo, invalid_progress):
    # Arrange
    todo_handler = TodoHandler(session)

    # Act & Assert
    with pytest.raises(ValueError):
        todo_handler.update(
            sample_todo.id,
            progress=invalid_progress,
        )

# Happy Path: update() akzeptiert gültigen Fortschritt
@pytest.mark.parametrize("valid_progress", [0, 50, 100])
def test_update_accepts_valid_progress(
    session,
    sample_todo,
    valid_progress,
):
    # Arrange
    todo_handler = TodoHandler(session)

    # Act
    updated_todo = todo_handler.update(
        sample_todo.id,
        progress=valid_progress,
    )

    # Assert
    assert updated_todo is not None
    assert updated_todo.progress == valid_progress
