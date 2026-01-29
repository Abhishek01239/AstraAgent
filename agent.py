import json
import os
from openai import OpenAI
from tools import add_task, calculator

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

def load_memory():
    if not os.path.exists("memory.json"):
        return {"tasks": []}

    with open("memory.json", "r") as f:
        return json.load(f)

def save_memory(data):
    with open("memory.json", "w") as f:
        json.dump(data, f, indent=2)

TOOLS = {
    "add_task": add_task,
    "calculator": calculator
}

def decide_action(user_input):
    prompt = f"""
You are an AI agent.

Your job is to decide which tool to use.

Available tools:
1. add_task(task) → use when user wants to save or remember something
2. calculator(expression) → use when user asks for math

User input:
"{user_input}"

Respond ONLY in valid JSON format:
{{"tool": "tool_name", "value": "argument"}}
"""

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content.strip()
        return json.loads(content)

    except Exception as e:
        # Fallback (safe default)
        return {
            "tool": "add_task",
            "value": user_input
        }

def agent(user_input):
    memory = load_memory()
    decision = decide_action(user_input)

    tool = decision.get("tool")
    value = decision.get("value")

    if tool not in TOOLS:
        return "I don't know how to do that yet."

    if tool == "add_task":
        memory["tasks"].append(value)
        save_memory(memory)

    return TOOLS[tool](value)

if __name__ == "__main__":
    print("🤖 AstraAgent is running (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Agent: Goodbye 👋")
            break

        result = agent(user_input)
        print("Agent:", result)
