from sqlalchemy import Column, Integer, String , ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String(255), nullable=False)
    groups = relationship("user_group_members", back_populates="user")
