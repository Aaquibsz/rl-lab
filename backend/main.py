from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from environment import GridWorld
from episode import generate_episode
from returns import calculate_returns
from value_function import ValueFunction


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


env = GridWorld()
value_function = ValueFunction()
total_episodes_trained = 0  # tracks cumulative training across /train calls


@app.get("/")
def home():
    return {
        "message": "RL Lab backend is running"
    }


@app.post("/reset")
def reset():
    state = env.reset()

    return {
        "state": state,
        "reward": 0,
        "done": False,
    }


@app.post("/step/{action}")
def step(action: str):
    action = action.upper()

    if action not in ["UP", "DOWN", "LEFT", "RIGHT"]:
        return {
            "error": "Invalid action"
        }

    state, reward, done = env.step(action)

    return {
        "state": state,
        "reward": reward,
        "done": done,
    }


@app.post("/train")
def train():
    global total_episodes_trained

    episodes = 1000

    for _ in range(episodes):
        episode = generate_episode()
        episode_returns = calculate_returns(episode)
        value_function.update(episode_returns)

    total_episodes_trained += episodes

    return {
        "message": "Training completed",
        "episodes": episodes,
        "total_episodes": total_episodes_trained,
        "values": {
            f"{state[0]},{state[1]}": round(value, 2)
            for state, value in value_function.values.items()
        }
    }