# Contacting the service to get the supplier details

import httpx
from app.schemas.supplier import SupplierProduct

class SupplierService:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_by_id(self, product_id: int) -> dict | None:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/products/{product_id}")

        item = SupplierProduct.model_validate(response.json())
        return item.model_dump()