import json
import os
from typing import Any

from openai import OpenAI

from backend.app.schemas import ChatMessage

SYSTEM_PROMPT = """You are a KBC digital banking assistant.
Answer in the same language as the customer.
Use only the attached customer context. Do not invent balances, transactions, other clients, or facts not in that context.
Do not execute or offer to execute transfers, payments, or collect credentials.
You are not giving formal financial advice.
"""

HISTORY_LIMIT = 10


def _openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    kwargs: dict[str, Any] = {"api_key": api_key}
    base_url = os.environ.get("OPENAI_BASE_URL")
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


def generate_reply(
    message: str,
    customer: dict[str, Any],
    history: list[ChatMessage],
) -> str:
    client = _openai_client()
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    messages: list[dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "system",
            "content": "Customer context:\n" + json.dumps(customer, ensure_ascii=False),
        },
    ]
    for turn in history[-HISTORY_LIMIT:]:
        messages.append({"role": turn.role, "content": turn.content})
    messages.append({"role": "user", "content": message})

    completion = client.chat.completions.create(model=model, messages=messages)
    reply = completion.choices[0].message.content
    return reply or ""
