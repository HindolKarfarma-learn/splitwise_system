from fastapi import FastAPI, Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
# import models
from app.models.group import user_group
from app.models.user import User
from app.models.group_member import user_group_members
from app.schema.group import groupCreate,AddMember
from app.db import Base,get_db

router = APIRouter()

@router.get("/groups")
def get_group(db: Session = Depends(get_db)):
    groups = db.query(user_group).all()
    members = db.query(User).all()
    # return [groups,members]
    return {"groups":groups,"members":members}

@router.post("/groups")
def create_group(groups: groupCreate, db: Session = Depends(get_db)):
    new_group = user_group(
        name=groups.name,
      
    )

    db.add(new_group)     # add to DB
    db.commit()          # save permanently
    db.refresh(new_group) # get updated data (like id)

    return new_group
@router.post("/groups/{group_id}/add-member")
def add_member(group_id: int, data: AddMember, db: Session = Depends(get_db)):

    group = db.query(user_group).filter(user_group.id == group_id).first()
    user = db.query(User).filter(User.id == data.user_id).first()

    if not group or not user:
        raise HTTPException(status_code=404, detail="Not found")

    # group.members.append(user)
    # db.commit()
    member = user_group_members(
    user=user,
    group=group
)

    db.add(member)
    db.commit()

    return {"message": "User added"}