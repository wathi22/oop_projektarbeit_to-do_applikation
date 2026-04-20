from app.services.UserHandler import UserHandler
from app.models.user import User


# Happy Path: Ein Benutzer wird erfolgreich gespeichert
def test_save_user_sets_id(session, sample_user):
    # Arrange
    user_handler = UserHandler(session)

    # Act
    saved_user = user_handler.save(sample_user)

    # Assert
    assert saved_user.id is not None


# Happy Path: Ein gespeicherter Benutzer wird erfolgreich gelöscht
def test_delete_user_removes_user_from_database(session, sample_user):
    # Arrange
    user_handler = UserHandler(session)

    # Act
    result = user_handler.delete(sample_user.id)

    # Assert
    assert result is True
    assert user_handler.get_by_id(sample_user.id) is None


# Edge Case: Löschen mit unbekannter ID soll False zurückgeben
def test_delete_returns_false_for_unknown_user(session):
    # Arrange
    user_handler = UserHandler(session)

    # Act
    result = user_handler.delete(9999)

    # Assert
    assert result is False


# Happy Path: Benutzer kann über ID wieder gefunden werden
def test_get_by_id_returns_saved_user(session, sample_user):
    # Arrange
    user_handler = UserHandler(session)

    # Act
    retrieved_user = user_handler.get_by_id(sample_user.id)

    # Assert
    assert retrieved_user is not None
    assert retrieved_user.id == sample_user.id


# Edge Case: Unbekannte ID soll None zurückgeben
def test_get_by_id_returns_none_for_unknown_user(session):
    # Arrange
    user_handler = UserHandler(session)

    # Act
    result = user_handler.get_by_id(9999)

    # Assert
    assert result is None


# Happy Path: Alle gespeicherten Benutzer werden zurückgegeben
def test_get_all_returns_all_users(session):
    # Arrange
    user_handler = UserHandler(session)

    user1 = User(
        firstname="Wathanak",
        lastname="Deng",
        email="wathanak.deng@example.com",
        password_hash=User.hash_password("password123"),
    )
    user2 = User(
        firstname="Matthias",
        lastname="Heiniger",
        email="matthias.heiniger@example.com",
        password_hash=User.hash_password("password123"),
    )
    user_handler.save(user1)
    user_handler.save(user2)

    # Act
    users = user_handler.get_all()

    # Assert
    assert len(users) == 2
    user_ids = [u.id for u in users]
    assert user1.id in user_ids
    assert user2.id in user_ids


# Happy Path: Vorname und E-Mail eines Benutzers werden erfolgreich aktualisiert
def test_update_changes_user_fields(session, sample_user):
    # Arrange
    user_handler = UserHandler(session)

    # Act
    updated_user = user_handler.update(
        sample_user.id,
        firstname="Updated",
        email="updated@example.com",
    )

    # Assert
    assert updated_user is not None
    assert updated_user.firstname == "Updated"
    assert updated_user.email == "updated@example.com"


# Edge Case: Update mit unbekannter ID soll None zurückgeben
def test_update_returns_none_for_unknown_user(session):
    # Arrange
    user_handler = UserHandler(session)

    # Act
    updated_user = user_handler.update(
        9999,
        firstname="Updated",
        email="updated@example.com",
    )

    # Assert
    assert updated_user is None


# Happy Path: Benutzer kann über E-Mail gefunden werden
def test_get_by_email_returns_matching_user(session, sample_user):
    # Arrange
    user_handler = UserHandler(session)

    # Act
    retrieved_user = user_handler.get_by_email(sample_user.email)

    # Assert
    assert retrieved_user is not None
    assert retrieved_user.id == sample_user.id
    assert retrieved_user.email == sample_user.email


# Edge Case: Unbekannte E-Mail soll None zurückgeben
def test_get_by_email_returns_none_for_unknown_email(session):
    # Arrange
    user_handler = UserHandler(session)

    # Act
    result = user_handler.get_by_email("unknown@example.com")

    # Assert
    assert result is None