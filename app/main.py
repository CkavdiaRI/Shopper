from sys import prefix
import os
from dotenv import load_dotenv

from fastapi import FastAPI
from app.routers import products

load_dotenv() # Load environment variables from .env file
SUPPLIER_BASE_URL = os.getenv("SUPPLIER_BASE_URL") # Get the value of SUPPLIER_BASE_URL from environment variables

app = FastAPI() # Creates an instance of FastAPI class, which is the main entry point for the application

app.include_router(products.router, prefix="/api/v1") # Include the products router in the main application


app.include_router(products.router, prefix="/api/v2")

# Split the main file into the following :
# 1. Routers -> HTTP, paths, status codes
# 2. Services -> business rules
# 3. Schemas -> data shapes
# 4. Main.py -> wiring everything together

# Main.py may import routers. Routers may import services. Services may import schemas. 
# Schemas should not import anything else. Never go back up the chanin of imports. 
# This is to avoid circular imports.




