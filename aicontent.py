import os
import openai
import config

openai.api_key = os.getenv("CEREBRAS_API_KEY", config.CEREBRAS_API_KEY)
openai.api_base = config.CEREBRAS_API_BASE


def _extract_response_text(response):
    choices = response.get("choices", [])
    if not choices:
        return "Sorry! The AI could not understand what you are looking for"

    first_choice = choices[0]
    message = first_choice.get("message", {})
    content = message.get("content")
    if content:
        return content.strip()

    text = first_choice.get("text")
    if text:
        return text.strip()

    return "Sorry! The AI could not understand what you are looking for"


def openAI(query):
        response = openai.ChatCompletion.create(
            model=config.CEREBRAS_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ],
            temperature=0.5,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return _extract_response_text(response)


