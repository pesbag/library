import uvicorn
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from database.book_db import BookDb
app=FastAPI()
book=BookDb("localhost",3306,"root","secret","library_db")

class Member(BaseModel):
    title:str
    author:str
    genre:str

class Update(BaseModel):
    title:str|None=None
    author: str|None=None
    genre: str|None=None
    is_available: bool| None=None
    borrowed_by_member_id:int| None=None

@app.post("/member")
def add_member(data:Member):
    data_dict=data.model_dump()
    return book.create_book(data_dict)

@app.get("/books")
def books_names():
    result=book.get_all_books()
    if not result:
        raise HTTPException(status_code=404,detail="Error the books tabel is empty there is no books to return")
    return result

@app.get("/books/{id}")
def book_by_id(id):
    result=book.get_book_by_id(id)
    if not result:
        raise HTTPException(status_code=404,detail=f"Error the book with id {id} was not found")
    return result

@app.put("/books/{id}")
def change_book_details(id:int,data:Update):
    data_dict=data.model_dump(exclude_unset=True)
    if not data_dict:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    result=book.update_book(id,data_dict)
    if not result:
        raise HTTPException(status_code=404,detail=f"Error book id {id} for update was not found")
    return {"The update is success":result}

@app.get("/reports/summary")
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
@app.get("/reports/books-by-genre")
def count_books_genre():
    result= book.count_by_genre()
    if not result:
        raise HTTPException(status_code=404,detail="Error any genre of book was not found")
    return {"found":result}

if __name__=="__main__":
    uvicorn.run("book_routes:app",reload=True)