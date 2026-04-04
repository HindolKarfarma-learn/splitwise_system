from fastapi import FastAPI, Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
# import models
# from app.models import expenses
# from app import models
from app.models.expenses import Expenses
from app.schema.expenses import expensesCreate
from app.db import Base,get_db

router = APIRouter()

@router.post("/expenses")
def create_expenses(expenses: expensesCreate, db: Session = Depends(get_db)):
    new_expenses = Expenses(
        description=expenses.description,
        amount=expenses.amount,
        group_id=expenses.group_id,
        paid_by=expenses.paid_by
      
    )

    db.add(new_expenses)     # add to DB
    db.commit()          # save permanently
    db.refresh(new_expenses) # get updated data (like id)

    return new_expenses
