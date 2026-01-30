from llm import call_llm
from memory import load_memory, save_memory

def agent(user_input):
    memory = load_memory()

    messages = [
        {"role": "system", "content": "You are AstraAgent, a helpful AI assistant."},
        *memory,
        {"role": "user", "content": user_input}
    ]

    reply = call_llm(messages)

    memory.append({"role": "user", "content": user_input})
    memory.append({"role": "assistant", "content": reply})

    save_memory(memory)
    return reply


if __name__ == "__main__":
    print("AstraAgent v0.1 (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        print("Agent:", agent(user_input))
