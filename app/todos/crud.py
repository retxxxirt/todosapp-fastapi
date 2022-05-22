from typing import Iterable
from uuid import UUID

from sqlalchemy.orm import Query
from sqlmodel import Session, select

from app.todos.schemas import TodoCreate, Todo, TodoUpdate, TodosFilter
from app.users.schemas import User


def get_user_todo_by_id(session: Session, user: User, todo_id: UUID) -> Todo | None:
    """Get todo_ by user and todo_id"""
    request = select(Todo).join(User).where(Todo.id == todo_id, Todo.user_id == user.id)
    return session.exec(request).first()


def get_user_todos(session: Session, user: User) -> Query | Iterable[Todo]:
    """Get user todos query"""
    return session.query(Todo).join(User).where(Todo.user_id == user.id)


def create_user_todo(session: Session, user: User, data: TodoCreate) -> Todo:
    """Create todo_ for user"""
    return Todo.create(session, user_id=user.id, **data.dict())


def update_todo(session: Session, todo: Todo, data: TodoUpdate) -> Todo:
    """Update todo_ partially"""
    return todo.update(session, **data.dict(exclude_unset=True))[0]


def delete_todo(session: Session, todo: Todo):
    """Delete todo_"""
    todo.delete(session)


def filter_todos(todos: Query | Iterable[Todo], filter: TodosFilter) -> Query | Iterable[Todo]:
    """Filter todos with TodosFilter"""

    if filter.is_completed is not None:
        todos = todos.where(Todo.is_completed == filter.is_completed)
    if filter.remind_at_from is not None:
        todos = todos.where(Todo.remind_at >= filter.remind_at_from)
    if filter.remind_at_to is not None:
        todos = todos.where(Todo.remind_at <= filter.remind_at_to)

    ordering_field = getattr(Todo, filter.order_by)
    order_by_clause = getattr(ordering_field, filter.ordering)().nullslast()

    return todos.order_by(order_by_clause)
