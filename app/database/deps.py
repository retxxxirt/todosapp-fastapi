from sqlmodel import Session

from app.database.engines import engine


def get_session() -> Session:
    """Yield session with contex manager, commit before exit"""

    with Session(engine) as session:
        yield session
        session.commit()
