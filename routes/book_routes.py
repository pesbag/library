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

if __name__=="__main__":
    uvicorn.run("book_routes:app",reload=True)