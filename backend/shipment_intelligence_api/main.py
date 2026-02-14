from fastapi import FastAPI
from contextlib import asynccontextmanager
from shipment_intelligence_api.core.dependencies import (
    get_qdrant_store_manager_instance,
)
from shipment_intelligence_api.health.router import (
    router as health_router,
)
from shipment_intelligence_api.rag.router import router as rag_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager.

    Initializes resources on startup and cleans up on shutdown.
    """
    # Application Startup
    print("Initializing application...")
    get_qdrant_store_manager_instance()
    print("Vector store initialized")

    yield

    # Application Shutdown
    print("Shutting down application...")


app = FastAPI(
    title="Shipment Intelligence API",
    description="Agent-based API for shipment intelligence",
    root_path="/api",
    docs_url="/swagger",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(rag_router)
