from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar("T")

class HttpResponse(BaseModel, Generic[T]):
    data: T | None
    message: str | None
    code: int = 200
