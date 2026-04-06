from sqlalchemy import Column, Integer, String , ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class user_group_members(Base):
    __tablename__ = "user_group_members"

    id = Column(Integer, primary_key=True, index=True)
    u_id = Column(Integer, ForeignKey("users.id"), index=True)
    g_id = Column(Integer, ForeignKey("user_group.id"), index=True)
    user = relationship("User", back_populates="groups")
    group = relationship("user_group", back_populates="members")
 