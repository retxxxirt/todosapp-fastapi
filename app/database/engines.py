from sqlmodel import create_engine

from app.settings import settings

engine = create_engine(settings.database_url)
