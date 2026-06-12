from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from database.member_db import MemberDB
member=MemberDB("localhost",3306,"root","secret","library_db")
router=APIRouter()

class AddMember(BaseModel):
    name:str
    email:str
    is_active:bool
    total_borrows:int

@router.post("/members")
def add_member(data:AddMember):
    new_data=data.model_dump()
    result=member.create_member(new_data)
    return {"created member successfully, new id is": result}
@router
