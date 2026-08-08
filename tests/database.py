from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

# IMPORTANT: Import all ORM models BEFORE create_all()
from app.database.session import Base

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
)

print(Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
