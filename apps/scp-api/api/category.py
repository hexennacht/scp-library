import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import Engine, text
from models.http_response import HttpResponse
from core.database import engine
from psycopg2 import ProgrammingError
from services.impl.category import CategoryServiceImpl
from services.category import CategoryService
from models.base import FilterParams


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
routes = APIRouter()

async def autowired(db: Engine = Depends(engine)) -> CategoryService:
    return CategoryServiceImpl(db_engine=db)

@routes.get("/")
async def get(param: Annotated[FilterParams, Query()], svc: Annotated[CategoryService, Depends(autowired)]) -> HttpResponse:
    response = await svc.get_categories(param=param)

    return HttpResponse(
            data={"totalItems": response[1], "totalPage": response[2], "items": response[0]},
            code=200, 
            message="SUCCESS"
        )