from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.document_service import (
    ask_document_question,
    list_documents,
    process_uploaded_document,
)


router = APIRouter()


class DocumentUploadResponse(BaseModel):
    id: int
    file_name: str
    file_type: str
    processed_status: str
    chunks_created: int
    uploaded_at: datetime


class DocumentListItem(BaseModel):
    id: int
    file_name: str
    file_type: str
    processed_status: str
    uploaded_at: datetime


class DocumentAskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        examples=["What does the escalation policy say about high-priority tickets?"],
    )
    top_k: int = Field(default=5, ge=1, le=10)


class DocumentAskResponse(BaseModel):
    question: str
    answer: str
    retrieved_chunks: list[dict]


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        return await process_uploaded_document(db=db, file=file)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(error)}",
        )


@router.get("", response_model=list[DocumentListItem])
def get_documents(db: Session = Depends(get_db)):
    return list_documents(db=db)


@router.post("/ask", response_model=DocumentAskResponse)
def ask_documents(
    request: DocumentAskRequest,
    db: Session = Depends(get_db),
):
    try:
        return ask_document_question(
            db=db,
            question=request.question,
            top_k=request.top_k,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Document question answering failed: {str(error)}",
        )