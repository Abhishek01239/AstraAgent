import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from llm import call_llm

def is_goal_complete(goal, history):
    """
    Ask LLM if goal is achieved.
    Return True or False.
    """

    messages = [
        {
            "role": "system",
            "content": """
You decide whether a discussion goal is complete.

Respond ONLY:
YES → if goal achieved
NO → if more work needed
"""
        },
        {
            "role": "user",
            "content": f"""
Goal:
{goal}

Discussion:
{history}
"""
        }
    ]

    result = call_llm(messages).strip().upper()
    return "YES" in result

def get_next_objective(goal, history):
    """
    Decide what agents should do next.
    """

    messages = [
        {
            "role": "system",
            "content": """
Given a goal and discussion, decide the next objective.
Return one short action.
"""
        },
        {
            "role": "user",
            "content": f"""
Goal:
{goal}

Discussion:
{history}
"""
        }
    ]

    return call_llm(messages).strip()
