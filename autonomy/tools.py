import os


def write_file(filename, content):
    """
    Write content to a file.
    """

    os.makedirs("outputs", exist_ok=True)

    path = os.path.join("outputs", filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"File saved at {path}"


AVAILABLE_TOOLS = {
    "write_file": write_file
}
