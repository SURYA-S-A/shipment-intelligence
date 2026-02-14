from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "/", summary="Health Check", description="Check the health status of the API."
)
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
