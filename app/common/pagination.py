from enum import Enum
from typing import TypeVar, Generic, Sequence

from pydantic import BaseModel, conint
from pydantic.generics import GenericModel
from sqlalchemy.orm import Query

T = TypeVar("T")


class Paginator(BaseModel):
    """Limit-offset schema"""

    limit: conint(ge=1, le=25) = 25
    offset: conint(ge=0) = 0


class Page(GenericModel, Generic[T]):
    """Page schema"""

    count: conint(ge=0)
    items: Sequence[T]


class Ordering(str, Enum):
    """Ordering enum"""

    asc = "asc"
    desc = "desc"


def paginate(items: list | Query, paginator: Paginator) -> Page:
    """Paginate items with paginator"""

    if isinstance(items, Query):
        count = items.count()
        items = list(items.offset(paginator.offset).limit(paginator.limit))
    else:
        count = len(items)
        items = items[paginator.offset : paginator.offset + paginator.limit]

    return Page(count=count, items=items)
