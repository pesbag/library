import uvicorn
from enum import Enum
from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from database.book_db import BookDb
from database.member_db import MemberDB
import logging
logger=logging.getLogger(__name__)

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
    logger.debug("enter to rest GET/boobs")
    logger.info("enter to add_member function to create a new book in book_routes file")
    data_dict=data.model_dump()
    logger.debug("exit from rest GET/boobs")
    return book.create_book(data_dict)

@router.get("/books")
def books_names():
    logger.debug("enter to rest GET/boobs")
    logger.info("enter to books_names function to get all the books names in book_routes file")
    result=book.get_all_books()
    if not result:
        logger.error("Error the books tabel is empty there is no books to return")
        raise HTTPException(status_code=404,detail="Error the books tabel is empty there is no books to return")
    logger.debug("exit from rest GET/boobs")
    return result

@router.get("/books/{id}")
def book_by_id(id):
    logger.debug("enter to rest GET/books/{id}")
    logger.info("enter to book_by_id function to get a specific book in book_routes file")
    result=book.get_book_by_id(id)
    if not result:
        logger.error(f"Error the book with id {id} was not found")
        raise HTTPException(status_code=404,detail=f"Error the book with id {id} was not found")
    logger.debug("exit from rest GET/books/{id}")
    return result

@router.put("/books/{id}")
def change_book_details(id:int,data:Update):
    logger.debug("enter to rest PUT/books/{id}")
    logger.info("enter to change_book_details function in book_routes")
    data_dict=data.model_dump(exclude_unset=True)
    if not data_dict:
        logger.error("No fields provided for update in change_book_details in book_routes file")
        raise HTTPException(status_code=400, detail="No fields provided for update")
    result=book.update_book(id,data_dict)
    if not result:
        logger.error(f"Error book id {id} for update was not found in change_book_details in book_routes file")
        raise HTTPException(status_code=404,detail=f"Error book id {id} for update was not found")
    logger.debug("exit from rest PUT/books/{id}")
    return {"The update is success":result}

@router.put("/books/{id}/borrow/{member_id}")
def set_book_borrow(id: int, member_id: int):
    logger.debug("enter to rest PUT/books/{id}/borrow/{member_id}")
    logger.info("enter to set_book_borrow function in book_routes")
    try:
        get_member = member.get_member_by_id(member_id)
        if not get_member:
            logger.error("Member not found in set_book_borrow function in book_routes file")
            raise HTTPException(status_code=404, detail="Member not found")
        if not get_member["is_active"]:
            logger.error("Inactive member cannot borrow a book in set_book_borrow function in book_routes file")
            raise HTTPException(status_code=400, detail="Inactive member cannot borrow a book")
        if get_member["total_borrows"]>2:
            logger.error("Member has reached maximum borrows in set_book_borrow function in book_routes file")
            raise HTTPException(status_code=400, detail="Member has reached maximum borrows")
        result = book.set_available(id, "borrow", member_id)
        if not result:
            logger.error(f"Book id {id} was not found or is already borrowed in set_book_borrow function in book_routes file")
            raise HTTPException(status_code=404, detail=f"Book id {id} was not found or is already borrowed")
        member.increment_borrows(id, member_id)
        logger.debug("exit from rest PUT/books/{id}/borrow/{member_id}")
        return {"message": "Changed successfully"}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logger.error(f"Internal Server Error: {str(e)} in set_book_borrow function in book_routes file")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.put("/books/{id}/return/{member_id}")
def set_book_return(id:int,member_id:int):
    logger.debug("enter to rest PUT/books/{id}/return/{member_id}")
    logger.info("Enter to set_book_return function in book_routes file")
    result=book.set_available(id,"return",member_id)
    if not result:
        logger.error("Error book id or member id was not found in book_routes file")
        raise HTTPException(404,"Error book id or member id was not found")
    logger.debug("exit from rest PUT/books/{id}/return/{member_id}")
    return {"return book successfully":result}

if __name__=="__main__":
    uvicorn.run("book_routes:app",reload=True)