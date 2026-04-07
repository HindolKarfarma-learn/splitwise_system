from pydantic import BaseModel
from typing import List

class SP(BaseModel):
    user_id: int
    ammount: int
class expensesCreate(BaseModel):
    description: str
    amount:int
    group_id:int
    paid_by:int
    splits:List[SP]