import uvicorn
from enum import Enum
from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from database.book_db import BookDb
from database.member_db import MemberDB
router=APIRouter()
book=BookDb("localhost",3306,"root","secret","library_db")
member=MemberDB("localhost",3306,"root","secret","library_db")

class Member(BaseModel):
    title:str
    author:str
    genre:str

class GenreEnum(str,Enum):
    FICTION='FICTION'
    NON_FICTION='Non-Fiction'
    SCIENCE='Science'
    HISTORY='History'
    OTHER='OTHER'

class Update(BaseModel):
    title:str | None=None
    author: str | None=None
    genre: GenreEnum | None=None
    is_available: bool | None=None
    borrowed_by_member_id:int | None=None

@router.post("/books")
def add_member(data:Member):
    data_dict=data.model_dump()
    return book.create_book(data_dict)

@router.get("/books")
def books_names():
    result=book.get_all_books()
    if not result:
        raise HTTPException(status_code=404,detail="Error the books tabel is empty there is no books to return")
    return result

@router.get("/books/{id}")
def book_by_id(id):
    result=book.get_book_by_id(id)
    if not result:
        raise HTTPException(status_code=404,detail=f"Error the book with id {id} was not found")
    return result

@router.put("/books/{id}")
def change_book_details(id:int,data:Update):
    data_dict=data.model_dump(exclude_unset=True)
    if not data_dict:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    result=book.update_book(id,data_dict)
    if not result:
        raise HTTPException(status_code=404,detail=f"Error book id {id} for update was not found")
    return {"The update is success":result}


@router.put("/books/{id}/borrow/{member_id}")
def set_book_borrow(id:int,member_id:int):
    member_total_borrows = member.increment_borrows(id, member_id)
    if member_total_borrows>3:
        raise HTTPException(status_code=400,detail="Member has reach maximum borrows")
    if not member_total_borrows:
        raise HTTPException(status_code=404, detail=f"Error the id {id} was not found cannot update borrows")
    is_member_active=member.get_member_by_id(member_id)["is_active"]
    if not is_member_active:
        raise HTTPException(status_code=400,detail="Error inactive member cannot borrow a book")
    result=book.set_available(id,"borrow",member_id)
    if not result:
        raise HTTPException(status_code=404,detail="Error book id was not found")
    return {"Changed successfully":result}


@router.put("/books/{id}/return/{member_id}")
def set_book_return(id:int,member_id:int):
    result=book.set_available(id,"return",member_id)
    if not result:
        raise HTTPException(404,"Error book id or member id was not found")

# @router.put("/books/{id}/borrow/{member_id}")
# def update_borrow(id:int,member_id:int):
#     result=member.increment_borrows(id,member_id)
#     if not result:
#         raise HTTPException(status_code=404,detail=f"Error the id {id} was not found cannot update borrows")
if __name__=="__main__":
    uvicorn.run("book_routes:app",reload=True)