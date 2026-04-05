from fastapi import Depends,HTTPException
from jose import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
security = HTTPBearer()


def generate_token(userid:str)->str:
    """
    intput:pass the id :str
    output:get the token :str
    """
    exp=datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"id":userid,"exp":exp},SECRET_KEY,ALGORITHM)
    return token


def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)):# for swagger for some reason
    token = credentials.credentials
    return token
def verify_token(full_token:str):
    """
    input : full token taken from the header :str
    output: user id :str
    """
    token=full_token.split(" ")[-1]
    data= jwt.decode(token,SECRET_KEY,ALGORITHM)
    if data.get("exp")<datetime.now().timestamp():
        raise HTTPException(status_code=400, detail="Login Timeout")
    return data.get("id")
    