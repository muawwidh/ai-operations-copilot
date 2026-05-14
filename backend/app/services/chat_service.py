from sqlalchemy.orm import Session

from app.ai.llm_client import generate_ai_response
from app.ai.prompts import (
    OPERATIONS_COPILOT_SYSTEM_PROMPT,
    build_business_analysis_prompt,
)
from app.models.ai_interaction import AIInteraction
from app.services.analytics_service import (
    get_customer_activity,
    get_operations_summary,
    get_shipment_delay_summary,
    get_ticket_summary,
)


def detect_question_type(question: str) -> str:
    """
    Simple intent detection for MVP.
    Later this can be replaced by proper tool-calling or LangGraph.
    """

    q = question.lower()

    if any(word in q for word in ["delay", "delayed", "shipment", "carrier", "delivery"]):
        return "shipment_delays"

    if any(word in q for word in ["ticket", "support", "sla", "priority", "complaint"]):
        return "ticket_summary"

    if any(word in q for word in ["customer", "active", "activity", "account"]):
        return "customer_activity"

    if any(word in q for word in ["summary", "operation", "kpi", "performance", "overview"]):
        return "operations_summary"

    return "operations_summary"


def get_context_for_question(db: Session, question_type: str) -> dict:
    if question_type == "shipment_delays":
        return get_shipment_delay_summary(db)

    if question_type == "ticket_summary":
        return get_ticket_summary(db)

    if question_type == "customer_activity":
        return get_customer_activity(db, limit=10)

    return get_operations_summary(db)


def save_ai_interaction(
    db: Session,
    user_question: str,
    ai_response: str,
    tools_used: str,
    source_type: str,
) -> AIInteraction:
    interaction = AIInteraction(
        user_question=user_question,
        ai_response=ai_response,
        tools_used=tools_used,
        source_type=source_type,
    )

    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    return interaction


def ask_operations_copilot(db: Session, question: str) -> dict:
    question_type = detect_question_type(question)

    analytics_context = get_context_for_question(db, question_type)

    user_prompt = build_business_analysis_prompt(
        user_question=question,
        analytics_context=analytics_context,
    )

    ai_response = generate_ai_response(
        system_prompt=OPERATIONS_COPILOT_SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )

    interaction = save_ai_interaction(
        db=db,
        user_question=question,
        ai_response=ai_response,
        tools_used=question_type,
        source_type="database",
    )

    return {
        "interaction_id": interaction.id,
        "question": question,
        "question_type": question_type,
        "tools_used": [question_type],
        "answer": ai_response,
        "context_preview": analytics_context,
    }