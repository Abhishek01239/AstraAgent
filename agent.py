from llm import call_llm
from memory import add_to_memory, get_memory
from tools import calculator

# ================= PROMPTS =================

PLANNER_PROMPT = """
You are the Planner.

Decide whether the user request needs a TOOL or not.

If a tool is needed, respond EXACTLY in this format:
TOOL: calculator
INPUT: <math expression>

If no tool is needed, respond with:
NO_TOOL

Do NOT solve the task.
Do NOT explain.
"""

EXECUTOR_PROMPT = """
You are the Executor.

Answer the user's request clearly and naturally.
Use conversation context if needed.
"""

CRITIC_PROMPT = """
You are a silent Critic.

You NEVER mention planning, reviewing, or roles.
You NEVER explain your reasoning.
You ONLY return the final improved answer for the user.

Fix mistakes if any.
Improve clarity.
If the answer is already good, return it as-is.
"""

# ================= CORE FUNCTIONS =================

def planner(task: str) -> str:
    messages = [
        {"role": "system", "content": PLANNER_PROMPT},
        *get_memory(),
        {"role": "user", "content": task}
    ]
    return call_llm(messages).strip()


def executor(task: str) -> str:
    messages = [
        {"role": "system", "content": EXECUTOR_PROMPT},
        *get_memory(),
        {"role": "user", "content": task}
    ]
    return call_llm(messages)


def critic(original_task: str, execution_result: str) -> str:
    messages = [
        {"role": "system", "content": CRITIC_PROMPT},
        *get_memory(),
        {
            "role": "user",
            "content": (
                f"User request:\n{original_task}\n\n"
                f"Executor answer:\n{execution_result}"
            )
        }
    ]
    return call_llm(messages)


# ================= TOOL ROUTER =================

def route_tool(plan: str):
    if plan.startswith("TOOL:"):
        lines = plan.splitlines()
        if len(lines) < 2:
            return None

        tool_name = lines[0].replace("TOOL:", "").strip()
        tool_input = lines[1].replace("INPUT:", "").strip()

        if tool_name == "calculator":
            return calculator(tool_input)

    return None


# ================= AGENT =================

def agent(user_input: str) -> str:
    if len(user_input.strip()) < 2:
        return "Can you please clarify your question?"

    # 1️⃣ store user input FIRST
    add_to_memory("user", user_input)

    # 2️⃣ plan
    plan = planner(user_input)

    # 3️⃣ tool check
    tool_result = route_tool(plan)
    if tool_result is not None:
        add_to_memory("assistant", tool_result)
        return tool_result

    # 4️⃣ execute
    execution = executor(user_input)

    # 5️⃣ critic (silent)
    final_answer = critic(user_input, execution).strip()

    # 6️⃣ store final answer
    add_to_memory("assistant", final_answer)

    return final_answer


# ================= MAIN LOOP =================

if __name__ == "__main__":
    print("AstraAgent v0.4 (Planner → Tool → Executor → Critic)")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response = agent(user_input)
        print("Agent:", response)
