class GridWorld:

    def __init__(self):
        self.size = 5
        self.start = (0, 0)
        self.goal = (4, 4)

        self.obstacles = {
            (1, 2),
            (2, 2),
        }

        self.agent_position = self.start

    def reset(self):
        self.agent_position = self.start
        return self.agent_position

    def simulate_step(self, state, action):
        row, col = state

        if action == "UP":
            row -= 1

        elif action == "DOWN":
            row += 1

        elif action == "LEFT":
            col -= 1

        elif action == "RIGHT":
            col += 1

        # Outside grid
        if (
            row < 0
            or row >= self.size
            or col < 0
            or col >= self.size
        ):
            return state, -1, False

        # Obstacle
        if (row, col) in self.obstacles:
            return state, -5, False

        next_state = (row, col)

        # Goal
        if next_state == self.goal:
            return next_state, 10, True

        return next_state, -1, False

    def step(self, action):

        state, reward, done = self.simulate_step(
            self.agent_position,
            action
        )

        self.agent_position = state

        return state, reward, done