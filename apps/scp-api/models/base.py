from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class BaseEntity(BaseModel):
    id: int | None = None
    created_at: datetime | str | None = None
    updated_at: datetime | str | None = None

    class Config:
        # This allows the BaseEntity fields to be inherited in child classes
        arbitrary_types_allowed = True
        from_attributes = True

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    page: int = Field(1, gt=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"