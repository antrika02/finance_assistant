from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class User(Base):
    """
    Represents an application user.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )