from datetime import datetime, timedelta

import pytest
from sqlmodel import Session

from app.todos.schemas import Todo
from app.users.schemas import User


@pytest.fixture
def todos(session: Session, users: list[User]) -> list[Todo]:
    """Generate todos and save them in database"""

    todos = [
        Todo(user_id=users[0].id, title="Todo #1", description="Todo description"),
        Todo(user_id=users[0].id, title="Todo #2", remind_at=datetime.utcnow() + timedelta(days=1)),
        Todo(user_id=users[0].id, title="Todo #3", is_completed=True),
        Todo(user_id=users[1].id, title="Todo #1", description="Todo description"),
        Todo(user_id=users[1].id, title="Todo #2", description="Todo description"),
    ]

    session.add_all(todos)
    session.flush()

    for todo in todos:
        session.refresh(todo)

    return todos


@pytest.fixture
def todo(todos: list[Todo]) -> Todo:
    """Unpack one todo_ from todos"""
    return todos[0]


@pytest.fixture
def user_todos(user: User, todos: list[Todo]) -> list[Todo]:
    """Filter only main user todos"""
    return [t for t in todos if t.user_id == user.id]


@pytest.fixture
def nonuser_todos(user: User, todos: list[Todo]) -> list[Todo]:
    """Filter only not main user todos"""
    return [t for t in todos if t.user_id != user.id]
