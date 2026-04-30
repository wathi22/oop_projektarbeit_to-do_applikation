from app.services.TodoListHandler import TodoListHandler
from app.models.todo_list import TodoList
import pytest

# Happy Path: Eine TodoList wird erfolgreich gespeichert
def test_save_todo_list_sets_id(session, sample_todo_list):
    # Arrange
    todo_list_handler = TodoListHandler(session)

    # Act
    saved_todo_list = todo_list_handler.save(sample_todo_list)

    # Assert
    assert saved_todo_list.id is not None

# Happy Path: Eine TodoList wird erfolgreich gelöscht
def test_delete_todo_list_removes_it_from_db(session, sample_todo_list):
    # Arrange
    todo_list_handler = TodoListHandler(session)
    saved_todo_list = todo_list_handler.save(sample_todo_list)

    # Act
    result = todo_list_handler.delete(saved_todo_list.id)

    # Assert
    assert result is True
    assert todo_list_handler.get_by_id(saved_todo_list.id) is None  

# Edge Case: Versuch, eine nicht existierende TodoList zu löschen, soll False zurückgeben
def test_delete_nonexistent_todo_list_returns_false(session):   
    # Arrange
    todo_list_handler = TodoListHandler(session)

    # Act
    result = todo_list_handler.delete(9999)  # ID, die nicht existiert

    # Assert
    assert result is False

# Happy Path: Eine TodoList mit ID wird erfolgreich abgerufen
def test_get_by_id_returns_todo_list(session, sample_todo_list):    
    # Arrange
    todo_list_handler = TodoListHandler(session)
    saved_todo_list = todo_list_handler.save(sample_todo_list)

    # Act
    retrieved = todo_list_handler.get_by_id(saved_todo_list.id)

    # Assert
    assert retrieved is not None
    assert retrieved.id == saved_todo_list.id
    assert retrieved.name == saved_todo_list.name

# Edge Case: Versuch, eine nicht existierende TodoList abzurufen, soll None zurückgeben
def test_get_by_id_with_nonexistent_id_returns_none(session):
    # Arrange
    todo_list_handler = TodoListHandler(session)

    # Act
    result = todo_list_handler.get_by_id(9999)  # ID, die nicht existiert

    # Assert
    assert result is None

# Happy Path: Alle TodoLists werden erfolgreich abgerufen
def test_get_all_returns_all_todo_lists(session, sample_todo_list):
    # Arrange
    todo_list_handler = TodoListHandler(session)
    todo_list_handler.save(sample_todo_list)

    # Act
    all_lists = todo_list_handler.get_all()

    # Assert
    assert len(all_lists) >= 1  # Es könnte bereits andere Listen geben
    assert any(lst.id == sample_todo_list.id for lst in all_lists)

# Edge Case: Wenn keine TodoLists existieren, soll eine leere Liste zurückgegeben werden
def test_get_all_returns_empty_list_when_no_todo_lists_exist(session):
    # Arrange
    todo_list_handler = TodoListHandler(session)

    # Act
    all_lists = todo_list_handler.get_all()

    # Assert
    assert all_lists == []

# Happy Path: Eine TodoList wird erfolgreich aktualisiert
def test_update_todo_list_changes_fields(session, sample_todo_list):
    # Arrange
    todo_list_handler = TodoListHandler(session)

    # Act
    updated_todo_list = todo_list_handler.update(
        sample_todo_list.id,
        name="Updated Studium",
    )

    # Assert
    assert updated_todo_list is not None
    assert updated_todo_list.id == sample_todo_list.id
    assert updated_todo_list.name == "Updated Studium"


# Edge Case: Update mit nicht existierender ID soll None zurückgeben
def test_update_nonexistent_todo_list_returns_none(session):
    # Arrange
    todo_list_handler = TodoListHandler(session)

    # Act
    result = todo_list_handler.update(
        9999,
        name="Updated Name",
    )

    # Assert
    assert result is None


# Happy Path: Alle TodoLists eines Benutzers werden korrekt zurückgegeben
def test_get_lists_for_user_returns_only_matching_lists(session, sample_user):
    # Arrange
    todo_list_handler = TodoListHandler(session)

    todo_list_1 = TodoList(name="Studium", owner_id=sample_user.id)
    todo_list_2 = TodoList(name="Privat", owner_id=sample_user.id)

    todo_list_handler.save(todo_list_1)
    todo_list_handler.save(todo_list_2)

    # Act
    result = todo_list_handler.get_lists_for_user(sample_user.id)

    # Assert
    assert len(result) == 2
    assert all(todo_list.owner_id == sample_user.id for todo_list in result)


# Edge Case: Ein Benutzer ohne TodoLists soll eine leere Liste zurückbekommen
def test_get_lists_for_user_returns_empty_list_for_user_without_lists(session):
    # Arrange
    todo_list_handler = TodoListHandler(session)

    # Act
    result = todo_list_handler.get_lists_for_user(9999)

    # Assert
    assert result == []


# Happy Path: create_list erstellt eine neue TodoList korrekt
def test_create_list_creates_new_todo_list(session, sample_user):
    # Arrange
    todo_list_handler = TodoListHandler(session)

    # Act
    created_todo_list = todo_list_handler.create_list(sample_user.id, "Neue Liste")

    # Assert
    assert created_todo_list is not None
    assert created_todo_list.id is not None
    assert created_todo_list.name == "Neue Liste"
    assert created_todo_list.owner_id == sample_user.id


# Edge Case: create_list mit leerem Namen soll fehlschlagen
def test_create_list_with_empty_name_fails(session, sample_user):
    # Arrange
    todo_list_handler = TodoListHandler(session)

    # Act & Assert
    with pytest.raises(ValueError):
        todo_list_handler.create_list(sample_user.id, " ")

# Edge Case: update mit leerem Namen soll fehlschlagen
def test_update_with_empty_name_fails(session, sample_todo_list):
    # Arrange
    todo_list_handler = TodoListHandler(session)

    # Act & Assert
    with pytest.raises(ValueError):
        todo_list_handler.update(sample_todo_list.id, name="   ")