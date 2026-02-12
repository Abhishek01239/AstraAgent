import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from llm import call_llm

class Agent:
    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt

    def speak(self, chat_history, topic):
        """
        Agent reads full chat and produces next message.
        """

        history_text = "\n".join(
            [f"{msg['sender']}: {msg['text']}" for msg in chat_history]
        )

        messages = [
            {"role": "system", "content": self.system_prompt},
            {
                "role": "user",
                "content": f"""
Topic: {topic}

Conversation so far:
{history_text}

Respond with ONE short message continuing the discussion.
Do not repeat previous messages.
"""
            }
        ]

        reply = call_llm(messages)
        return reply.strip()
