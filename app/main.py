import asyncio
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException

app = FastAPI() # Creates an instance of FastAPI class, which is the main entry point for the application

PRODUCTS = {
    1: {"id": 1, "title": "Essence Mascara Lash Princess", "price": 9.99, "stock": 99, "cost_price": 4.20},
    2: {"id": 2, "title": "Eyeshadow Palette with Mirror", "price": 19.99, "stock": 34, "cost_price": 9.50},
}

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


# @app.get("/products/{product_id}") 
# def get_product(product_id: int):
#     #await asyncio.sleep(3) # Simulating a call to a database warehouse
#     time.sleep(3)
#     if product_id not in PRODUCTS:
#         raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
#     return PRODUCTS[product_id]
##### FastAPI runs plain def routes in separate worker threads, so the blocking time.sleep()
#  does not block the entire server. It only blocks the thread that is handling that request.
#  This is why the server can still handle other requests while one request is sleeping.

#  However, if you have many requests that are all sleeping, you could run out of threads
#  and the server would become unresponsive. In such cases, using async def and await asyncio.sleep() 
# would be more efficient.


@app.get("/products/{product_id}", response_model=ProductOut) 
async def get_product(product_id: int):
    await asyncio.sleep(3) # Simulating a call to a database warehouse
    if product_id not in PRODUCTS:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return PRODUCTS[product_id]

@app.post("/products/", response_model=ProductOut)
async def create_product(product: ProductCreate):
    new_id = max(PRODUCTS) + 1
    PRODUCTS[new_id] = {"id": new_id, **product.model_dump()} # modeldump() converts the Pydantic model to a dictionary
    return PRODUCTS[new_id]

# If input is {"title": "M", "price": "banana", "stock": -5} , it will still work
# Hence we need to add input validation using Pydantic models. 

# 422	Error: Unprocessable Content if given wrong input