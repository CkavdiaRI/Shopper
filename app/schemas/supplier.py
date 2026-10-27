from pydantic import BaseModel, Field
from app.schemas.product import Dimensions


class SupplierProduct(BaseModel):
    id: int
    title: str
    description: str
    category: str
    price: float
    stock: int 
    image_url: str = Field(alias="thumbnail")  # Use alias to match the JSON field name
    discount_percentage: float = Field(alias="discountPercentage")  # Use alias to match the JSON field name
    dimensions: Dimensions | None = None  # Optional field for dimensions