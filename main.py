from fastapi import FastAPI,APIRouter
from routes import member_routes
from routes import book_routes
from routes import report_routes
import uvicorn
import logging
from database.db_connection import DbConnection
conn=DbConnection()

full_path="logs/app.log"
logging.basicConfig(
    filename=full_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app=FastAPI()
app.include_router(member_routes.router)
logging.info("include routes of members in main")
app.include_router(book_routes.router)
logging.info("include routes of book in main")
app.include_router(report_routes.router)
logging.info("include routes of report in main")
conn.create_tables()

if __name__=="__main__":
    uvicorn.run("main:app",reload=True)