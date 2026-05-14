from sqlalchemy.orm import Session

from app.ai.llm_client import generate_ai_response
from app.ai.prompts import REPORT_SYSTEM_PROMPT, build_operations_report_prompt
from app.models.report import Report
from app.services.analytics_service import (
    get_customer_activity,
    get_operations_summary,
    get_shipment_delay_summary,
    get_ticket_summary,
)


def build_report_context(db: Session) -> dict:
    """
    Collects all analytics needed for an operations report.
    """

    return {
        "operations_summary": get_operations_summary(db),
        "shipment_delay_summary": get_shipment_delay_summary(db),
        "ticket_summary": get_ticket_summary(db),
        "customer_activity": get_customer_activity(db, limit=10),
    }


def generate_report_title(report_type: str) -> str:
    clean_report_type = report_type.strip().title()

    if not clean_report_type:
        clean_report_type = "Operations Report"

    return f"{clean_report_type}"


def save_report(
    db: Session,
    report_type: str,
    title: str,
    content: str,
    generated_by: str = "system",
) -> Report:
    report = Report(
        report_type=report_type,
        title=title,
        content=content,
        generated_by=generated_by,
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report


def generate_operations_report(
    db: Session,
    report_type: str = "Weekly Operations Report",
    generated_by: str = "system",
) -> dict:
    analytics_context = build_report_context(db)

    user_prompt = build_operations_report_prompt(
        report_type=report_type,
        analytics_context=analytics_context,
    )

    report_content = generate_ai_response(
        system_prompt=REPORT_SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )

    title = generate_report_title(report_type)

    report = save_report(
        db=db,
        report_type=report_type,
        title=title,
        content=report_content,
        generated_by=generated_by,
    )

    return {
        "id": report.id,
        "report_type": report.report_type,
        "title": report.title,
        "content": report.content,
        "generated_by": report.generated_by,
        "created_at": report.created_at,
        "context_preview": analytics_context,
    }


def list_reports(db: Session, limit: int = 20) -> list[dict]:
    reports = (
        db.query(Report)
        .order_by(Report.created_at.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": report.id,
            "report_type": report.report_type,
            "title": report.title,
            "generated_by": report.generated_by,
            "created_at": report.created_at,
        }
        for report in reports
    ]


def get_report_by_id(db: Session, report_id: int) -> Report | None:
    return db.query(Report).filter(Report.id == report_id).first()