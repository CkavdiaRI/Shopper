from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class Dimensions(BaseModel):
    width: float
    height: float
    depth: float


class ProductCreate(BaseModel):
    title: str = Field(min_length=3)
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0)
    category: str | None = None


class ProductOut(BaseModel):
    id: int
    title: str
    price: Decimal
    stock: int
    low_stock: bool
    description: str | None = None
    category: str | None = None
    image_url: str | None = None
    discount_percentage: float | None = None
    dimensions: Dimensions | None = None


class ProductQuery(BaseModel):
    page: int = Field(default=0, ge=0)
    size: int = Field(default=10, ge=1, le=100)
    sort_by: Literal["id", "title", "price", "stock"] = "id"
    order: Literal["asc", "desc"] = "asc"
    keyword: str | None = None
    min_price: Decimal | None = Field(default=None, ge=0)
    max_price: Decimal | None = Field(default=None, ge=0)


class PitchOut(BaseModel):
    product_id: int
    notification: str
