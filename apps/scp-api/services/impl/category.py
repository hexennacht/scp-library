from models.base import FilterParams
from typing import Tuple
from services.category import CategoryService
from models.category import Category
from psycopg2 import ProgrammingError
from fastapi import HTTPException
from sqlalchemy import text, Engine
from core.database import engine

class CategoryServiceImpl(CategoryService):
    db: Engine

    def __init__(self, db_engine: Engine):
        self.db = db_engine

    async def get_categories(self, param: FilterParams) -> Tuple:
        print(self.db is None)

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
                id = trx.connection.execute(
                        text(f"INSERT INTO categories (name, description) VALUES ('{category.name}', '{category.description}') RETURNING id")
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
                        text(f"DELETE FROM categories WHERE id = {id}")
                    )
                trx.commit()
            except ProgrammingError as e:
                trx.rollback()
                raise HTTPException(status_code=500, detail=e.pgerror)
        trx.close()
        return True