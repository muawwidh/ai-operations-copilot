from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "AI Operations Copilot",
        "version": "0.1.0",
    }