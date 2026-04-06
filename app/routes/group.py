from fastapi import FastAPI, Depends,HTTPException,APIRouter,Request
from sqlalchemy.ext.asyncio import AsyncSession
# from app.models.group import user_group
# from app.models.user import User
# from app.models.group_member import user_group_members
from app.model.group import user_group
from app.model.user import User
from app.model.user_group_member import user_group_members
from app.schema.group import GroupCreate,AddMember
from app.db import get_db
from sqlalchemy.future import select
from app.auth import generate_token,get_token,verify_token

router = APIRouter()

@router.get("/{group_id}")
async def get_group(group_id:int ,db: AsyncSession = Depends(get_db),token: str = Depends(get_token)):
    uid=verify_token(token)
    userid =await db.execute(select(User.id).where(User.id==uid))
    userid=userid.scalar_one_or_none()
    if not userid:
        raise HTTPException(status_code=400, detail="Invalid token")
    result = await db.execute(select(user_group).where(user_group.id == group_id))
    result = result.scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=404, detail="Group not found")
    groups = await db.execute(
        select(User.id,User.name)
        .join(user_group_members,User.id==user_group_members.user_id)
        .where(user_group_members.group_id ==group_id)
    )
    members =[{"id": i.id, "name": i.name} for i in groups.all()]
    return {
        "group_id": result.id,
        "group_name": result.name,
        "members": members
        }


@router.post("/")
async def create_group(groups: GroupCreate, db: AsyncSession = Depends(get_db),token: str = Depends(get_token)):
    uid=verify_token(token)
    userid =await db.execute(select(User.id).where(User.id==uid))
    userid=userid.scalar_one_or_none()
    if not userid:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    new_group = user_group(
        name=groups.name,
      
    )

    db.add(new_group)     # add to DB
    await db.commit()          # save permanently
    await db.refresh(new_group) # get updated data (like id)

    return {"group_id":new_group}


@router.post("/{group_id}/add-member")
async def add_member(group_id: int, data: AddMember, db: AsyncSession = Depends(get_db),token: str = Depends(get_token)):
    uid=verify_token(token)
    userid =await db.execute(select(User.id).where(User.id==uid))
    userid=userid.scalar_one_or_none()
    if not userid:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    group = (await db.execute(select(user_group).where(user_group.id == group_id))).scalar_one_or_none()
    user = (await db.execute(select(User).where(User.id == data.user_id))).scalar_one_or_none()
    pre_mem =(await db.execute(select(user_group_members)
                               .where(user_group_members.group_id == group_id,user_group_members.user_id == data.user_id))).scalar_one_or_none()
    if not group :
        raise HTTPException(status_code=404, detail="Group Not found")
    if not user :
        raise HTTPException(status_code=404, detail="User Not found")
    if pre_mem :
        raise HTTPException(status_code=404, detail="Alredy member of the group")
    
    member = user_group_members(user_id=data.user_id,
                                group_id=group_id
    )

    db.add(member)
    await db.commit()

    return {"message": "User added to Group"}