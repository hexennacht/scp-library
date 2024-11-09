from abc import ABC, abstractmethod
from models.base import FilterParams
from models.category import Category
from typing import Tuple


class CategoryService(ABC):
    
    @abstractmethod
    async def get_categories(self, param: FilterParams) -> Tuple:
        pass

    @abstractmethod
    async def create(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def update(self, category: Category) -> Category:
        pass