import sys
import os
from tool_executor import execute_tool

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from llm import call_llm


class Agent:
    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt

    def speak(self, topic, history=""):
        """
        Agent can either:
        - respond normally
        - call a tool using JSON
        """

        messages = [
            {
                "role": "system",
                "content": self.system_prompt + """
You may use tools.

If a tool is needed, respond ONLY with JSON:

{
 "tool": "write_file",
 "args": {"filename": "name.txt", "content": "text"}
}

Otherwise respond normally.
"""
        },
        {
            "role": "user",
            "content": f"""
Objective:
{topic}

Conversation:
{history}
"""
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

        response = call_llm(messages).strip()

        if response.startswith("{") and "tool" in response:
            return execute_tool(response)
        
        return response
