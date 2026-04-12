from fastapi import FastAPI
from app.routes import user,group,expense,balance
from app.db import engine,Base
from starlette.middleware.sessions import SessionMiddleware

app=FastAPI()

app.add_middleware(
    SessionMiddleware, 
    secret_key="your_secret_key"
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(user.router, prefix="/auth", tags=["User"])
app.include_router(group.router, prefix="/groups", tags=["Groups"])
app.include_router(expense.router, prefix="/expences", tags=["Expences"])
app.include_router(balance.router, prefix="/balance", tags=["Balance"])

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to the Splitwise app"}