import re

from llm import call_llm
from memory import add_to_memory, get_memory
from facts import remember_fact, get_fact
from summarizer import summarize   # you must already have / or create this

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

    # fallback safety
    return {"status": "accept", "answer": answer}

# ================= AGENT =================

def agent(user_input: str) -> str:
    text = user_input.strip().lower()

    # 🧠 FACT STORE (SAFE)
    match = re.match(r"^my name is\s+(.+)$", text)
    if match:
        name = match.group(1).strip().title()
        remember_fact(
            key="user_name",
            value=name,
            confidence=0.95,
            source="user_statement"
        )
        return f"Got it 👍 I’ll remember your name is {name}."

    # 🧠 FACT QUERY
    if "what is my name" in text:
        name = get_fact("user_name")
        return f"Your name is {name}." if name else "I don’t know your name yet 😊"

    # 🧠 NORMAL MEMORY FLOW
    add_to_memory("user", user_input)

    # 🔴 SUMMARY LOGIC — THIS IS WHERE IT GOES
    if len(get_memory()) >= 6:
        summary = summarize(get_memory())
        remember_fact(
            key="conversation_summary",
            value=summary,
            confidence=0.6,
            source="auto_summary"
        )

    # 1️⃣ PLAN
    plan = planner(user_input)

    retries = 0
    feedback = None

    # 2️⃣ EXECUTE → CRITIC LOOP
    while retries < 2:
        execution = executor(plan, feedback)
        review = critic(user_input, execution)

        if review["status"] == "accept":
            final_answer = review["answer"]
            add_to_memory("assistant", final_answer)
            return final_answer

        feedback = review["feedback"]
        retries += 1

    # fallback
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
