import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    logger.warning(f"Integrity error: {exc}")
    return JSONResponse(status_code=400, content={"detail": "Data integrity error"})
