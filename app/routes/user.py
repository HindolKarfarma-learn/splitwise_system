from fastapi import FastAPI, Depends,HTTPException,APIRouter,Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.model.user import User
from app.model.auth_model import UserCreate, UserLogin
from app.db import get_db
from sqlalchemy.future import select
from jose import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
security = HTTPBearer()


router = APIRouter()

@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await db.query(User).all()
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
async def create_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    check_user= await db.execute(select(User).where(User.email==user.email))
    user_if=check_user.scalar_one_or_none()
    if not user_if:
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    
    if not user_if.verify_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    exp=datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"id":user_if.id,"exp":exp},SECRET_KEY,ALGORITHM)

    return {"token": token}

def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return token

@router.post("/Uname")
async def create_user(request:Request,token: str = Depends(get_token), db: AsyncSession = Depends(get_db)):
    # token=request.headers.get("authorization") #for non swagger ui
    
    token=token.split(" ")[-1]
    data= jwt.decode(token,SECRET_KEY,ALGORITHM)
    print("TOKEN RECEIVED:", data)
    username =await db.execute(select(User.name).where(User.id==data.get("id")))
    username=username.scalar_one_or_none()
    return {"name":username}