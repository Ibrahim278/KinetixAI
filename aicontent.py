import os
import openai as _openai
from openai import OpenAI
import config

# Prefer explicit env var, fall back to config values
_api_key = os.getenv("CEREBRAS_API_KEY") or os.getenv("OPENAI_API_KEY") or config.CEREBRAS_API_KEY or config.OPENAI_API_KEY
_base_url = os.getenv("CEREBRAS_API_BASE") or config.CEREBRAS_API_BASE

_client = OpenAI(
    api_key=_api_key,
    base_url=_base_url,
)

_FORMAT_GUIDE = """
Formatting requirements:
- Return valid Markdown only.
- Use clear section headings with '##' and '###'.
- Use standard lists with '-' or '1.' for bullets.
- Do not use unicode bullet symbols like '•'.
- Keep spacing and indentation consistent.
- Avoid markdown tables unless explicitly requested.
""".strip()


def _extract_response_text(response):
    choices = response.choices if response and response.choices else []
    if not choices:
        return "Sorry! The AI could not understand what you are looking for"

    first_choice = choices[0]
    message = getattr(first_choice, "message", None)
    content = message.content if message else None
    if content:
        return content.strip()

    text = getattr(first_choice, "text", None)
    if text:
        return text.strip()

    return "Sorry! The AI could not understand what you are looking for"


def openAI(query):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that writes clean, structured, easy-to-scan markdown.",
        },
        {"role": "user", "content": f"{query}\n\n{_FORMAT_GUIDE}"},
    ]

    # Validate API key before attempting requests
    if not _api_key:
        return "[Error] No API key configured. Set CEREBRAS_API_KEY or OPENAI_API_KEY in your environment."

    chunks = []
    for _ in range(3):
        try:
            response = _client.chat.completions.create(
                model=config.CEREBRAS_MODEL,
                messages=messages,
                temperature=0.5,
                max_tokens=900,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
        except Exception as e:
            # Provide a helpful error string instead of raising an internal server error
            try:
                err_msg = str(e)
            except Exception:
                err_msg = "Unknown API error"
            return f"[Error] AI request failed: {err_msg}. Check your API key and CEREBRAS_API_BASE configuration."

        choices = response.choices if response and response.choices else []
        if not choices:
            break

        first_choice = choices[0]
        message = getattr(first_choice, "message", None)
        content = message.content if message else getattr(first_choice, "text", "")
        content = content.strip() if content else ""

        if content:
            chunks.append(content)

        if getattr(first_choice, "finish_reason", None) != "length":
            break

        # Ask for continuation only if model truncated due to token length.
        if content:
            messages.append({"role": "assistant", "content": content})
        messages.append(
            {
                "role": "user",
                "content": "Continue exactly from where you stopped. Do not repeat previous text and preserve the same markdown structure.",
            }
        )

    if chunks:
        return "\n\n".join(chunks)

    return "Sorry! The AI could not understand what you are looking for"


