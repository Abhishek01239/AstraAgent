import re

from llm import call_llm
from memory import add_to_memory, get_memory
from facts import remember_fact, get_fact

# ================= PROMPTS =================

PLANNER_PROMPT = """
You are the Planner.

Given a user request, break it into clear and minimal steps.
Do NOT solve the task.
Return steps as a numbered list.
"""

EXECUTOR_PROMPT = """
You are the Executor.

Follow the given plan and perform the task.
Explain clearly and step by step.
"""

CRITIC_PROMPT = """
You are a strict Critic.

Evaluate the answer.

If the answer is correct and complete, respond EXACTLY as:
STATUS: ACCEPT
FINAL_ANSWER: <final answer>

If the answer has errors or is incomplete, respond EXACTLY as:
STATUS: RETRY
FEEDBACK: <what went wrong and how to fix it>

Do not add anything else.
"""

# ================= CORE STAGES =================

def planner(task: str) -> str:
    messages = [
        {"role": "system", "content": PLANNER_PROMPT},
        *get_memory(),
        {"role": "user", "content": task}
    ]
    return call_llm(messages)


def executor(plan: str, feedback: str | None = None) -> str:
    messages = [
        {"role": "system", "content": EXECUTOR_PROMPT},
        *get_memory(),
        {"role": "user", "content": plan}
    ]

    if feedback:
        messages.append({
            "role": "user",
            "content": f"Critic feedback: {feedback}"
        })

    return call_llm(messages)


def critic(task: str, answer: str) -> dict:
    messages = [
        {"role": "system", "content": CRITIC_PROMPT},
        {
            "role": "user",
            "content": f"Task:\n{task}\n\nAnswer:\n{answer}"
        }
    ]

    result = call_llm(messages)

    if "STATUS: ACCEPT" in result:
        final = result.split("FINAL_ANSWER:", 1)[1].strip()
        return {"status": "accept", "answer": final}

    if "STATUS: RETRY" in result:
        feedback = result.split("FEEDBACK:", 1)[1].strip()
        return {"status": "retry", "feedback": feedback}

    return {"status": "accept", "answer": answer}


# ================= AGENT =================

def agent(user_input: str) -> str:
    text = user_input.strip().lower()

    # 🧠 MEMORY WRITE (SAFE PARSING)
    match = re.match(r"^my name is\s+(.+)$", text)
    if match:
        name = match.group(1).strip().title()
        remember_fact(
            "user_name",
            name,
            confidence=0.95,
            source="user_statement"
        )
        return f"Got it 👍 I’ll remember your name is {name}."

    # 🧠 MEMORY READ
    if "what is my name" in text:
        name = get_fact("user_name")
        if name:
            return f"Your name is {name}."
        return "I don’t know your name yet. You can tell me 😊"

    # 🧠 NORMAL PIPELINE
    add_to_memory("user", user_input)

    plan = planner(user_input)

    retries = 0
    feedback = None

    while retries < 2:
        execution = executor(plan, feedback)
        review = critic(user_input, execution)

        if review["status"] == "accept":
            final_answer = review["answer"]
            add_to_memory("assistant", final_answer)
            return final_answer

        feedback = review["feedback"]
        retries += 1

    add_to_memory("assistant", execution)
    return execution


# ================= MAIN =================

if __name__ == "__main__":
    print("AstraAgent v0.3 (Planner → Executor → Critic)")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        print("Agent:", agent(user_input))
