from sqlalchemy.orm import Session

from app.ai.agent import run_operations_agent
from app.models.ai_interaction import AIInteraction


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
    agent_result = run_operations_agent(
        db=db,
        user_question=question,
    )

    tools_used = agent_result.get("tools_used", [])
    answer = agent_result.get("answer", "")

    source_type = "general"

    if "search_documents" in tools_used:
        source_type = "document"
    elif tools_used:
        source_type = "database"

    if "search_documents" in tools_used and len(tools_used) > 1:
        source_type = "mixed"

    interaction = save_ai_interaction(
        db=db,
        user_question=question,
        ai_response=answer,
        tools_used=", ".join(tools_used),
        source_type=source_type,
    )

    return {
        "interaction_id": interaction.id,
        "question": question,
        "answer": answer,
        "tools_used": tools_used,
        "source_type": source_type,
        "tool_outputs": agent_result.get("tool_outputs", []),
    }