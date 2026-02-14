from fastapi import FastAPI
from shipment_intelligence_api.infrastructure.health.router import (
    router as health_router,
)

app = FastAPI(
    title="Shipment Intelligence API",
    description="Agent-based API for shipment intelligence",
    root_path="/api",
    docs_url="/swagger",
)


app.include_router(health_router)
