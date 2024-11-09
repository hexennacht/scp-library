import logging
from models.base import FilterParams
from typing import Tuple
from services.category import CategoryService
from models.category import Category
from psycopg2 import ProgrammingError
from fastapi import HTTPException
from sqlalchemy import text, Engine
from datetime import datetime


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CategoryServiceImpl(CategoryService):
    db: Engine

    def __init__(self, db_engine: Engine):
        self.db = db_engine

    async def get_categories(self, param: FilterParams) -> Tuple:
        with self.db.connect() as connection:
            try:
                count = int(f"{connection.execute(text("select count(id) from categories")).scalar()}")
                result = connection.execute(text(f"select * from categories limit {param.limit} offset {(param.page-1)*param.limit}"))
            except ProgrammingError as e:
                raise HTTPException(status_code=500, detail=e.pgerror)
        
        data: list[Category] = []

        for row in result:
            category = Category(id=row[0], name=row[1], description=row[2], created_at=row[3], updated_at=row[4])
            data.append(category)

        total_pages = (count + param.limit - 1) // param.limit

        return (data, count, total_pages)
    
    async def create(self, category: Category) -> Category:
        with self.db.connect() as connection:
            trx = connection.begin()
            try:
                args = {"name": category.name, "description": category.description}
                id = trx.connection.execute(
                        text(f"INSERT INTO categories (name, description) VALUES (:name, :description) RETURNING id"),
                        args
                    ).scalar()
                category.id = int(f"{id}")
                trx.commit()
            except ProgrammingError as e:
                trx.rollback()
                trx.close()
                raise HTTPException(status_code=500, detail=e.pgerror)
        trx.close()
        return category
    
    async def delete(self, id: int) -> bool:
        with self.db.connect() as connection:
            trx = connection.begin()
            try:
                trx.connection.execute(
                        text(f"DELETE FROM categories WHERE id = :id"),
                        {"id": id}
                    )
                trx.commit()
            except ProgrammingError as e:
                trx.rollback()
                raise HTTPException(status_code=500, detail=e.pgerror)
        trx.close()
        return True
    
    async def update(self, category: Category) -> Category:
        old_category = await self.get_by_id(int(f"{category.id}"))

        if old_category:
            old_category.name = category.name
            old_category.description = category.description
            old_category.updated_at = datetime.now()

            category = await self.update_by_id(old_category)

        return category
    

    async def update_by_id(self, category: Category) -> Category:
        with self.db.connect() as connection:
            trx = connection.begin()
            args = {"name": category.name, "description": category.description, "id": category.id}
            try:
                trx.connection.execute(
                    text("UPDATE categories SET name = :name, description = :description WHERE id = :id"),
                    args
                )
                trx.commit()
            except ProgrammingError as e:
                trx.rollback()
                raise HTTPException(status_code=500, detail=e.pgerror)
            
        trx.close()

        return category

    async def get_by_id(self, id: int) -> Category:
        with self.db.connect() as connection:
            try:
                result = connection.execute(text("SELECT * FROM categories WHERE id = :id"), {"id": id})
            except ProgrammingError as e:
                raise HTTPException(status_code=404, detail="CATEGORY NOT FOUND")
        
        row = result.fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="CATEGORY NOT FOUND")
        
        return Category(**row._mapping)