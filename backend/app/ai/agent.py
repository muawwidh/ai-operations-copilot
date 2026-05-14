import json

from openai import OpenAI
from sqlalchemy.orm import Session

from app.ai.tool_schemas import AGENT_TOOLS
from app.config import settings
from app.services.analytics_service import (
    get_customer_activity,
    get_operations_summary,
    get_shipment_delay_summary,
    get_ticket_summary,
)
from app.services.document_service import retrieve_relevant_chunks
from app.services.report_service import generate_operations_report


client = OpenAI(api_key=settings.OPENAI_API_KEY)


AGENT_SYSTEM_PROMPT = """
You are AI Operations Copilot, an enterprise-style AI assistant for logistics, SaaS operations,
customer support, document intelligence, and reporting.

You have access to approved backend tools. Use tools when the user asks about:
- operations KPIs
- shipment delays
- support tickets
- SLA breaches
- customer activity
- uploaded documents
- report generation

Rules:
- Do not invent numbers.
- Use tools for business-data questions.
- Use document search for policy, SOP, or uploaded-document questions.
- If a tool result is empty or limited, say so clearly.
- Provide concise business explanations with practical next actions.
- When a report is generated, mention the report ID.
"""


def to_json_string(data) -> str:
    return json.dumps(data, default=str)


def execute_agent_tool(
    db: Session,
    tool_name: str,
    arguments: dict,
):
    if tool_name == "get_operations_summary":
        return get_operations_summary(db)

    if tool_name == "get_shipment_delay_summary":
        return get_shipment_delay_summary(db)

    if tool_name == "get_ticket_summary":
        return get_ticket_summary(db)

    if tool_name == "get_customer_activity":
        limit = int(arguments.get("limit", 10))
        limit = max(1, min(limit, 50))
        return get_customer_activity(db, limit=limit)

    if tool_name == "search_documents":
        question = arguments.get("question", "")
        top_k = int(arguments.get("top_k", 5))
        top_k = max(1, min(top_k, 10))

        return {
            "question": question,
            "retrieved_chunks": retrieve_relevant_chunks(
                question=question,
                top_k=top_k,
            ),
        }

    if tool_name == "generate_operations_report":
        report_type = arguments.get("report_type", "Weekly Operations Report")
        generated_by = arguments.get("generated_by", "agent")

        return generate_operations_report(
            db=db,
            report_type=report_type,
            generated_by=generated_by,
        )

    return {
        "error": f"Unknown tool: {tool_name}",
    }


def run_operations_agent(
    db: Session,
    user_question: str,
) -> dict:
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key_here":
        return {
            "answer": "OpenAI API key is not configured. Please set OPENAI_API_KEY in your .env file.",
            "tools_used": [],
            "tool_outputs": [],
        }

    messages = [
        {
            "role": "system",
            "content": AGENT_SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_question,
        },
    ]

    first_response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=messages,
        tools=AGENT_TOOLS,
        tool_choice="auto",
        temperature=0.2,
    )

    assistant_message = first_response.choices[0].message
    messages.append(assistant_message)

    tools_used: list[str] = []
    tool_outputs: list[dict] = []

    if assistant_message.tool_calls:
        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name

            try:
                arguments = json.loads(tool_call.function.arguments or "{}")
            except json.JSONDecodeError:
                arguments = {}

            tool_result = execute_agent_tool(
                db=db,
                tool_name=tool_name,
                arguments=arguments,
            )

            tools_used.append(tool_name)
            tool_outputs.append(
                {
                    "tool_name": tool_name,
                    "arguments": arguments,
                    "result": tool_result,
                }
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": to_json_string(tool_result),
                }
            )

        final_response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            tools=AGENT_TOOLS,
            temperature=0.2,
        )

        final_answer = final_response.choices[0].message.content or ""

    else:
        final_answer = assistant_message.content or ""

    return {
        "answer": final_answer,
        "tools_used": tools_used,
        "tool_outputs": tool_outputs,
    }