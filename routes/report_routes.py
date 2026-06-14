from fastapi import APIRouter,HTTPException
import uvicorn
router=APIRouter()
from database.book_db import BookDb
from database.member_db import MemberDB
book=BookDb("localhost",3306,"root","secret","library_db")
member=MemberDB("localhost",3306,"root","secret","library_db")

@router.get("/reports/books-by-genre")
def count_books_genre():
    result= book.count_by_genre()
    if not result:
        raise HTTPException(status_code=404,detail="Error any genre of book was not found")
    return {"found":result}

@router.get("/reports/top-member")
def top_member():
    return member.get_top_member()

@router.get("/reports/summary")
def get_report_summary():
    num_of_book = book.count_total_books()
    num_of_book_avail = book.count_available_books()
    num_of_book_non_avail=book.count_borrowed_books()
    if not num_of_book:
        raise HTTPException(status_code=404, detail=f"Error the book with id {id} was not found")
    return {
        "total books": num_of_book,
        "total available books": num_of_book_avail,
        "total borrowed books": num_of_book_non_avail
    }
