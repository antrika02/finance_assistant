from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.enums import CategoryType
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.budget import Budget
    from app.models.transaction import Transaction
    from app.models.user import User


class Category(TimestampMixin, Base):
    """
    Represents an income or expense category.
    """

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    type: Mapped[CategoryType] = mapped_column(
        SQLEnum(
            CategoryType,
            values_callable=lambda enum: [e.value for e in enum],
        ),
        nullable=False,
    )

    icon: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    color: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    user: Mapped["User"] = relationship(
        back_populates="categories",
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
    )

    budgets: Mapped[list["Budget"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
    )
