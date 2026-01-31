def calculator(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": {}})
        return f"Result: {result}"
    except Exception as e:
        return f"Invalid Expression {str(e)}"

TOOLS = {
    'calculator': calculator
}
    
