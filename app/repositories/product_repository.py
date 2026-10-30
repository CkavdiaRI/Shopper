from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Product
from app.schemas.product import ProductQuery


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, product_id: int) -> Product | None:
        return await self.session.get(Product, product_id, options=[selectinload(Product.category)])

    async def search(self, query: ProductQuery) -> list[Product]:
        stmt = select(Product).options(selectinload(Product.category))
        if query.keyword:
            stmt = stmt.where(Product.title.ilike(f"%{query.keyword}%"))
        if query.min_price is not None:
            stmt = stmt.where(Product.price >= query.min_price)
        if query.max_price is not None:
            stmt = stmt.where(Product.price <= query.max_price)
        column = getattr(Product, query.sort_by)
        if query.order == "desc":
            column = column.desc()
        stmt = stmt.order_by(column, Product.id).limit(query.size).offset(query.page * query.size)
        result = await self.session.scalars(stmt)
        return list(result)

    async def add(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.commit()
        return product
