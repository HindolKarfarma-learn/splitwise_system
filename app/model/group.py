from sqlalchemy import Integer, String 
from sqlalchemy.orm import mapped_column, Mapped,relationship
from app.db import Base

class user_group(Base):
    __tablename__ = "user_group"

    id: Mapped[int] = mapped_column(primary_key=True,index=True, autoincrement=True)
    name: Mapped[str]= mapped_column(String(50))
    members = relationship("user_group_members", back_populates="group")
    expenses = relationship("Expense", back_populates="group")