from fastapi import FastAPI, Depends,HTTPException,APIRouter,Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.model.user import User
from app.schema.user import UserCreate, UserLogin
from app.db import get_db
from sqlalchemy.future import select
from app.auth import generate_token,get_token,verify_token

router = APIRouter()

@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    users =( await db.execute(select(User))).scalar_one_or_none()
    return users

@router.post("/register")
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

@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    check_user= await db.execute(select(User).where(User.email==user.email))
    user_if=check_user.scalar_one_or_none()
    if not user_if:
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    
    if not user_if.verify_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    token=generate_token(user_if.id)
    return {"token": token}

@router.post("/Uname")
async def show_user(request:Request,token: str = Depends(get_token), db: AsyncSession = Depends(get_db)):
    # token=request.headers.get("authorization") #for non swagger ui
    uid=verify_token(token)
    username =await db.execute(select(User.name).where(User.id==uid))
    username=username.scalar_one_or_none()
    if not username:
        raise HTTPException(status_code=400, detail="User not found ,cheak your token")
    return {"username":username}