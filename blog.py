import os
from openai import OpenAI
import config

_client = OpenAI(
  api_key=os.getenv("CEREBRAS_API_KEY", config.CEREBRAS_API_KEY),
  base_url=config.CEREBRAS_API_BASE,
)


def _extract_response_text(response):
  choices = response.choices if response and response.choices else []
  if not choices:
    return ""

  first_choice = choices[0]
  message = getattr(first_choice, "message", None)
  content = message.content if message else None
  if content:
    return content.strip()

  text = getattr(first_choice, "text", None)
  if text:
    return text.strip()

  return ""


def generateBlogTopics(prompt1):
  response = _client.chat.completions.create(
      model=config.CEREBRAS_MODEL,
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Generate blog topics on: {}. \\n\\n1.".format(prompt1)}
      ],
      temperature=0.7,
      max_tokens=100,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
  )

  return _extract_response_text(response)

def generateBlogSections(prompt1):
  response = _client.chat.completions.create(
      model=config.CEREBRAS_MODEL,
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Expand the blog title into high level blog sections: {} \\n\\n- Introduction:".format(prompt1)}
      ],
      temperature=0.6,
      max_tokens=100,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
  )

  return _extract_response_text(response)

def blogSectionExpander(prompt1):
  response = _client.chat.completions.create(
      model=config.CEREBRAS_MODEL,
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Expand the blog section into a detailed professional, witty and clever explanation.\\n\\n{}".format(prompt1)}
      ],
      temperature=0.7,
      max_tokens=200,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
  )

  return _extract_response_text(response)
