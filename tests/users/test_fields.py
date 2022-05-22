import pytest

from app.users.fields import Username, Password


def test_username():
    assert Username.validate("valid-username") == "valid-username"
    assert Username.validate("._-valid-username-too") == "._-valid-username-too"


def test_username_invalid():
    with pytest.raises(ValueError):
        Username.validate("неверные буквы")

    with pytest.raises(ValueError):
        Username.validate("inval|d symb0]s")


def test_password():
    assert Password.validate("Passw0rd") == "Passw0rd"
    assert Password.validate("paSSword1") == "paSSword1"


def test_password_invalid():
    with pytest.raises(ValueError):
        Password.validate("weak-password")

    with pytest.raises(ValueError):
        Password.validate("$ti||-we@k-p@$$w0rd")
