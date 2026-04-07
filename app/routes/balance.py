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


router =APIRouter()

@router.post("/{group_id}")
async def find_balance(group_id: int,db: AsyncSession = Depends(get_db),token: str = Depends(get_token)):
    uid = verify_token(token)

    user = (await db.execute(
        select(User).where(User.id == uid)
    )).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    group_exist = (await db.execute(
        select(user_group).where(user_group.id == group_id)
    )).scalar_one_or_none()

    if not group_exist:
        raise HTTPException(status_code=404, detail="Group not found")
    

    #make a dictionary with zipping user_id form the group and 0 dict.fromkeys(user_idlist,0)
    #  go through expences table to find payers for the given group_id 
            # add expence.ammout to in the dict
    # go through expence split atble to find amout owed 
            # substract that ammout  in the dict 

    members=(await db.execute(
        select(user_group_members.user_id)
        .where(user_group_members.group_id == group_id)
    )).scalars().all()

    balance= {user_id: 0 for user_id in members}

    expenses_done = (await db.execute(
        select(Expense).where(Expense.group_id == group_id)
    )).scalars().all()
    
    for exp in expenses_done:
        balance[exp.paid_by] += exp.amount

    splits = (await db.execute(
        select(ExpenseSplit)
        .join(Expense, ExpenseSplit.expense_id == Expense.id)
        .where(Expense.group_id == group_id)
    )).scalars().all()

    for split in splits:
        balance[split.user_id] -= split.amount_owed