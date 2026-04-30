from app.models.user import User

# Happy Path: Passwort wird korrekt gehasht und überprüft
# Arrange
def test_password_hashing_and_check(sample_user):

        # Act
    result = sample_user.check_password("password123")

    # Assert
    assert result is True

# Happy Path: Passwort-Check schlägt fehl bei falschem Passwort
# Arrange
def test_password_check_fails_with_wrong_password(sample_user):

    # Act
    result = sample_user.check_password("wrongpassword")

    # Assert
    assert result is False

# Happy Path: __str__ gibt Vor- und Nachname zurück
def test_str_returns_full_name():

    # Arrange
    user = User(
        id=1,
        firstname="Wathanak",
        lastname="Deng",
        email="wathanak.deng@example.com",
        password_hash="dummy"
    )

    # Act
    result = str(user)

    # Assert
    assert result == "Wathanak Deng"

# Happy Path: __repr__ gibt alle wichtigen Felder zurück, aber versteckt das Passwort
def test_repr_returns_all_fields():

    # Arrange
    user = User(
        id=1,
        firstname="Wathanak",
        lastname="Deng",
        email="wathanak.deng@example.com",
        password_hash="dummy"
    )

    # Act
    repr_str = repr(user)

    # Assert
    assert "User(id=" in repr_str
    assert "firstname='Wathanak'" in repr_str
    assert "lastname='Deng'" in repr_str
    assert "email='wathanak.deng@example.com'" in repr_str
    assert "password_hash=" not in repr_str

# Magic-Method Happy Path __eq__ gleiche ID => gleich
def test_eq_returns_true_for_same_id():

    # Arrange
    user = User(
        id=1,
        firstname="Wathanak",
        lastname="Deng",
        email="wathanak.deng@example.com",
        password_hash="dummy"
    )

    user2 = User(
        id=user.id,                # GLEICH
        firstname="Max",                  # anders
        lastname="Mustermann",            # anders
        email="max@example.com",          # anders
        password_hash="dummy",            # anders
    )

    # Act
    result = (user == user2)

    # Assert
    assert result is True

# Magic-Method Happy Path __eq__ unterschiedliche ID => ungleich
def test_eq_returns_false_for_different_id():

    # Arrange
    user = User(
        id=1,
        firstname="Wathanak",
        lastname="Deng",
        email="wathanak.deng@example.com",
        password_hash="dummy"
    )

    user2 = User(
        id=999,
        firstname="Wathanak",
        lastname="Deng",
        email="wathanak.deng@example.com",
        password_hash="dummy"
    )

    # Act
    result = user == user2

    # Assert
    assert result is False

# Magic-Method Edge Case: Vergleich mit einem Objekt eines anderen Typs soll False zurückgeben
def test_eq_returns_false_when_comparing_with_different_type():

    # Arrange
    user = User(
        id=1,
        firstname="Wathanak",
        lastname="Deng",
        email="wathanak.deng@example.com",
        password_hash="dummy"
    )

    not_a_user = "Ich bin kein User-Objekt"

    # Act
    result = (user == not_a_user)

    # Assert
    assert result is False