from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Float, UniqueConstraint
from app.db import Base

class ExpenseSplit(Base):
    __tablename__ = "expense_split"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    expense_id: Mapped[int] = mapped_column(ForeignKey("expenses.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    amount_owed: Mapped[float] = mapped_column(Float)

    __table_args__ = (
        UniqueConstraint("expense_id", "user_id"),
    )

    expense = relationship("Expense", back_populates="splits")
    user = relationship("User", back_populates="expense_splits")