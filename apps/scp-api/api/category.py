import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy import Engine
from models.http_response import HttpResponse
from core.database import engine
from services.impl.category import CategoryServiceImpl
from services.category import CategoryService
from models.base import FilterParams
from models.category import Category


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
routes = APIRouter(prefix="/category", tags=["Category"])

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

@routes.post("/")
async def create(request: Category, svc: Annotated[CategoryService, Depends(autowired)]) -> HttpResponse:
    category = await svc.create(request)

    return HttpResponse(data=category, code=201, message="CREATED")

@routes.delete("/{id}")
async def delete(id: Annotated[int, Path(title="The id of the category")], svc: Annotated[CategoryService, Depends(autowired)]) -> HttpResponse:
    category = await svc.delete(id=id)

    return HttpResponse(data=category, code=200, message="SUCCESS")