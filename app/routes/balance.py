from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.db import get_db
from app.model.owed import Owed
from app.model.user import User
from app.auth import get_token, verify_token
from sqlalchemy.orm import selectinload

router = APIRouter()


@router.get("/{user_id}")
async def get_balances(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(get_token)
):

    uid = verify_token(token)

    user = (await db.execute(
        select(User).where(User.id == uid)
    )).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    user = (await db.execute(
        select(User).where(User.id == user_id)
    )).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await db.execute(
    select(Owed)
    .options(
        selectinload(Owed.from_user),
        selectinload(Owed.to_user)
    )
    .where(
        (Owed.from_user_id == user_id) |
        (Owed.to_user_id == user_id)
    )
)

    rows = result.scalars().all()

    balances = []

    for row in rows:
        balances.append({
            "from": row.from_user.name if row.from_user else row.from_user_id,
            "to": row.to_user.name if row.to_user else row.to_user_id,
            "amount": row.amount
        })

    return {
        "balances": balances
    }