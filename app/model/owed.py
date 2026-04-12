from sqlalchemy import Integer, String ,ForeignKey, UniqueConstraint

from sqlalchemy.orm import mapped_column, Mapped,relationship
from app.db import Base



class Owed(Base):
    __tablename__ = "owed"

    id: Mapped[int] = mapped_column(primary_key=True)

    from_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    to_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    amount: Mapped[float] = mapped_column(default=0)

    __table_args__ = (
        UniqueConstraint("from_user_id", "to_user_id"),
    )

    from_user: Mapped["User"] = relationship(foreign_keys=[from_user_id])
    to_user: Mapped["User"] = relationship(foreign_keys=[to_user_id])
    