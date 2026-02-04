from llm import call_llm
from memory import add_to_memory, get_memory
from tools import calculator, recall_memory

# ================= PROMPTS =================

PLANNER_PROMPT = """
You are the Planner.

Decide which tools are required.

Available tools:
- calculator
- recall_memory

If tools are needed, respond EXACTLY in this format:
TOOLS:
- <tool_name>: <input>

You may use multiple tools.

If no tools are needed, respond with:
NO_TOOL

Do NOT solve the task.
Do NOT explain.
"""

EXECUTOR_PROMPT = """
You are the Executor.

Answer the user's request clearly and naturally.
Use the conversation context if needed.
"""

CRITIC_PROMPT = """
You are a silent Critic.

You NEVER mention planning, tools, or reviewing.
You NEVER explain your reasoning.
You ONLY return the final improved answer.

Fix mistakes if any.
Improve clarity.
If the answer is already correct, return it as-is.
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


# ================= TOOL ROUTING =================

def route_tools(plan: str):
    results = {}

    if not plan.startswith("TOOLS:"):
        return results

    lines = plan.splitlines()[1:]

    for line in lines:
        if ":" not in line:
            continue

        tool, arg = line.split(":", 1)
        tool = tool.strip("- ").strip()
        arg = arg.strip()

        if tool == "calculator":
            results["calculator"] = calculator(arg)

        elif tool == "recall_memory":
            results["recall_memory"] = recall_memory(get_memory(), arg)

    return results


# ================= AGENT =================

def agent(user_input: str) -> str:
    if len(user_input.strip()) < 2:
        return "Can you please clarify your question?"

    # 1️⃣ store user input
    add_to_memory("user", user_input)

    # 2️⃣ plan
    plan = planner(user_input)

    # 3️⃣ tool execution
    tool_results = route_tools(plan)

    # 4️⃣ verify tool results
    if tool_results:
        for result in tool_results.values():
            if result in ("ERROR", "NOT_FOUND"):
                break
        else:
            # all tools succeeded
            if len(tool_results) == 1:
                final = list(tool_results.values())[0]
            else:
                final = ", ".join(
                    f"{k}: {v}" for k, v in tool_results.items()
                )

            add_to_memory("assistant", final)
            return final

    # 5️⃣ fallback to executor
    execution = executor(user_input)

    # 6️⃣ critic refinement
    final_answer = critic(user_input, execution).strip()

    add_to_memory("assistant", final_answer)
    return final_answer


# ================= MAIN LOOP =================

if __name__ == "__main__":
    print("AstraAgent v0.5 (Multi-Tool Agent)")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response = agent(user_input)
        print("Agent:", response)
