from pydantic import BaseModel, Field


class Dimensions(BaseModel):
    width : float
    height : float
    depth : float

class ProductCreate(BaseModel):
    title: str = Field(min_length=3)    
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    cost_price: float = Field(gt=0)
    dimensions: Dimensions | None = None

class ProductOut(BaseModel):
    id: int
    title: str
    price: float
    stock: int
    dimensions: Dimensions | None = None
    low_stock: bool