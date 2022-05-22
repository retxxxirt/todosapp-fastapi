import typing
from datetime import datetime, date
from enum import Enum
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Column, TEXT, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as _UUID
from sqlmodel import Field, Relationship, SQLModel

from app.common.pagination import Ordering
from app.database.schemas import DatabaseModel

if typing.TYPE_CHECKING:
    from app.users.schemas import User


class TodoBase(BaseModel):
    """Base todo_ schema"""

    title: str
    is_completed: bool = Field(False, nullable=False)
    description: str = Field(None, sa_column=Column(TEXT))
    remind_at: datetime = None


class Todo(TodoBase, DatabaseModel, SQLModel, table=True):
    """Database todo_ schema"""

    user_id: UUID = Field(
        sa_column=Column(
            _UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        )
    )

    user: "User" = Relationship(back_populates="todos")


class TodoRead(TodoBase):
    """Todo_ read schema"""

    id: UUID
    created_at: datetime


class TodoCreate(TodoBase):
    """Todo_ create schema"""


class TodoUpdate(TodoBase):
    """Todo_ partial update schema"""

    title: str = None
    is_completed: bool = None


class TodosOrderBy(str, Enum):
    """Todos order by enum"""

    created_at = "created_at"
    remind_at = "remind_at"


class TodosFilter(BaseModel):
    """Todos filter schema"""

    order_by: TodosOrderBy = TodosOrderBy.created_at
    ordering: Ordering = Ordering.asc

    is_completed: bool = None
    remind_at_from: date = None
    remind_at_to: date = None
