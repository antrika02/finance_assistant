from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum as SQLEnum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.enums import TransactionType
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.user import User


class Transaction(TimestampMixin, Base):

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    type: Mapped[TransactionType] = mapped_column(
        SQLEnum(
            TransactionType,
            values_callable=lambda enum: [e.value for e in enum],
        ),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
    )

    transaction_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    category: Mapped["Category"] = relationship(
        back_populates="transactions",
    )

    user: Mapped["User"] = relationship(
        back_populates="transactions",
    )