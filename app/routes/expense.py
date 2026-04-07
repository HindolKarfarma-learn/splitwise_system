# from fastapi import Depends, HTTPException, APIRouter
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# from app.schema.expenses import expensesCreate
# from app.db import get_db
from app.auth import get_token, verify_token
from app.model.expence_split import ExpenseSplit
from app.model.group import user_group
from app.model.user import User
from app.model.user_group_member import user_group_members 




from fastapi import Depends,HTTPException,APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
# import models
# from app.models import expenses
# from app import models
from app.model.expense import Expense
from app.schema.expenses import expensesCreate
from app.db import Base,get_db

router = APIRouter()


@router.post("/")
async def create_expenses(
    expenseschema: expensesCreate,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(get_token),
):
    uid = verify_token(token)

    user = (await db.execute(
        select(User).where(User.id == uid)
    )).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    group_exist = (await db.execute(
        select(user_group).where(user_group.id == expenseschema.group_id)
    )).scalar_one_or_none()

    if not group_exist:
        raise HTTPException(status_code=404, detail="Group not found")

    payer = (await db.execute(
        select(User).where(User.id == expenseschema.paid_by)
    )).scalar_one_or_none()

    if not payer:
        raise HTTPException(status_code=404, detail="Payer not found")

    payer_in_group = (await db.execute(
        select(user_group_members).where(
            user_group_members.group_id == expenseschema.group_id,
            user_group_members.user_id == expenseschema.paid_by
        )
    )).scalar_one_or_none()

    if not payer_in_group:
        raise HTTPException(status_code=400, detail="Payer not in group")

    ##add exp=sum(splits.ammount) cheak

    new_expense = Expense(
        description=expenseschema.description,
        amount=expenseschema.amount,
        group_id=expenseschema.group_id,
        paid_by=expenseschema.paid_by
    )

    db.add(new_expense)
    await db.flush()

    for split in expenseschema.splits:
        db.add(ExpenseSplit(
            expense_id=new_expense.id,
            user_id=split.user_id,
            amount_owed=split.ammount
        ))

    await db.commit()

    return {
        "message": "Expense created",
        "expense_id": new_expense.id
    }