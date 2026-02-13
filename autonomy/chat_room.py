from memory_store import load_discussion, save_discussion


class ChatRoom:
    def __init__(self):
        self.chat_log = load_discussion()

    def add(self, agent_name, message):
        entry = {
            "agent": agent_name,
            "message": message
        }

        self.chat_log.append(entry)
        save_discussion(self.chat_log)

    def history_text(self):
        if not self.chat_log:
            return "No previous discussion."

        return "\n".join(
            f"{e['agent']}: {e['message']}"
            for e in self.chat_log[-20:]
        )

    def show(self):
        for e in self.chat_log:
            print(f"{e['agent']}: {e['message']}")
