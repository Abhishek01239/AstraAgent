def calculator(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception:
        return "ERROR"

def recall_memory(memory, keyword: str) -> str:
    for item in reversed(memory):
        if keyword.lower() in item['content'].lower():
            return item['content']
    return "NOT_FOUND"

TOOLS = {
    'calculator': calculator
}
    
