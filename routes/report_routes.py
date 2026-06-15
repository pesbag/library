from fastapi import APIRouter,HTTPException
import uvicorn
router=APIRouter()
from database.book_db import BookDb
from database.member_db import MemberDB
book=BookDb("localhost",3306,"root","secret","library_db")
member=MemberDB("localhost",3306,"root","secret","library_db")

import logging
logger=logging.getLogger(__name__)

@router.get("/reports/books-by-genre")
def count_books_genre():
    logger.debug("enter to GET/reports/books-by-genre")
    logger.info("enter to count_books_genre function in report_routes file")
    result= book.count_by_genre()
    if not result:
        logger.error("Error any genre of book was not found in count_books_genre function in report_routes file")
        raise HTTPException(status_code=404,detail="Error any genre of book was not found")
    logger.debug("exit from GET/reports/books-by-genre")
    return {"found":result}

@router.get("/reports/top-member")
def top_member():
    logger.debug("enter to GET/reports/top-member")
    logger.info("enter to top_member function in report_routes file")
    logger.debug("exit from GET/reports/books-by-genre")
    return member.get_top_member()

@router.get("/reports/summary")
def get_report_summary():
    logger.debug("enter to GET/reports/summary")
    logger.info("enter to get_report_summary function in report_routes file")
    num_of_book = book.count_total_books()
    num_of_book_avail = book.count_available_books()
    num_of_book_non_avail=book.count_borrowed_books()
    if not num_of_book:
        logger.error(f"Error the book with id {num_of_book} was not found in get_report_summary function in report_routes file")
        raise HTTPException(status_code=404, detail=f"Error the book with id {num_of_book} was not found")
    logger.debug("exit from GET/reports/books-by-genre")
    return {
        "total books": num_of_book,
        "total available books": num_of_book_avail,
        "total borrowed books": num_of_book_non_avail
    }
