from dataclasses import dataclass

import pytest
from sqlmodel import Session

from app.users import services as users_services
from app.users.schemas import User


@dataclass
class UserData:
    instance: User
    password: str


@pytest.fixture
def users_data(session: Session) -> list[UserData]:
    """Generate users and save them in database, return users_data"""

    users = []

    for index in range(3):
        password_hash = users_services.encode_password("Passw0rd")
        user = User(username=f"username{index}", password_hash=password_hash)
        users.append(UserData(user, "Passw0rd"))

        session.add(user)
        session.flush()
        session.refresh(user)

    return users


@pytest.fixture
def users(users_data: list[UserData]) -> list[User]:
    """Unpack users from users_data"""
    return [d.instance for d in users_data]


@pytest.fixture
def user_data(users_data: list[UserData]) -> UserData:
    """Get first user_data from users_data"""
    return users_data[0]


@pytest.fixture
def user(user_data: UserData) -> User:
    """Unpack user from user_data"""
    return user_data.instance
