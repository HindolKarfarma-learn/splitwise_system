from fastapi import FastAPI, Depends,HTTPException,APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.model.user import User
from app.model.auth_model import UserCreate, UserLogin
from app.db import get_db
from sqlalchemy.future import select
router = APIRouter()

@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await db.query(User).all()
    return users

@router.post("/users")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    check_user= await db.execute(select(User).where(User.email==user.email))
    user_if=check_user.scalar_one_or_none()
    if user_if:
        raise HTTPException(status_code=400, detail="User Exists")
    new_user = User(
        name=user.username,
        email=user.email,
        password=user.password
    )

    db.add(new_user)     # add to DB
    await db.commit()          # save permanently
    return HTTPException(status_code=200, detail="User Created")
