from fastapi import FastAPI

from app.users.routes import auth_router, users_router, profile_router
from utils._sqlmodel import fix_inherit_cache_warning

fix_inherit_cache_warning()

app = FastAPI(
    redoc_url=None,
    swagger_ui_parameters={
        "tryItOutEnabled": True,
        "persistAuthorization": True,
    },
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(profile_router)
