import httpx

from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

from app.core.config import settings
from app.core.errors import AuthServiceError, NotAuthenticatedError
from app.core.breaker import Breaker


class TryAgain(Exception):
    """The friend had a bad moment. Asking again may work."""

class AuthCLient : 
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.breaker = Breaker()

    @retry(
        retry=retry_if_exception_type(TryAgain),
        stop=stop_after_attempt(3),
        wait=wait_exponential_jitter(multiplier=0.5, max=4, jitter=0.5),
        reraise=True,
    )
    async def _ask(self, authorization: str) -> httpx.Response:
        try:
            response = await self.client.get("/api/v1/auth/validate-token", headers={"Authorization": authorization})
        
        except httpx.TransportError as exc:
            self.breaker.failure()
            raise TryAgain from exc

        if response.status_code in (500, 502, 503, 504):
            self.breaker.failure()
            raise TryAgain(f"Auth service returned {response.status_code}")

        self.breaker.success()
        return response

    async def check_token(self, authorization: str | None) -> dict:
        if authorization is None:
            raise NotAuthenticatedError("Not authenticated")
        try:
            response = await self._ask(authorization)
        except httpx.HTTPError:
            raise AuthServiceError("The login service is not available right now")
        if response.status_code == 401:
            raise NotAuthenticatedError("Invalid or expired token")
        if response.status_code != 200:
            raise AuthServiceError("The login service is not available right now")
        return response.json()


AuthClient = AuthCLient
