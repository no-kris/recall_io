from fastapi import APIRouter

from app.routes.notes import router as notes_router
from app.routes.users import router as users_router

api_router = APIRouter()

api_router.include_router(users_router)
api_router.include_router(notes_router)
