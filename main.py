from fastapi import FastAPI,APIRouter
from routes import member_routes
from routes import book_routes
from database.db_connection import create_tables
app=FastAPI()
app.include_router(member_routes.router)
app.include_router(book_routes.router)
create_tables()
