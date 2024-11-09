from fastapi import APIRouter
from api import health, category

api: APIRouter = APIRouter()
api.include_router(router=health.routes, prefix="/api/v1")
api.include_router(router=category.routes, prefix="/api/v1/category")