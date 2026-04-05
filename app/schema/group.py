from pydantic import BaseModel
class groupCreate(BaseModel):
    name: str
   
class AddMember(BaseModel):
    user_id: int