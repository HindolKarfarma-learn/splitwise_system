from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey
from app.db import Base

class user_group_members(Base):
    __tablename__ = "user_group_members"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("user_group.id"), primary_key=True)

    user = relationship("User", back_populates="groups")
    group = relationship("user_group", back_populates="members")