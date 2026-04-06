from sqlalchemy import Column, Integer, String 
from sqlalchemy.orm import mapped_column, Mapped,relationship
import bcrypt

from app.db import Base

class User(Base):
    __tablename__="users"

    id: Mapped[int]=mapped_column(primary_key=True,index=True, autoincrement=True)
    name: Mapped[str]=mapped_column(String(50))
    email: Mapped[str]=mapped_column(String(70),unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    groups = relationship("user_group_members", back_populates="user")
    
    @property 
    def password(self):
        raise AttributeError("Password is write-only use verify_password(pssword:str)->bool to cheak for password")

    @password.setter
    def password(self, password: str):
        self.password_hash = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
    

