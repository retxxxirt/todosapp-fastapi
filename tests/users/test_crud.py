import uuid

import pytest
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.users import crud
from app.users.schemas import UserCreate, User, UserUpdate
from tests.users.fixtures import UserData


def test_get_user_by_id(session: Session, user: User):
    assert crud.get_user_by_id(session, user.id).id == user.id


def test_get_user_by_id_nonexistent(session: Session, users: list[User]):
    assert crud.get_user_by_id(session, uuid.uuid4()) is None


def test_get_user_by_username(session: Session, user: User):
    assert crud.get_user_by_username(session, user.username).id == user.id


def test_get_user_by_username_nonexistent(session: Session, users: list[User]):
    assert crud.get_user_by_username(session, "nonexistent-username") is None


def test_create_user(session: Session):
    data = UserCreate(username="username", password="password")
    user = crud.create_user(session, data)

    assert user.username == "username"
    assert pbkdf2_sha256.verify("password", user.password_hash)


def test_create_user_duplicated_username(session: Session, user: User):
    data = UserCreate(username=user.username, password="password")

    with pytest.raises(IntegrityError):
        crud.create_user(session, data)


def test_update_user(session: Session, user: User):
    changed_username = f"changed-{user.username}"
    data = UserUpdate(username=changed_username)
    user = crud.update_user(session, user, data)

    assert user.username == changed_username


def test_update_user_password(session: Session, user_data: UserData):
    new_password = f"new-{user_data.password}"
    user = crud.update_user_password(session, user_data.instance, password=new_password)
    assert pbkdf2_sha256.verify(new_password, user.password_hash)


def test_get_users(session: Session, users: list[User]):
    assert crud.get_users(session).count() == len(users)


def test_get_users_without_users(session: Session):
    assert crud.get_users(session).count() == 0


def test_delete_user(session: Session, user: User):
    crud.delete_user(session, user)
    assert session.query(User).get(user.id) is None
