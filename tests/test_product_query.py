import pytest
from pydantic import ValidationError 
from app.schemas.product import ProductQuery

@pytest.mark.parametrize("size", [1, 10, 100])
def test_product_query_within_valid_limits (size):
    assert ProductQuery(size=size).size == size

@pytest.mark.parametrize("size", [0, 101, -1])
def test_product_query_outside_valid_limits(size):
    with pytest.raises(ValidationError):
        ProductQuery(size=size)

def test_page_must_be_non_negative():
    with pytest.raises(ValidationError):
        ProductQuery(page=-1)