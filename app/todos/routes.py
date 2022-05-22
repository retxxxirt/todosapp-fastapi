from fastapi import APIRouter, Depends, Body
from sqlmodel import Session

from app.common.pagination import Page, Paginator, paginate
from app.database.deps import get_session
from app.todos import crud
from app.todos.deps import todo_or_404
from app.todos.schemas import TodoRead, TodoCreate, TodoUpdate, Todo, TodosFilter
from app.users.deps import get_current_user
from app.users.schemas import User

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=Page[TodoRead])
def list_todos(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
    filter: TodosFilter = Depends(),
    paginator: Paginator = Depends(),
):
    """Return filtered and paginated todos"""

    todos = crud.get_user_todos(session, user)
    todos = crud.filter_todos(todos, filter)

    return paginate(todos, paginator)


@router.post("/", response_model=TodoRead)
def create_todo(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
    data: TodoCreate = Body(),
):
    """Return created todo_"""
    return crud.create_user_todo(session, user, data)


@router.patch("/{todo_id}", response_model=TodoRead)
def update_todo(
    session: Session = Depends(get_session),
    todo: Todo = Depends(todo_or_404),
    data: TodoUpdate = Body(),
):
    """Return updated todo_"""
    return crud.update_todo(session, todo, data)


@router.delete("/{todo_id}")
def delete_todo(
    session: Session = Depends(get_session),
    todo: Todo = Depends(todo_or_404),
):
    """Delete todo_"""
    crud.delete_todo(session, todo)
