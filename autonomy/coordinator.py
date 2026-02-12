import random


class Coordinator:
    def __init__(self, agents, max_turns=8):
        self.agents = agents
        self.max_turns = max_turns

    def choose_agent(self):
        return random.choice(self.agents)

    def should_stop(self, turn_count):
        return turn_count >= self.max_turns
