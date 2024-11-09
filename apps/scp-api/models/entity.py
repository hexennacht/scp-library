from .base import BaseEntity
from .category import Category


class Entity(BaseEntity):
    name: str
    category_id: int
    category: Category | None