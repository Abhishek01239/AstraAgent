import json
from tools import AVAILABLE_TOOLS


def execute_tool(tool_call: str):
    """
    Execute tool from JSON instruction.

    Expected format:
    {
      "tool": "write_file",
      "args": {"filename": "...", "content": "..."}
    }
    """

    try:
        data = json.loads(tool_call)

        tool_name = data.get("tool")
        args = data.get("args", {})

        if tool_name not in AVAILABLE_TOOLS:
            return "Unknown tool"

        result = AVAILABLE_TOOLS[tool_name](**args)
        return result

    except Exception as e:
        return f"Tool execution failed: {e}"
