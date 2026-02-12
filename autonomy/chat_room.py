class ChatRoom:
    def __init__(self):
        self.messages = []

    def add(self, sender, text):
        self.messages.append({
            "sender": sender,
            "text": text
        })

    def get_history(self):
        return self.messages

    def show(self):
        for msg in self.messages:
            print(f"{msg['sender']}: {msg['text']}")
