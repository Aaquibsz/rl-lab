def calculate_returns(episode, gamma=0.9):
    returns = []

    G = 0

    for state, action, reward in reversed(episode):
        G = reward + gamma * G

        returns.insert(0, (state, G))

    return returns