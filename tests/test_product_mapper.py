import uuid
from decimal import Decimal

import pytest

from app.db.models import Category, Product
from app.services import product_mapper

PRODUCT_ID = uuid.UUID("11111111-1111-7111-8111-111111111111")

def make_product(stock=20, category=None):
    return Product(id=PRODUCT_ID, title="Test Product", price=Decimal("1.00"), stock=stock, category=category)


def test_low_stock():
    product = Product(id=PRODUCT_ID, title="Test Product", price=Decimal("1.00"), stock=5)
    assert product_mapper.to_dict(product)["low_stock"] is True

@pytest.mark.parametrize("stock, expected", [(10, True), (9, True), (11, False)])
def test_low_stock_boundary(stock, expected):
    product = make_product(stock=stock)
    
    assert product_mapper.to_dict(product)["low_stock"] is expected

def test_to_dict_copies_the_fields():
    # Arrange
    product = make_product(category=Category(name="Test Category"))

    # Act
    result = product_mapper.to_dict(product)

    # Assert
    assert result["id"] == PRODUCT_ID
    assert result["title"] == "Test Product"
    assert result["price"] == Decimal("1.00")
    assert result["stock"] == 20
    assert result["category"] == "Test Category"

def test_to_dict_handles_none_category():
    # Arrange
    product = make_product()

    # Act
    result = product_mapper.to_dict(product)

    # Assert
    assert result["category"] is None

