from typing import Iterable
from uuid import UUID

from sqlalchemy.orm import Query
from sqlmodel import Session, select

from app.users import services
from app.users.schemas import UserCreate, User, UserUpdate


def get_user_by_id(session: Session, user_id: UUID | str) -> User | None:
    """Get user by id, return None if user not exists"""
    return session.exec(select(User).where(User.id == user_id)).first()


def get_user_by_username(session: Session, username: str) -> User | None:
    """Get user by name, return None if user not exists"""
    return session.exec(select(User).where(User.username == username)).first()


def create_user(session: Session, data: UserCreate) -> User:
    """Create user, generate password_hash for them"""

    user_data = data.dict(exclude={"password"})
    user_data["password_hash"] = services.encode_password(data.password)

    return User.create(session, **user_data)


def update_user(session: Session, user: User, data: UserUpdate) -> User:
    """Update user partially"""
    return user.update(session, **data.dict(exclude_unset=True))[0]


def update_user_password(session: Session, user: User, password: str) -> User:
    """Update user password"""
    return user.update(session, password_hash=services.encode_password(password))[0]


def get_users(session: Session) -> Query | Iterable[User]:
    """Get all users"""
    return session.query(User)


def delete_user(session: Session, user: User):
    """Delete user"""
    user.delete(session)
