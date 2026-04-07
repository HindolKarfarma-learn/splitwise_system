from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.db import Base


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    description: Mapped[str] = mapped_column(String(255))
    amount: Mapped[int] = mapped_column()

    paid_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("user_group.id"))
    
    # relationships
    group = relationship("user_group", back_populates="expenses")
    splits = relationship("ExpenseSplit", back_populates="expense")