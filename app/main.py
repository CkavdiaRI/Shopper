from sys import prefix

from fastapi import FastAPI
import httpx
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

from app.core.errors import register_error_handlers
from app.db.database import engine, get_db
from app.services.auth_client import AuthClient
from app.services.ai_service import AiService


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # one client for each service
    auth_http = httpx.AsyncClient(base_url=settings.auth_service_url, timeout=httpx.Timeout(3.0, connect=0.5))
    groq_http = httpx.AsyncClient(base_url=settings.groq_url, timeout=httpx.Timeout(4.0, connect=1.0))
    app.state.auth = AuthClient(auth_http)
    app.state.ai = AiService(groq_http, settings.groq_api_key, settings.groq_url)

    yield

    await auth_http.aclose()
    await groq_http.aclose()
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
register_error_handlers(app)



# load_dotenv() # Load environment variables from .env file
# SUPPLIER_BASE_URL = os.getenv("SUPPLIER_BASE_URL") # Get the value of SUPPLIER_BASE_URL from environment variables

settings.supplier_base_url #-> You can access the supplier_base_url from the settings object, which is an instance of the Settings class.

#app = FastAPI() # Creates an instance of FastAPI class, which is the main entry point for the application

app.include_router(products.router, prefix="/api/v1") # Include the products router in the main application

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

