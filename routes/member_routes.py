from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from database.member_db import MemberDB
import logging
logger=logging.getLogger(__name__)

member=MemberDB("localhost",3306,"root","secret","library_db")
router=APIRouter()

class AddMember(BaseModel):
    name:str
    email:str
    is_active:bool

class UpdateMember(BaseModel):
    name: str|None=None
    email: str|None=None
    is_active: bool|None=None

@router.post("/members")
def add_member(data:AddMember):
    logger.debug("enter to POST/members")
    logger.info("enter to add_member function in member_routes file")
    new_data=data.model_dump()
    result=member.create_member(new_data)
    if not result:
        logger.error("Error duplicate email found in add_member function in member_routes file")
        raise HTTPException(status_code=409,detail="Error duplicate email found")
    logger.debug("exit from POST/members")
    return {"created member successfully, new id is": result}

@router.get("/members")
def get_members():
    logger.debug("enter to GET/members")
    logger.info("enter to get_member function in member_routes file")
    result=member.get_all_members()
    if not result:
        logger.error("Error the members tabel was empty, no member founds in get_member function in member_routes file")
        raise HTTPException(status_code=404,detail="Error the members tabel was empty, no member founds")
    logger.debug("exit from GET/members")
    return result

@router.get("/members/{id}")
def get_by_id(id:int):
    logger.debug("enter to GET/members/{id}")
    logger.info("enter to get_by_id function in member_routes file")
    result=member.get_member_by_id(id)
    if not result:
        logger.error(f"Error the member id {id} was not found in get_by_id function in member_routes file")
        raise HTTPException(status_code=404,detail=f"Error the member id {id} was not found")
    logger.debug("exit from GET/members/{id}")
    return {f"The member by {id} is ":result}

@router.put("/members/{id}")
def update_fields(id:int, data:UpdateMember):
    logger.debug("enter to PUT/members/{id}")
    logger.info("enter to update_fields function in member_routes file")
    new_data=data.model_dump(exclude_unset=True)
    result=member.update_member(id,new_data)
    if not result:
        logger.error("Error duplicate email found or another problem in updating data in member_routes file")
        raise HTTPException(status_code=409, detail="Error duplicate email found or another problem in updating data")
    logger.debug("exit from PUT/members/{id}")
    return{f"Successfully changed {result} items"}

@router.put("/members/{id}/deactivate")
def deactivate(id:int):
    logger.debug("enter to PUT/members/{id}/deactivate")
    logger.info("enter to deactivate function in member_routes file")
    result=member.deactivate_member(id)
    if not result:
        logger.error(f"Error the member {id} was not found in deactivate function in member_routes file")
        raise HTTPException(status_code=404,detail=f"Error the member {id} was not found")
    logger.debug("exit from PUT/members/{id}/deactivate")
    return result
@router.put("/members/{id}/activate")
def activate(id:int):
    logger.debug("enter to PUT/members/{id}/activate")
    logger.info("enter to activate function in member_routes file")
    result = member.activate_member(id)
    if not result:
        logger.error("enter to activate function in member_routes file")
        raise HTTPException(status_code=404, detail=f"Error the member {id} was not found")
    logger.debug("exit from PUT/members/{id}/deactivate")
    return result