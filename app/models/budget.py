from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.user import User


class Budget(TimestampMixin, Base):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    amount: Mapped[float]

    month: Mapped[int]

    year: Mapped[int]

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user: Mapped["User"] = relationship(
        back_populates="budgets",
    )

    category: Mapped["Category"] = relationship(
        back_populates="budgets",
    )
