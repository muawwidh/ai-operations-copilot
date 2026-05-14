from openai import OpenAI

from app.config import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_ai_response(system_prompt: str, user_prompt: str) -> str:
    """
    Sends a prompt to the OpenAI model and returns the text response.
    """

    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key_here":
        return (
            "OpenAI API key is not configured. Please set OPENAI_API_KEY in your .env file."
        )

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content or ""