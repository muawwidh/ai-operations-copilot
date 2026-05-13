from fastapi import FastAPI

from app.api.routes_health import router as health_router

app = FastAPI(
    title="AI Operations Copilot",
    description="Enterprise-style AI assistant for business operations, logistics, support, analytics, and reporting.",
    version="0.1.0",
)

app.include_router(
    health_router,
    prefix="/api",
    tags=["Health"],
)