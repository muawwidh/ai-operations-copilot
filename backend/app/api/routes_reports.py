from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.report_service import (
    generate_operations_report,
    get_report_by_id,
    list_reports,
)


router = APIRouter()


class GenerateReportRequest(BaseModel):
    report_type: str = Field(
        default="Weekly Operations Report",
        examples=["Weekly Operations Report"],
    )
    generated_by: str = Field(
        default="system",
        examples=["operations_manager"],
    )


class GenerateReportResponse(BaseModel):
    id: int
    report_type: str
    title: str
    content: str
    generated_by: str
    created_at: datetime
    context_preview: dict


class ReportListItem(BaseModel):
    id: int
    report_type: str
    title: str
    generated_by: str
    created_at: datetime


class ReportDetailResponse(BaseModel):
    id: int
    report_type: str
    title: str
    content: str
    generated_by: str
    created_at: datetime


@router.post("/generate", response_model=GenerateReportResponse)
def generate_report(
    request: GenerateReportRequest,
    db: Session = Depends(get_db),
):
    return generate_operations_report(
        db=db,
        report_type=request.report_type,
        generated_by=request.generated_by,
    )


@router.get("", response_model=list[ReportListItem])
def get_reports(
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return list_reports(db=db, limit=limit)


@router.get("/{report_id}", response_model=ReportDetailResponse)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
):
    report = get_report_by_id(db=db, report_id=report_id)

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found",
        )

    return {
        "id": report.id,
        "report_type": report.report_type,
        "title": report.title,
        "content": report.content,
        "generated_by": report.generated_by,
        "created_at": report.created_at,
    }