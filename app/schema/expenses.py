from pydantic import BaseModel
class expensesCreate(BaseModel):
    description: str
    amount:int
    group_id:int
    paid_by:int