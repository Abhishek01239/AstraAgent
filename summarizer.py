from llm import call_llm

SUMMARY_PROMPT = """
Summarize the following conversation into important facts
and conclusions only.

Ignore small talk.

Be concise.
"""

def summarize(memory):
    if not memory:
        return None

    messages = [
        {"role": "system", "content": SUMMARY_PROMPT},
        {"role":"user", "content": str(memory)}
    ]

    return call_llm(messages)