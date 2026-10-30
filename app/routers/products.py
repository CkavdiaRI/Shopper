from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.database import get_db
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product import PitchOut, ProductCreate, ProductOut, ProductQuery
from app.services.ai_service import AiService
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


def get_ai_service() -> AiService:
    return AiService(settings.groq_api_key)


def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(ProductRepository(db), CategoryRepository(db))


@router.get("/{product_id}", response_model=ProductOut, summary="Get one product")
async def get_product(
    product_id: int = Path(gt=0),
    service: ProductService = Depends(get_product_service),
):
    return await service.get_by_id(product_id)


@router.get("", response_model=list[ProductOut], summary="List products, one page at a time")
async def list_products(
    query: Annotated[ProductQuery, Query()],
    service: ProductService = Depends(get_product_service),
):
    return await service.list_products(query)


@router.post("", response_model=ProductOut, status_code=201, summary="Create a product")
async def create_product(
    product: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    return await service.create(product)


@router.get("/{product_id}/pitch", response_model=PitchOut, summary="A short AI-written notification")
async def get_pitch(
    product_id: int = Path(gt=0),
    service: ProductService = Depends(get_product_service),
    ai: AiService = Depends(get_ai_service),
):
    product = await service.get_by_id(product_id)
    notification = await ai.make_pitch(product)
    return {"product_id": product_id, "notification": notification}
