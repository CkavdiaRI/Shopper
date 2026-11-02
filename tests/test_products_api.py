from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app.db.models import Category, Product
from app.main import app
from app.routers.products import get_product_service
from app.services.product_service import ProductService


class FakeProductRepository:
    def __init__(self):
        lip_gloss = Product(id=1, title="Lip Gloss", price=Decimal("9.99"), stock=5, category=Category(name="Makeup"))

        self.products = {1: lip_gloss}

    async def get_by_id(self, product_id):
        return self.products.get(product_id)

@pytest.fixture
def client():
    app.dependency_overrides[get_product_service] = lambda: ProductService(FakeProductRepository(), None)
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_get_one_product(client):
    response = client.get("/api/v1/products/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Lip Gloss"
    assert response.json()["low_stock"] is True

def test_unknown_product_is_404(client):
    response = client.get("/api/v1/products/999")
    assert response.status_code == 404
    assert response.json()["error"]["detail"] == "Product 999 not found"

# @pytest.mark.parametrize("product_id", [0, -1])
# def test_bad_id_is_422(client):
#     response = client.get(f"/api/v1/products/{product_id}")
#     assert response.status_code == 422