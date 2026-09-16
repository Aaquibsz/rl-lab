from episode import generate_episode
from returns import calculate_returns


episode = generate_episode()

returns = calculate_returns(episode)

for state, G in returns:
    print(
        "State:", state,
        "| Return:", round(G, 2)
    )

print("\nEpisode length:", len(episode))