from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    status_code = 500
    error_code = "internal_error"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ProductNotFoundError(AppError):
    status_code = 404
    error_code = "product_not_found"


def register_error_handlers(app):
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.status_code, "type": exc.error_code, "detail": exc.message}},
        )
