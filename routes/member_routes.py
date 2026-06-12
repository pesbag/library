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

@router.get("/members")
def get_members():
    result=member.get_all_members()
    if not result:
        raise HTTPException(status_code=404,detail="Error the members tabel was empty, no member founds")
    return result
