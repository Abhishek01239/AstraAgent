from llm import call_llm
from memory import add_to_memory, get_memory
from tools import calculator, recall_memory
from facts import remember_fact
# ================= PROMPTS =================

PLANNER_PROMPT = """
You are the Planner.

Decide which tools are required.

Available tools:
- calculator
- recall_memory

Respond EXACTLY in this format if tools are needed:
TOOLS:
- <tool_name>: <input>

If no tools are needed:
NO_TOOL

Do NOT solve the task.
"""

EXECUTOR_WITH_TOOLS_PROMPT = """
You are the Executor.

User request:
{user_request}

Tool results:
{tool_results}

Answer naturally using the tool results.
Do NOT mention tools or reasoning.
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

# ================= CORE =================

def planner(task: str) -> str:
    messages = [
        {"role": "system", "content": PLANNER_PROMPT},
        *get_memory(),
        {"role": "user", "content": task}
    ]
    return call_llm(messages).strip()


def run_tools(plan: str):
    results = {}

    if not plan.startswith("TOOLS:"):
        return results

    for line in plan.splitlines()[1:]:
        if ":" not in line:
            continue

        tool, arg = line.split(":", 1)
        tool = tool.strip("- ").strip()
        arg = arg.strip()

        if tool == "calculator":
            results["calculator"] = calculator(arg)

        elif tool == "recall_memory":
            results["memory"] = recall_memory(get_memory(), arg)

    return results


def executor_with_tools(task: str, tool_results: dict) -> str:
    messages = [
        {
            "role": "system",
            "content": EXECUTOR_WITH_TOOLS_PROMPT.format(
                user_request=task,
                tool_results=tool_results or "None"
            )
        },
        *get_memory()
    ]
    return call_llm(messages)


def critic(task: str, answer: str) -> str:
    messages = [
        {"role": "system", "content": CRITIC_PROMPT},
        *get_memory(),
        {
            "role": "user",
            "content": f"User request:\n{task}\n\nAnswer:\n{answer}"
        }
    ]
    return call_llm(messages).strip()


# ================= AGENT =================

def agent(user_input: str) -> str:
    add_to_memory("user", user_input)

    plan = planner(user_input)
    tool_results = run_tools(plan)

    execution = executor_with_tools(user_input, tool_results)
    final_answer = critic(user_input, execution)

    if "my name is" in user_input.lower():
        name = user_input.split("is")[-1].strip()
        remember_fact("user_name", name)

    add_to_memory("assistant", final_answer)
    return final_answer


# ================= MAIN =================

if __name__ == "__main__":
    print("AstraAgent v0.6 — Tool-Aware Reasoning")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        print("Agent:", agent(user_input))
