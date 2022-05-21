from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from sqlmodel import SQLModel


def create_tables(engine: Engine):
    """Create all tables"""
    SQLModel.metadata.create_all(engine)


def drop_tables(engine: Engine):
    """Drop all tables"""
    for table in SQLModel.metadata.sorted_tables:
        if inspect(engine).has_table(table):
            table.drop(engine)
