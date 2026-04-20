from app.models.user import User
import pytest

def test_user_creation_sets_attributes():
    user = User(
        firstname="Wathanak",
        lastname="Deng",
        email="wathanak.deng@example.com",
        password_hash="dummy"
    )

    assert user.firstname == "Wathanak"
    assert user.lastname == "Deng"
    assert user.email == "wathanak.deng@example.com"

def test_full_name():
    user = User(firstname="Wathanak", lastname="Deng", email="wathanak.deng@example.com", password_hash=User.hash_password("password123"))
    assert user.full_name() == "Wathanak Deng"

def test_check_password_returns_true_for_correct_password(sample_user):
    assert sample_user.check_password("password123") == True

def test_check_password_returns_false_for_incorrect_password(sample_user):
    assert sample_user.check_password("wrongpassword") == False