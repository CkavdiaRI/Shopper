from typing import Annotated

from fastapi import Depends, Header
from httpx import request

from app.core.errors import ForbiddenError
from app.services import auth_client


async def current_user(authorization: Annotated[str | None, Header()] = None) -> dict:
    return await request.app.state.auth.check_token(authorization)


def require_admin(user: dict = Depends(current_user)) -> dict:
    if user["role"] != "ADMIN":
        raise ForbiddenError("Admins only")
    return user
