from environment import GridWorld
from agent import RandomAgent


def generate_episode():

    env = GridWorld()
    agent = RandomAgent()

    state = env.reset()

    episode = []

    for _ in range(100):

        action = agent.choose_action(state)

        next_state, reward, done = env.step(action)

        episode.append(
            (state, action, reward)
        )

        state = next_state

        if done:
            break

    return episode