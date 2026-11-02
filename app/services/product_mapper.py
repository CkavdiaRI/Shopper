from app.db.models import Product

LOW_STOCK_LIMIT = 10


def to_dict(product: Product) -> dict:
        return {
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "image_url": product.image_url,
            "category": product.category.name if product.category else None,
            "low_stock": product.stock <= LOW_STOCK_LIMIT,
        }