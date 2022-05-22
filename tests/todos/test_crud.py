import uuid
from datetime import datetime

from sqlmodel import Session

from app.todos import crud
from app.todos.schemas import Todo, TodoCreate, TodoUpdate, TodosFilter
from app.users.schemas import User


def test_get_user_todo_by_id(session: Session, user: User, todo: Todo):
    assert crud.get_user_todo_by_id(session, user, todo.id).id == todo.id


def test_get_user_todo_by_id_nonexistent(session: Session, user: User):
    assert crud.get_user_todo_by_id(session, user, uuid.uuid4()) is None


def test_get_user_todo_by_id_invalid_user(session: Session, user: User, nonuser_todos: list[Todo]):
    assert crud.get_user_todo_by_id(session, user, nonuser_todos[0].id) is None


def test_get_user_todos(session: Session, user: User, user_todos: list[Todo]):
    todos = crud.get_user_todos(session, user)
    assert todos.count() == len(user_todos)

    for todo, user_todo in zip(todos, user_todos):
        assert todo.id == user_todo.id


def test_create_user_todo(session: Session, user: User):
    data = TodoCreate(title="New todo", description="Todo description")
    todo = crud.create_user_todo(session, user, data)

    assert todo.title == "New todo"
    assert todo.user_id == user.id


def test_update_todo(session: Session, todo: Todo):
    data = TodoUpdate(title=(modified_title := f"modified: {todo.title}"))
    todo = crud.update_todo(session, todo, data)

    assert todo.title == modified_title


def test_delete_todo(session: Session, todo: Todo):
    crud.delete_todo(session, todo)
    assert session.query(User).get(todo.id) is None


def test_filter_todos(session: Session, user: User, todos: list[Todo]):
    todos_query = session.query(Todo).join(User).where(Todo.user_id == user.id)
    filtered_query = crud.filter_todos(todos_query, TodosFilter(is_completed=True))

    assert filtered_query.count() > 0

    for todo in filtered_query:
        assert todo.is_completed

    filter = TodosFilter(remind_at_from=datetime.utcnow())
    filtered_query = crud.filter_todos(todos_query, filter)

    assert filtered_query.count() > 0

    for todo in filtered_query:
        assert todo.remind_at > datetime.utcnow()
