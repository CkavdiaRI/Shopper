from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Category


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, name: str) -> Category:
        result = await self.session.scalars(select(Category).where(Category.name == name))
        category = result.one_or_none()
        if category is None:
            category = Category(name=name)
            self.session.add(category)
        return category
