class ValueFunction:

    def __init__(self):
        self.values = {}
        self.returns = {}

    def update(self, episode_returns):

        for state, G in episode_returns:

            # Store all returns received from this state
            if state not in self.returns:
                self.returns[state] = []

            self.returns[state].append(G)

            # Monte Carlo estimate:
            # V(s) = average of observed returns
            self.values[state] = (
                sum(self.returns[state])
                / len(self.returns[state])
            )

    def get_value(self, state):
        return self.values.get(state, 0)