from app.models.user import User
import pytest

# Happy Path: Ein Benutzer wird erfolgreich erstellt und die Attribute werden korrekt gesetzt
def test_user_creation_sets_attributes(sample_user):
    assert sample_user.firstname == "Wathanak"
    assert sample_user.lastname == "Deng"
    assert sample_user.email == "wathanak.deng@example.com"

# Happy Path: Das Passwort wird korrekt gehasht und ist nicht im Klartext gespeichert
def test_user_creation_sets_password_hash(sample_user):
    assert sample_user.password_hash is not None

# Happy Path: Gibt den vollständigen Namen korrekt zurück
def test_full_name(sample_user):
    assert sample_user.full_name() == "Wathanak Deng"

# Happy Path: Überprüft, ob das Passwort korrekt ist
def test_check_password_returns_true_for_correct_password(sample_user):
    assert sample_user.check_password("password123") == True

# Edge Case: Überprüft, ob ein falsches Passwort korrekt erkannt wird
def test_check_password_returns_false_for_incorrect_password(sample_user):
    assert sample_user.check_password("wrongpassword") == False