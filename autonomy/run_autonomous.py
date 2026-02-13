from agent_base import Agent
from chat_room import ChatRoom
from coordinator import choose_next_agent

MAX_TURNS = 10

# ===== AGENT PERSONALITIES =====

THINKER_PROMPT = """
You are a creative thinker.
Propose ideas and move the discussion forward.
Be concise.
"""

RESEARCHER_PROMPT = """
You are a researcher.
Ask questions, explore reasons, provide context.
Be analytical.
"""

CRITIC_PROMPT = """
You are a critic.
Challenge weak logic and point out problems.
Be constructive and brief.
"""

if __name__ == "__main__":
    print("\n=== Autonomous AI Discussion ===\n")

    topic = input("Enter discussion topic: ")

    room = ChatRoom()

    # create agents with personalities
    thinker = Agent("Thinker", THINKER_PROMPT)
    researcher = Agent("Researcher", RESEARCHER_PROMPT)
    critic = Agent("Critic", CRITIC_PROMPT)

    agents = [thinker, researcher, critic]

    room.add("SYSTEM", f"Topic: {topic}")

    for turn in range(MAX_TURNS):
        agent = choose_next_agent(agents, turn)

        message = agent.speak(
            topic=topic,
            history=room.history_text()
        )

        room.add(agent.name, message)
        print(f"{agent.name}: {message}")

    print("\nDiscussion saved. Agents will remember next time.")
