import uuid
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app.db.models import Category, Product
from app.main import app
from app.routers.products import get_product_service
from app.services.product_service import ProductService

PRODUCT_ID = uuid.UUID("11111111-1111-7111-8111-111111111111")
UNKNOWN_ID = uuid.UUID("99999999-9999-7999-8999-999999999999")


class FakeProductRepository:
    def __init__(self):
        lip_gloss = Product(id=PRODUCT_ID, title="Lip Gloss", price=Decimal("9.99"), stock=5, category=Category(name="Makeup"))

        self.products = {PRODUCT_ID: lip_gloss}

    async def get_by_id(self, product_id):
        return self.products.get(product_id)

@pytest.fixture
def client():
    app.dependency_overrides[get_product_service] = lambda: ProductService(FakeProductRepository(), None)
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_get_one_product(client):
    response = client.get(f"/api/v1/products/{PRODUCT_ID}")
    assert response.status_code == 200
    assert response.json()["id"] == str(PRODUCT_ID)
    assert response.json()["title"] == "Lip Gloss"
    assert response.json()["low_stock"] is True

def test_unknown_product_is_404(client):
    response = client.get(f"/api/v1/products/{UNKNOWN_ID}")
    assert response.status_code == 404
    assert response.json()["error"]["detail"] == f"Product {UNKNOWN_ID} not found"

@pytest.mark.parametrize("product_id", ["0", "not-a-uuid"])
def test_bad_id_is_422(client, product_id):
    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 422