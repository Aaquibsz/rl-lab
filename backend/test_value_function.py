from episode import generate_episode
from returns import calculate_returns
from value_function import ValueFunction


value_function = ValueFunction()


# Generate many episodes
for _ in range(1000):

    episode = generate_episode()

    episode_returns = calculate_returns(episode)

    value_function.update(episode_returns)


print("\nSTATE VALUES\n")

for row in range(5):

    for col in range(5):

        state = (row, col)

        value = value_function.get_value(state)

        print(
            f"{state}: {value:.2f}",
            end="   "
        )

    print()