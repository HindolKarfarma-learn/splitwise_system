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



from app.model.owed import Owed 
from fastapi import Depends,HTTPException,APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
# import models
# from app.models import expenses
# from app import models
from app.model.expense import Expense
from app.schema.expenses import expensesCreate
from app.db import Base,get_db

router = APIRouter()

async def update_balance(db, debtor_id: int, creditor_id: int, amount: float):
    if debtor_id == creditor_id:
        return

    reverse = (await db.execute(
        select(Owed).where(
            Owed.from_user_id == creditor_id,
            Owed.to_user_id == debtor_id
        )
    )).scalar_one_or_none()

    if reverse:
        if reverse.amount > amount:
            reverse.amount -= amount
        elif reverse.amount < amount:
            new_amount = amount - reverse.amount
            await db.delete(reverse)

            db.add(Owed(
                from_user_id=debtor_id,
                to_user_id=creditor_id,
                amount=new_amount
            ))
        else:
            await db.delete(reverse)
    else:
        existing = (await db.execute(
            select(Owed).where(
                Owed.from_user_id == debtor_id,
                Owed.to_user_id == creditor_id
            )
        )).scalar_one_or_none()

        if existing:
            existing.amount += amount
        else:
            db.add(Owed(
                from_user_id=debtor_id,
                to_user_id=creditor_id,
                amount=amount
            ))


@router.post("/")
async def create_expenses(
    expenseschema: expensesCreate,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(get_token)
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
        await update_balance(
        db,
        debtor_id=split.user_id,
        creditor_id=expenseschema.paid_by,
        amount=split.ammount
        )

    await db.commit()

    return {
        "message": "Expense created",
        "expense_id": new_expense.id
    }