import random

def choose_next_agent(agents, turn):
    """
    Decide which agent speaks next.

    Strategy:
    - simple round robin rotation
    - fallback to random if needed
    """

    if not agents:
        return None

    # round robin
    index = turn % len(agents)
    return agents[index]
