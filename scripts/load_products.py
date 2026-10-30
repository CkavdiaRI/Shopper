import asyncio

import httpx

from app.core.config import settings
from app.db.database import SessionLocal, engine
from app.db.models import Product
from app.repositories.category_repository import CategoryRepository
from app.schemas.supplier import SupplierProduct


async def main():
    engine.echo = False
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.supplier_base_url}/products?limit=0")
    items = response.json()["products"]
    async with SessionLocal() as session:
        categories = CategoryRepository(session)
        for raw in items:
            item = SupplierProduct.model_validate(raw)
            category = await categories.get_or_create(item.category)
            session.add(Product(title=item.title, description=item.description,
                                price=item.price, stock=item.stock, category=category))
        await session.commit()
    print("Loaded", len(items), "products")


asyncio.run(main())
