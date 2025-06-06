from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from paido_core.core.settings import Settings

engine = create_engine(Settings().DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():  # pragma: no cover
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
