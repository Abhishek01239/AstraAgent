from agent_base import Agent
from chat_room import ChatRoom
from coordinator import Coordinator


# ================= AGENT PERSONALITIES =================

THINKER_PROMPT = """
You are a Thinker AI.

- Propose ideas
- Move discussion forward
- Suggest conclusions
- Be concise
"""

RESEARCHER_PROMPT = """
You are a Researcher AI.

- Ask why and how
- Provide context
- Explore alternatives
- Challenge assumptions
"""

CRITIC_PROMPT = """
You are a Critic AI.

- Find logical gaps
- Point out risks
- Challenge weak reasoning
- Keep discussion realistic
"""


# ================= SETUP =================

def main():
    topic = input("Enter discussion topic: ")

    thinker = Agent("Thinker", THINKER_PROMPT)
    researcher = Agent("Researcher", RESEARCHER_PROMPT)
    critic = Agent("Critic", CRITIC_PROMPT)

    agents = [thinker, researcher, critic]

    room = ChatRoom()
    coordinator = Coordinator(agents, max_turns=9)

    print("\n=== Autonomous Discussion Started ===\n")

    turn = 0

    while not coordinator.should_stop(turn):
        agent = coordinator.choose_agent()

        message = agent.speak(
            room.get_history(),
            topic
        )

        room.add(agent.name, message)
        print(f"{agent.name}: {message}\n")

        turn += 1

    print("=== Discussion Finished ===")


if __name__ == "__main__":
    main()
