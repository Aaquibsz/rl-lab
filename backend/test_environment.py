from environment import GridWorld


env = GridWorld()

state = env.reset()

print("Starting state:", state)

actions = [
    "RIGHT",
    "RIGHT",
    "RIGHT",
    "RIGHT",
    "DOWN",
    "DOWN",
    "DOWN",
    "DOWN",
]

for action in actions:

    next_state, reward, done = env.step(action)

    print(
        "Action:", action,
        "| State:", next_state,
        "| Reward:", reward,
        "| Done:", done
    )

    if done:
        break