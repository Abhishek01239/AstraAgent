from agent_base import Agent
from chat_room import ChatRoom
from coordinator import choose_next_agent
from goal_manager import is_goal_complete, get_next_objective

MAX_TURNS = 15

THINKER_PROMPT = "You generate ideas to solve the objective."
RESEARCHER_PROMPT = "You analyze and provide useful information."
CRITIC_PROMPT = "You find weaknesses and improve solutions."

if __name__ == "__main__":
    print("\n=== Goal-Driven Autonomous AI ===\n")

    goal = input("Enter goal for agents: ")

    room = ChatRoom()

    thinker = Agent("Thinker", THINKER_PROMPT)
    researcher = Agent("Researcher", RESEARCHER_PROMPT)
    critic = Agent("Critic", CRITIC_PROMPT)

    agents = [thinker, researcher, critic]

    room.add("SYSTEM", f"Goal: {goal}")

    for turn in range(MAX_TURNS):

        history = room.history_text()

        # check goal completion
        if is_goal_complete(goal, history):
            print("\n✅ Goal achieved. Stopping discussion.")
            break

        # decide next objective
        objective = get_next_objective(goal, history)
        room.add("SYSTEM", f"Current Objective: {objective}")

        agent = choose_next_agent(agents, turn)

        message = agent.speak(
            topic=objective,
            history=history
        )

        room.add(agent.name, message)
        print(f"{agent.name}: {message}")

    print("\nSession complete.")
