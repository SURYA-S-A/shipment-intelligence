from fastapi import FastAPI
from contextlib import asynccontextmanager
from shipment_intelligence_api.core.dependencies import (
    get_qdrant_store_manager_instance,
)
from shipment_intelligence_api.core.exceptions import global_exception_handler
from shipment_intelligence_api.health.router import (
    router as health_router,
)
from shipment_intelligence_api.rag.router import router as rag_router
from shipment_intelligence_api.agents.router import router as agents_router
from shipment_intelligence_api.core.logging import get_logger
from fastapi.middleware.cors import CORSMiddleware

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager.

    Initializes resources on startup and cleans up on shutdown.
    """
    logger.info("Initializing application...")
    get_qdrant_store_manager_instance()
    logger.info("Vector store initialized")

    yield

    # Application Shutdown
    logger.info("Shutting down application...")


app = FastAPI(
    title="Shipment Intelligence API",
    description="Agent-based API for shipment intelligence",
    root_path="/api",
    docs_url="/swagger",
    lifespan=lifespan,
)

app.add_exception_handler(Exception, global_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(rag_router)
app.include_router(agents_router)
