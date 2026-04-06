from sqlalchemy import Column, Integer, String , ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class user_group(Base):
    __tablename__ = "user_group"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    members = relationship("user_group_members", back_populates="group")
 