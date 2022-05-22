from sqlmodel import Session
from starlette import status
from starlette.testclient import TestClient

from app.todos.schemas import Todo
from app.users.schemas import User
from tests._utils import make_request


def test_list_todos(client: TestClient, user_todos: list[Todo]):
    response, response_data = make_request(client, "get", "/todos/")

    assert response.status_code == status.HTTP_200_OK
    assert response_data["count"] == len(user_todos)

    for todo, todo_data in zip(user_todos, response_data["items"]):
        assert str(todo.id) == todo_data["id"]


def test_create_todo(client: TestClient, session: Session, user: User):
    data = {"title": "New todo", "description": "Todo description"}
    response, response_data = make_request(client, "post", "/todos/", data)

    assert response.status_code == status.HTTP_200_OK
    assert response_data["title"] == "New todo"

    todo = session.query(Todo).where(Todo.id == response_data["id"]).first()

    assert isinstance(todo, Todo)
    assert todo.user_id == user.id


def test_update_todo(client: TestClient, session: Session, todo: Todo):
    data = {"title": (modified_title := f"modified: {todo.title}")}
    response, response_data = make_request(client, "patch", f"/todos/{todo.id}", data)

    assert response.status_code == status.HTTP_200_OK
    assert response_data["title"] == modified_title

    session.refresh(todo)
    assert todo.title == modified_title


def test_delete_todo(client: TestClient, session: Session, todo: Todo):
    response, response_data = make_request(client, "delete", f"/todos/{todo.id}")

    assert response.status_code == status.HTTP_200_OK
    assert session.query(Todo).get(todo.id) is None
