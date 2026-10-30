class AiService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def make_pitch(self, product: dict) -> str:
        # Fallback pitch: the real AI call returns here when the key is fake or missing.
        return f"Only {product['stock']} left of {product['title']} at {product['price']}!"
