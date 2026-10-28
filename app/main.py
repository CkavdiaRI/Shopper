from sys import prefix

from fastapi import FastAPI
from app.routers import products
from app.core.config import settings

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.db.database import engine, get_db
from app.routers import products
from app.db.models import Base

from contextlib import asynccontextmanager


from app.db.database import engine, get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose

app = FastAPI(lifespan=lifespan)



# load_dotenv() # Load environment variables from .env file
# SUPPLIER_BASE_URL = os.getenv("SUPPLIER_BASE_URL") # Get the value of SUPPLIER_BASE_URL from environment variables

settings.supplier_base_url #-> You can access the supplier_base_url from the settings object, which is an instance of the Settings class.

#app = FastAPI() # Creates an instance of FastAPI class, which is the main entry point for the application

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


@app.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    await db.execute(text("SELECT 1"))
    return {
        "status":"ok",
        "supplier":settings.supplier_base_url,
        "database":"up",
    }

