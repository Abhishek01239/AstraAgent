from openai import OpenAI
from config import OPENROUTER_API_KEY, BASE_URL, MODEL, MAX_TOKENS, TEMPERATURE

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL
)

def call_llm(messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE
    )
    return response.choices[0].message.content
