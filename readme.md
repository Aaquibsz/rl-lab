# RL LAB

An interactive Reinforcement Learning playground built from scratch, based on concepts from David Silver's *Reinforcement Learning Lecture 1*.

![Demo](demo.gif)

## What this is

RL LAB is a 5×5 GridWorld where an agent moves around, hits rewards and obstacles, and — after training — a Monte Carlo policy evaluation algorithm learns to estimate how good every state is under a random policy.

This project is built **without** RL frameworks like Stable-Baselines3, Gymnasium, or PyTorch. Every piece — the environment, the agent, episode generation, discounted returns, and the value function — is implemented from first principles, on purpose, to actually understand what's happening under the hood rather than call a library function.

## Concepts implemented

| Concept | Where |
|---|---|
| Environment (states, actions, rewards) | `backend/environment.py` |
| Agent / Policy (currently a random policy) | `backend/agent.py` |
| Episode generation | `backend/episode.py` |
| Discounted returns: `G_t = R_(t+1) + γ·G_(t+1)` | `backend/returns.py` |
| Monte Carlo policy evaluation: `Vπ(s) = Eπ[G_t \| S_t = s]` | `backend/value_function.py` |

Clicking **Train Agent** runs 1,000 episodes of the random policy, calculates the return for every visited state, and averages those returns into an estimated value `Vπ(s)` — shown live on the grid. Repeated training accumulates more episodes into the same running average.

## Tech stack

**Desktop app (recommended):** Python + tkinter (standard library only, dark/night-mode UI)
**RL engine (shared):** plain Python — `backend/environment.py`, `agent.py`, `episode.py`, `returns.py`, `value_function.py`
**Website (optional):** FastAPI + Uvicorn backend, React + Vite + lucide-react frontend

## Running it locally

### Desktop app (recommended — no browser, no server, no install)

The desktop app reuses the same GridWorld + Monte Carlo engine as the website, in a native dark-mode window.

Requirements: standard Python 3 with tkinter (ships with Python on Windows/macOS — verified with Python 3.14 + tkinter 9.0). No `pip install` needed.

**Option 1 — double-click (Windows)**
```
Double-click  Run RL Lab.bat
```

**Option 2 — terminal**
```bash
python desktop/app.py
```

### Using the desktop app

| Action | How |
|---|---|
| Move agent | Click arrow buttons, or press arrow keys / WASD |
| Reset episode | Click **Reset (R)** or press `R` |
| Train | Click **Train Agent** — runs 1,000 random-policy episodes in the background, then shows estimated `V(s)` numbers on the grid. Repeat to accumulate more episodes into the running average |

Grid legend: `A` = agent, `G` = goal (+10), `×` = obstacle (−5), empty step = −1. Numbers on cells are the learned `V(s)` values. Training never freezes the window (runs on a background thread).

### Website (optional)

The original web version still works if you prefer the browser.

**Backend**
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
uvicorn main:app --reload
```
Backend runs at `http://127.0.0.1:8000` (docs at `/docs`).

**Frontend**
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
Frontend runs at `http://localhost:5173`.

## Project structure

```text
RL LAB/
├── desktop/app.py        # desktop UI (tkinter, dark mode) — imports the engine from backend/
├── Run RL Lab.bat        # Windows double-click launcher for the desktop app
├── backend/              # RL engine + optional FastAPI server
│   ├── environment.py    # GridWorld (states, actions, rewards)
│   ├── agent.py          # random policy
│   ├── episode.py        # episode generation
│   ├── returns.py        # discounted returns
│   ├── value_function.py # Monte Carlo value estimates
│   └── main.py           # FastAPI server (website only)
└── frontend/             # React website (optional)
```

## What's next

- Policy visualization (showing which action the policy favors per state)
- Policy improvement / Generalized Policy Iteration
- A learned agent that moves based on estimated values instead of randomly

## Why I built this

The reason why i built this was that I wanted to implement what i had learn about the basics of Reinforcement Learning and to make sure that i actually understood the Monte Carlo method.