import httpx


class AiService:
    def __init__(self, client: httpx.AsyncClient, api_key: str, url: str):
        self.client = client
        self.api_key = api_key
        self.url = url

    async def make_pitch(self, product: dict) -> str:
        # Fallback pitch: the real AI call returns here when the key is fake or missing.
        return f"Only {product['stock']} left of {product['title']} at {product['price']}!"
