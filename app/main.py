from fastapi import FastAPI
from app.routes import user#auth_routes
from app.db import engine
from app.model.user import User, Base
from starlette.middleware.sessions import SessionMiddleware

app=FastAPI()

app.add_middleware(
    SessionMiddleware, 
    secret_key="your_secret_key"
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(user.router, prefix="/auth", tags=["user"])
# app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to the Splitwise app"}