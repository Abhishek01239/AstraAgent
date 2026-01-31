import json
from llm import call_llm
from memory import load_memory, save_memory
from tools import TOOLS

SYSTEM_PROMPT = """
You are AstraAgent, an AI assistant.

Decide whether a tool is required.
If a calculation is needed, use the calculator tool.

Respond ONLY in valid JSON.

FORMAT:
{
  "action": "tool" | "answer",
  "tool_name": "<tool name if any>",
  "input": "<tool input if any>",
  "output": "<final answer if no tool>"
}
"""

def agent(user_input):
    # 🛡️ Input validation
    if len(user_input.strip()) < 2:
        return "Can you please clarify?"

    memory = load_memory()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *memory,
        {"role": "user", "content": user_input}
    ]

    try:
        decision_raw = call_llm(messages)
    except Exception:
        return "LLM error. Please try again."

    # 🛡️ JSON safety
    try:
        decision = json.loads(decision_raw)
    except Exception:
        return "I didn't understand that. Can you rephrase?"

    if "action" not in decision:
        return "I’m not sure how to respond to that."

    # 🛠️ Tool path
    if decision["action"] == "tool":
        tool_name = decision.get("tool_name")
        tool_input = decision.get("input")

        if tool_name not in TOOLS:
            return f"Unknown tool: {tool_name}"

        result = TOOLS[tool_name](tool_input)

        memory.append({"role": "user", "content": user_input})
        memory.append({"role": "assistant", "content": result})
        save_memory(memory)

        return result

    # 💬 Direct answer
    output = decision.get("output", "Okay.")
    memory.append({"role": "user", "content": user_input})
    memory.append({"role": "assistant", "content": output})
    save_memory(memory)

    return output


if __name__ == "__main__":
    print("AstraAgent v0.2 (tools enabled)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        print("Agent:", agent(user_input))
