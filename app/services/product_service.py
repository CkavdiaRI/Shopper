from app.routers import products
from app.schemas.product import ProductCreate

LOW_STOCK_LIMIT = 10

PRODUCTS = {
    1: {"id": 1, "title": "Essence Mascara Lash Princess", "price": 9.99, "stock": 99, "cost_price": 4.20},
    2: {"id": 2, "title": "Eyeshadow Palette with Mirror", "price": 19.99, "stock": 34, "cost_price": 9.50},
}


class ProductService:
    def get_by_id(self, product_id: int) -> dict | None:
        product = PRODUCTS.get(product_id)
        if product is None:
            raise ValueError(f"Product {product_id} not found")
        return self._with_flags(product) 
        # low_stock is a derived field, not stored in the database

    def _with_flags(self, product: dict):
        return {**product, "low_stock": product["stock"] < LOW_STOCK_LIMIT}