from sqlalchemy.engine import Engine
from sqlmodel import SQLModel


def create_tables(engine: Engine):
    """Create all tables"""
    SQLModel.metadata.create_all(engine)


def drop_tables(engine: Engine):
    """Drop all tables"""
    SQLModel.metadata.drop_all(engine)
