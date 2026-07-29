from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.settings import get_settings

settings = get_settings()


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)


SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    expire_on_commit=False,
)