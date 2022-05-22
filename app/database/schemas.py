import uuid
from datetime import datetime
from typing import TypeVar, Generic

from pydantic.generics import GenericModel
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, Session

T = TypeVar("T")


class DatabaseModel(GenericModel, Generic[T]):
    """Base database model"""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True, nullable=False)

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name based on class name"""
        return cls.__name__.lower() + "s"

    @classmethod
    def create(cls, session: Session, **fields) -> T:
        """Create class instance with given fields, flush it and refresh"""

        instance = cls(**fields)

        session.add(instance)
        session.flush()
        session.refresh(instance)

        return instance

    def update(self, session: Session, **fields) -> tuple[T, dict]:
        """Update class instance with given fields, flush it and refresh"""

        changes, fields["updated_at"] = {}, datetime.utcnow()

        for field, value in fields.items():
            if (perv_value := getattr(self, field)) != value:
                changes[field] = perv_value

            setattr(self, field, value)

        session.add(self)
        session.flush()
        session.refresh(self)

        return self, changes

    def delete(self, session: Session):
        """Delete class instance"""
        session.delete(self)
        session.flush()
