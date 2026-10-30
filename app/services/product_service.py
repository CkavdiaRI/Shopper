from app.core.errors import ProductNotFoundError
from app.db.models import Product
from app.schemas.product import ProductCreate, ProductQuery

LOW_STOCK_LIMIT = 10


class ProductService:
    def __init__(self, repo, categories):
        self.repo = repo
        self.categories = categories

    async def get_by_id(self, product_id: int) -> dict:
        product = await self.repo.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(f"Product {product_id} not found")
        return self._to_dict(product)

    async def list_products(self, query: ProductQuery) -> list[dict]:
        products = await self.repo.search(query)
        return [self._to_dict(p) for p in products]

    async def create(self, data: ProductCreate) -> dict:
        category = None
        if data.category:
            category = await self.categories.get_or_create(data.category)
        product = Product(title=data.title, price=data.price, stock=data.stock, category=category)
        await self.repo.add(product)
        return self._to_dict(product)

    def _to_dict(self, product: Product) -> dict:
        return {
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "image_url": product.image_url,
            "category": product.category.name if product.category else None,
            "low_stock": product.stock < LOW_STOCK_LIMIT,
        }
