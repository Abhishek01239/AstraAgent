import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from llm import call_llm

def is_goal_complete(goal, history):
    """
    Goal is complete ONLY if:
    - task solved
    - AND output produced (file created if required)
    """

    messages = [
        {
            "role": "system",
            "content": """
Decide if goal is complete.

ONLY say YES if:
- the task is solved
- AND final output is produced
- AND if goal asks to save or create something, a file must be created

Otherwise say NO.
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
