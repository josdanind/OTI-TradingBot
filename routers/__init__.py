from config import APP_VERSION
from fastapi import APIRouter
from .users.router import router as users_router

api = APIRouter(prefix=f"/api/v{APP_VERSION}")
api.include_router(users_router)
