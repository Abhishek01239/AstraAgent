from llm import call_llm

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
You are the Critic.

Review the executor's answer.
Fix mistakes if any.
Improve clarity.
Return ONLY the final improved answer.
"""

# ================= FUNCTIONS =================

def planner(task: str) -> str:
    messages = [
        {"role": "system", "content": PLANNER_PROMPT},
        {"role": "user", "content": task}
    ]
    return call_llm(messages)


def executor(plan: str) -> str:
    messages = [
        {"role": "system", "content": EXECUTOR_PROMPT},
        {"role": "user", "content": plan}
    ]
    return call_llm(messages)


def critic(original_task: str, execution_result: str) -> str:
    messages = [
        {"role": "system", "content": CRITIC_PROMPT},
        {
            "role": "user",
            "content": f"Task:\n{original_task}\n\nAnswer:\n{execution_result}"
        }
    ]
    return call_llm(messages)


# ================= AGENT LOOP =================

def agent(user_input: str) -> str:
    if len(user_input.strip()) < 2:
        return "Can you please clarify your question?"

    # 1️⃣ PLAN
    plan = planner(user_input)

    # 2️⃣ EXECUTE
    execution = executor(plan)

    # 3️⃣ CRITIC
    final_answer = critic(user_input, execution)

    return final_answer


# ================= MAIN =================

if __name__ == "__main__":
    print("AstraAgent v0.3 (Planner → Executor → Critic)")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response = agent(user_input)
        print("Agent:", response)
