from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from starlette import status

from app.database.deps import get_session
from app.users import services, crud, errors
from app.users.schemas import User

auth_scheme = HTTPBearer(scheme_name="AccessToken", bearerFormat="JWT", auto_error=False)


def get_current_user(
    session: Session = Depends(get_session),
    auth_data: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> User:
    """Get user from authorization header, raise 401 for bad values"""

    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=errors.INVALID_ACCESS_TOKEN,
    )

    if auth_data is None:
        raise error
    if (user_id := services.decode_jwt_token(auth_data.credentials)) is None:
        raise error
    if (user := crud.get_user_by_id(session, user_id)) is None:
        raise error

    return user
