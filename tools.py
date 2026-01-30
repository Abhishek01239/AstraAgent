def add_task(task):
    return f"Task Added: {task}"

def calculator(expression):
    try:
        return str(eval(expression))
    except:
        return "Invalid Expression"
    
