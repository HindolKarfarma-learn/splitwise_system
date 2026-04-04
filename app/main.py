from fastapi import FastAPI, Depends,HTTPException
from sqlalchemy.orm import Session
# import models
from app.routes import users, group, expenses
from app import models

from app.db import Base,get_db,engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router,    prefix="/users",    tags=["Users"])
app.include_router(group.router,   prefix="/groups",   tags=["Groups"])
app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])