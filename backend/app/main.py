from fastapi import FastAPI

from app.api.routes_analytics import router as analytics_router
from app.api.routes_chat import router as chat_router
from app.api.routes_documents import router as documents_router
from app.api.routes_health import router as health_router
from app.api.routes_reports import router as reports_router


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

app.include_router(
    analytics_router,
    prefix="/api/analytics",
    tags=["Analytics"],
)

app.include_router(
    chat_router,
    prefix="/api/chat",
    tags=["AI Chat"],
)

app.include_router(
    reports_router,
    prefix="/api/reports",
    tags=["Reports"],
)

app.include_router(
    documents_router,
    prefix="/api/documents",
    tags=["Documents"],
)