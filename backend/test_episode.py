from episode import generate_episode


episode = generate_episode()

for state, action, reward in episode:

    print(
        "State:", state,
        "| Action:", action,
        "| Reward:", reward
    )

print("\nEpisode length:", len(episode))