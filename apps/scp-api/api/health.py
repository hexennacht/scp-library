from fastapi import APIRouter, HTTPException, Depends
from core.database import engine
from sqlalchemy import text, Engine
from models.user import User
from models.http_response import HttpResponse
import logging
from typing import Annotated
from psycopg2 import ProgrammingError


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
routes = APIRouter()

@routes.get("/_health")
async def health(db: Annotated[Engine, Depends(engine)]) -> HttpResponse:
    with db.connect() as connection:
        try:
            query = text("select * from users")
            result = connection.execute(query)
        except ProgrammingError as e:
            logger.debug(f"got an error {e}")
            raise HTTPException(status_code=500, detail={"code": e.pgcode, "errors": e.pgerror})
        
    data: list[User] = []
    for row in result:
        data.append(User(id=int(row[0]), username=row[1]))

    logger.debug(f"{data}")

    return HttpResponse(code=200, message="SUCCESS", data=data);