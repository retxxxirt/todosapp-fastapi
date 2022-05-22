from fastapi.testclient import TestClient
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlmodel import Session
from starlette import status

from app.users import errors
from app.users.schemas import AccessTokenType, User
from tests._utils import make_request
from tests.users.fixtures import UserData


def test_signup(session: Session, anonymous_client: TestClient):
    data = {"username": "username", "password": "password", "password_confirm": "password"}
    response, response_data = make_request(anonymous_client, "post", "/signup", data)

    assert response.status_code == status.HTTP_200_OK
    assert response_data["type"] == AccessTokenType.bearer
    assert isinstance(response_data["access_token"], str)

    user = session.query(User).where(User.username == "username").first()
    assert isinstance(user, User)


def test_signin(anonymous_client: TestClient, user_data: UserData):
    data = {"username": user_data.instance.username, "password": user_data.password}
    response, response_data = make_request(anonymous_client, "post", "/signin", data)

    assert response.status_code == status.HTTP_200_OK
    assert response_data["type"] == AccessTokenType.bearer
    assert isinstance(response_data["access_token"], str)


def test_signin_invalid_credentials(anonymous_client: TestClient, user_data: UserData):
    data = {"username": user_data.instance.username, "password": f"invalid-{user_data.password}"}
    response, response_data = make_request(anonymous_client, "post", "/signin", data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data["detail"][0]["msg"] == errors.INVALID_CREDENTIALS

    data = {"username": f"invalid-{user_data.instance.username}", "password": user_data.password}
    response, response_data = make_request(anonymous_client, "post", "/signin", data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data["detail"][0]["msg"] == errors.INVALID_CREDENTIALS


def test_list_users(client: TestClient, users: list[User]):
    response, response_data = make_request(client, "get", "/users/")
    assert response_data["count"] == len(users)

    for user, user_data in zip(users, response_data["items"]):
        assert str(user.id) == user_data["id"]


def test_get_profile(client: TestClient, user: User):
    response, response_data = make_request(client, "get", "/profile/")
    assert response_data["id"] == str(user.id)


def test_update_profile(client: TestClient, session: Session, user: User):
    data = {"username": (changed_username := f"changed-{user.username}")}
    response, response_data = make_request(client, "patch", "/profile/", data)

    assert response.status_code == status.HTTP_200_OK
    assert response_data["username"] == changed_username

    session.refresh(user)
    assert user.username == changed_username


def test_delete_profile(client: TestClient, session: Session, user: User):
    response, response_data = make_request(client, "delete", "/profile/")
    assert response.status_code == status.HTTP_200_OK

    assert session.query(User).get(user.id) is None


def test_change_password(client: TestClient, session: Session, user_data: UserData):
    changed_password = f"changed-{user_data.password}"

    data = {
        "old_password": user_data.password,
        "password": changed_password,
        "password_confirm": changed_password,
    }

    response, response_data = make_request(client, "patch", "/profile/password", data)
    assert response.status_code == status.HTTP_200_OK

    session.refresh(user_data.instance)
    assert pbkdf2_sha256.verify(changed_password, user_data.instance.password_hash)
