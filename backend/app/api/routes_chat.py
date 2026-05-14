from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.chat_service import ask_operations_copilot


router = APIRouter()


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        examples=["Why are shipments delayed this week?"],
    )


class ChatResponse(BaseModel):
    interaction_id: int
    question: str
    question_type: str
    tools_used: list[str]
    answer: str
    context_preview: dict


@router.post("/ask", response_model=ChatResponse)
def ask_ai(request: ChatRequest, db: Session = Depends(get_db)):
    return ask_operations_copilot(
        db=db,
        question=request.question,
    )