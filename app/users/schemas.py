from enum import Enum
from uuid import UUID

from pydantic import BaseModel, validator
from sqlmodel import Field, SQLModel, Relationship

from app.database.schemas import DatabaseModel
from app.todos.schemas import Todo
from app.users.fields import Username, Password


class UserBase(BaseModel):
    """Base user schema"""

    username: Username = Field(sa_column_kwargs={"unique": True})


class User(UserBase, DatabaseModel, SQLModel, table=True):
    """Database user schema"""

    password_hash: str
    todos: list[Todo] = Relationship(back_populates="user")


class UserRead(UserBase):
    """User read schema"""

    id: UUID


class UserCreate(UserBase):
    """User create schema"""

    password: Password


class UserUpdate(UserBase):
    """User partial update schema"""

    username: Username = None


class PasswordConfirmationMixin(BaseModel):
    """Password confirmation mixin"""

    password: Password
    password_confirm: Password

    @validator("password_confirm")
    def validate_passwords_match(cls, value: str, values: dict) -> str:
        password = values.get("password")
        if password is None or value != password:
            raise ValueError("Passwords don't match")
        return value


class SignUp(UserCreate, PasswordConfirmationMixin):
    """Signup schema"""


class SignIn(UserBase):
    """Signin schema"""

    password: Password


class UserUpdatePassword(PasswordConfirmationMixin, BaseModel):
    """Update user password schema"""

    old_password: Password


class AccessTokenType(str, Enum):
    """Access token type enum"""

    bearer = "bearer"


class AccessToken(BaseModel):
    """Access token schema"""

    type: AccessTokenType
    access_token: str
