from fastapi import APIRouter, HTTPException
from schemas.product import ProductCreate, ProductOut
import asyncio


# Creates an instance of APIRouter class, which is used to define a group of related routes. 
# This allows for better organization and modularity of the application.
router = APIRouter() 

PRODUCTS = {
    1: {"id": 1, "title": "Essence Mascara Lash Princess", "price": 9.99, "stock": 99, "cost_price": 4.20},
    2: {"id": 2, "title": "Eyeshadow Palette with Mirror", "price": 19.99, "stock": 34, "cost_price": 9.50},
}


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



@router.get("/products/{product_id}", response_model=ProductOut) 
async def get_product(product_id: int):
    await asyncio.sleep(3) # Simulating a call to a database warehouse
    if product_id not in PRODUCTS:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return PRODUCTS[product_id]

@router.post("/products/", response_model=ProductOut)
async def create_product(product: ProductCreate):
    new_id = max(PRODUCTS) + 1
    PRODUCTS[new_id] = {"id": new_id, **product.model_dump()} # modeldump() converts the Pydantic model to a dictionary
    return PRODUCTS[new_id]


# If input is {"title": "M", "price": "banana", "stock": -5} , it will still work
# Hence we need to add input validation using Pydantic models.

# 422	Error: Unprocessable Content if given wrong input