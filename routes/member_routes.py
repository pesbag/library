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
class UpdateMember(BaseModel):
    name: str|None=None
    email: str|None=None
    is_active: bool|None=None
    total_borrows: int|None=None

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

@router.get("/members/{id}")
def get_by_id(id:int):
    result=member.get_member_by_id(id)
    # if not result:
    #     raise HTTPException(status_code=404,detail=f"Error the member id {id} was not found")
    return {f"The member by {id} is ":result}

@router.put("/members/{id}")
def update_fields(id:int, data:UpdateMember):
    new_data=data.model_dump(exclude_unset=True)
    result=member.update_member(id,new_data)
    if not result:
        return {"Error in update, number of items that change":result}
    return{f"Successfully changed {result} items"}

@router.put("/members/{id}/deactivate")
def deactivate(id:int):
    result=member.deactivate_member(id)
    if not result:
        raise HTTPException(status_code=404,detail=f"Error the member {id} was not found")
    return result
@router.put("/members/{id}/activate")
def activate(id:int):
    result = member.activate_member(id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Error the member {id} was not found")
    return result

@router.put("/books/{id}/borrow/{member_id}")
def update_borrow(id:int,member_id):
    result=member.increment_borrows(id)
    if not result:
        raise HTTPException(status_code=404,detail=f"Error the id {id} was not found cannot update borrows")
    return result

@router.get("/reports/summary")
def count_active():
    return member.count_active_members()

@router.get("/reports/top-member")
def top_member():
    return member.get_top_member()