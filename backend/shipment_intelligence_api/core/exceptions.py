from fastapi import Request
from fastapi.responses import JSONResponse
from shipment_intelligence_api.core.logging import get_logger

logger = get_logger(__name__)


async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled exceptions"""
    logger.error(f"Unhandled exception", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc),
        },
    )
