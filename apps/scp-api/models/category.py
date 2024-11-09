from .base import BaseEntity
from dataclasses import dataclass

class Category(BaseEntity):
    name: str
    description: str | None
    