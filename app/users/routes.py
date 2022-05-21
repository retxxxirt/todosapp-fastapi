from datetime import timedelta

from fastapi import APIRouter, Depends, Body
from sqlmodel import Session

from app.common.pagination import Paginator, paginate, Page
from app.common.validation import ValidationError
from app.database.deps import get_session
from app.users import crud, services, errors
from app.users.deps import get_current_user
from app.users.schemas import (
    UserRead,
    SignIn,
    SignUp,
    UserCreate,
    User,
    UserUpdate,
    AccessToken,
    AccessTokenType,
    UserUpdatePassword,
)

auth_router = APIRouter(tags=["auth"])
users_router = APIRouter(prefix="/users", tags=["users"])
profile_router = APIRouter(prefix="/profile", tags=["profile"])


@auth_router.post("/signup", response_model=AccessToken)
def signup(
    session: Session = Depends(get_session),
    data: SignUp = Body(),
):
    """Signin route, validate username then create user and return jwt-token"""

    if crud.get_user_by_username(session, data.username) is not None:
        raise ValidationError(errors.USERNAME_TAKEN, location="username")

    user = crud.create_user(session, UserCreate(**data.dict()))
    token = services.encode_jwt_token(user.id, expire_in=timedelta(days=30))
    return {"access_token": token, "type": AccessTokenType.bearer}


@auth_router.post("/signin", response_model=AccessToken)
def signin(
    session: Session = Depends(get_session),
    data: SignIn = Body(),
):
    """Signin route, validate username and password then return jwt-token"""

    if (user := crud.get_user_by_username(session, data.username)) is None:
        raise ValidationError(errors.INVALID_CREDENTIALS)

    if not services.verify_password(data.password, user.password_hash):
        raise ValidationError(errors.INVALID_CREDENTIALS)

    token = services.encode_jwt_token(user.id, expire_in=timedelta(days=30))
    return {"access_token": token, "type": AccessTokenType.bearer}


@users_router.get(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=Page[UserRead],
)
def list_users(
    session: Session = Depends(get_session),
    paginator: Paginator = Depends(),
):
    """List users route, return paginated users list"""
    return paginate(crud.get_users(session), paginator)


@profile_router.get("/", response_model=UserRead)
def get_profile(user: User = Depends(get_current_user)):
    """Profile route, return user profile"""
    return user


@profile_router.patch("/", response_model=UserRead)
def update_profile(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
    data: UserUpdate = Body(),
):
    """Update profile route, validate username than return updated user"""

    if data.username is not None:
        if crud.get_user_by_username(session, data.username) is not None:
            raise ValidationError(errors.USERNAME_TAKEN, location="username")

    return crud.update_user(session, user, data)


@profile_router.delete("/")
def delete_profile(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Delete profile route, delete user profile"""
    crud.delete_user(session, user)


@profile_router.patch("/password")
def change_password(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
    data: UserUpdatePassword = Body(),
):
    """Change password route, validate user password than update them"""

    if not services.verify_password(data.old_password, user.password_hash):
        raise ValidationError(errors.INVALID_PASSWORD, location="password")

    crud.update_user_password(session, user, data.password)
