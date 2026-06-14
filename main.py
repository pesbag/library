from fastapi import FastAPI,APIRouter
from routes import member_routes
from routes import book_routes
from routes import report_routes
import uvicorn
from database.db_connection import create_tables
app=FastAPI()
app.include_router(member_routes.router)
app.include_router(book_routes.router)
app.include_router(report_routes.router)
create_tables()


if __name__=="__main__":
    uvicorn.run("main:app",reload=True)