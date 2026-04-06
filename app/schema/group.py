from pydantic import BaseModel
class GroupCreate(BaseModel):
    name: str
   
class AddMember(BaseModel):
    user_id: int