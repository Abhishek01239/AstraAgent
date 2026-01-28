import json
from tools import add_task, calculator

def load_memory():
    with open("memory.json", "r") as f:
        return json.load(f)
    
def save_memory(data):
    with open("memory.json", "w") as f:
        json.dump(data, f, indent = 2)

def agent(user_input):
    memory = load_memory()

    if "add_task" in user_input.lower():
        task = user_input.replace("add task", "").strip()
        memory['tasks'].append(task)
        save_memory(memory)
        return add_task(task)
    
    elif "calculate" in user_input.lower():
        expr = user_input.replace("calculate", "").strip()
        return calculator(expr)
    
    else:
        return "I don't know how to do that yet."
    
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    print("Agent: ", agent(user_input))

    
