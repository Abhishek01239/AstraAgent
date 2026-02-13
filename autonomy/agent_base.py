import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from llm import call_llm


class Agent:
    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt

    def speak(self, topic, history=""):
        """
        Generate a message based on:
        - discussion topic
        - previous chat history
        """

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": f"""
Discussion Topic:
{topic}

Conversation so far:
{history}

Respond with ONE short message to continue discussion.
"""
            }
        ]

        response = call_llm(messages)
        return response.strip()
