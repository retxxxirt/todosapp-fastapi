from uuid import UUID

from fastapi import Depends, Path, HTTPException
from sqlmodel import Session
from starlette import status

from app.database.deps import get_session
from app.todos import crud, errors
from app.todos.schemas import Todo
from app.users.deps import get_current_user
from app.users.schemas import User


def todo_or_404(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
    todo_id: UUID = Path(),
) -> Todo:
    """Get authorized user todo_ based on path todo_id or raise 404"""

    if (todo := crud.get_user_todo_by_id(session, user, todo_id)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=errors.TODO_NOT_FOUND,
        )

    return todo
