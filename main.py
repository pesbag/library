from fastapi import FastAPI,APIRouter
from routes import member_routes
app=FastAPI()
app.include_router(member_routes.router)
