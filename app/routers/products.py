from fastapi import APIRouter, Depends, HTTPException
from app.schemas.product import ProductCreate, ProductOut
from app.services.product_service import ProductService
import asyncio


# Creates an instance of APIRouter class, which is used to define a group of related routes. 
# This allows for better organization and modularity of the application.
router = APIRouter(prefix = "/products", tags = ["products"]) 
# Prefix is added to all routes defined in this router. 
# Tags are used for documentation purposes.



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

def get_product_service() -> ProductService:
    return ProductService()


@router.get("/{product_id}", response_model=ProductOut) 
async def get_product(
     product_id: int, 
     service: ProductService = Depends(get_product_service)
     ):
    product = service.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return product

@router.post("", response_model=ProductOut, status_code=201, summary="Created a new product")
async def create_product(product: ProductCreate):
    service = ProductService()
    return service.create(product)
    # new_id = max(PRODUCTS) + 1
    # PRODUCTS[new_id] = {"id": new_id, **product.model_dump()} # modeldump() converts the Pydantic model to a dictionary
    # return PRODUCTS[new_id]


# If input is {"title": "M", "price": "banana", "stock": -5} , it will still work
# Hence we need to add input validation using Pydantic models.

# 422	Error: Unprocessable Content if given wrong input