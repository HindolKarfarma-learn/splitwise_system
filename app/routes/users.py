from fastapi import FastAPI, Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
# import models
from app.models.user import User
from app.schema.user import UserCreate
from app.db import Base,get_db

router = APIRouter()

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password
    )

    db.add(new_user)     # add to DB
    db.commit()          # save permanently
    db.refresh(new_user) # get updated data (like id)

    return new_user