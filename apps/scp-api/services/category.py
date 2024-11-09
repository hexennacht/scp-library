from abc import ABC, abstractmethod
from models.base import FilterParams
from core.database import Engine
from typing import Tuple


class CategoryService(ABC):
    
    @abstractmethod
    async def get_categories(self, param: FilterParams) -> Tuple:
        pass