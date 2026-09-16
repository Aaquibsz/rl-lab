"""RL LAB — desktop app (runs locally, no browser / server needed).

Run it:
    python desktop\\app.py
or double-click  Run RL Lab.bat

Same GridWorld + Monte Carlo engine as the website (backend/ folder),
with a native desktop window instead of React + FastAPI.
Requires only the Python standard library (tkinter).
"""
import os
import sys
import threading

try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:  # pragma: no cover
    sys.exit("tkinter is required (it ships with standard Python on Windows/macOS).")

# Reuse the website's engine: backend/environment.py, agent.py, episode.py, ...
_BACKEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
if os.path.isdir(_BACKEND_DIR) and _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

from environment import GridWorld
from episode import generate_episode
from returns import calculate_returns
from value_function import ValueFunction

GRID_SIZE = 5
TRAIN_EPISODES = 1000

# ---------- Night-mode theme ----------
THEME = {
    "bg": "#0f172a",        # window / frames
    "fg": "#e2e8f0",        # primary text
    "muted": "#94a3b8",     # secondary text
    "button_bg": "#1e293b",  # standard buttons
    "button_fg": "#e2e8f0",
    "button_active": "#334155",
    "accent_bg": "#2563eb",  # Train button
    "accent_fg": "white",
}

COLORS = {
    "agent": ("#3b82f6", "white"),
    "goal": ("#16a34a", "white"),
    "obstacle": ("#475569", "white"),
    "default": ("#1e293b", "#e2e8f0"),
}


class RLLabDesktop:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("RL LAB — GridWorld Desktop")
        root.resizable(False, False)
        root.configure(bg=THEME["bg"])

        self.env = GridWorld()
        self.vf = ValueFunction()
        self.total_episodes = 0

        self.position = self.env.agent_position
        self.reward = 0
        self.episode_no = 1
        self.last_action = "—"
        self.done = False
        self.training = False

        self._build_ui()
        self.refresh_grid()
        self._bind_keys()

    # ---------- UI ----------
    def _build_ui(self):
        bg, fg, muted = THEME["bg"], THEME["fg"], THEME["muted"]
        header = tk.Frame(self.root, padx=12, pady=8, bg=bg)
        header.pack(fill="x")
        tk.Label(header, text="RL LAB", font=("Segoe UI", 16, "bold"),
                 bg=bg, fg=fg).pack(side="left")
        tk.Label(header, text="GridWorld · Monte Carlo (Lecture 1)",
                 font=("Segoe UI", 9), bg=bg, fg=muted).pack(side="left", padx=(10, 0))

        body = tk.Frame(self.root, padx=12, pady=4, bg=bg)
        body.pack()

        # Grid (left)
        grid_box = tk.Frame(body, bg=bg)
        grid_box.pack(side="left", padx=(0, 16))
        self.cells = {}
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                lbl = tk.Label(grid_box, text="", font=("Segoe UI", 10, "bold"),
                               width=7, height=3, relief="solid", borderwidth=1,
                               bg=COLORS["default"][0], fg=COLORS["default"][1])
                lbl.grid(row=r, column=c, padx=1, pady=1)
                self.cells[(r, c)] = lbl

        self.hint = tk.Label(grid_box, text="Navigate the agent to the goal (G).",
                             font=("Segoe UI", 9), bg=bg, fg=muted)
        self.hint.grid(row=GRID_SIZE, column=0, columnspan=GRID_SIZE, pady=(6, 0))

        # Panel (right)
        panel = tk.Frame(body, bg=bg)
        panel.pack(side="left", anchor="n")

        self.state_var = tk.StringVar()
        self.action_var = tk.StringVar()
        self.reward_var = tk.StringVar()
        self.episode_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Not trained yet.")
        for label, var in (("Current State", self.state_var),
                           ("Last Action", self.action_var),
                           ("Reward", self.reward_var),
                           ("Episode", self.episode_var)):
            tk.Label(panel, text=label, font=("Segoe UI", 9), bg=bg, fg=muted).pack(anchor="w")
            tk.Label(panel, textvariable=var, font=("Segoe UI", 12, "bold"),
                     bg=bg, fg=fg).pack(anchor="w", pady=(0, 8))

        tk.Button(panel, text="Reset (R)", command=self.reset, width=18,
                  bg=THEME["button_bg"], fg=THEME["button_fg"],
                  activebackground=THEME["button_active"],
                  activeforeground=THEME["button_fg"]).pack(pady=(0, 6))

        moves = tk.Frame(panel, bg=bg)
        moves.pack(pady=4)
        move_btns = [
            ("↑", "UP", 0, 1), ("←", "LEFT", 1, 0),
            ("↓", "DOWN", 1, 1), ("→", "RIGHT", 1, 2),
        ]
        for text, action, row, col in move_btns:
            tk.Button(moves, text=text, width=5,
                      bg=THEME["button_bg"], fg=THEME["button_fg"],
                      activebackground=THEME["button_active"],
                      activeforeground=THEME["button_fg"],
                      command=lambda a=action: self.move(a)).grid(row=row, column=col)
        tk.Label(panel, text="Keys: arrows / WASD", font=("Segoe UI", 8),
                 bg=bg, fg=muted).pack()

        self.train_btn = tk.Button(panel, text="Train Agent", width=18,
                                   font=("Segoe UI", 10, "bold"), command=self.train,
                                   bg=THEME["accent_bg"], fg=THEME["accent_fg"],
                                   activebackground="#1d4ed8",
                                   activeforeground=THEME["accent_fg"])
        self.train_btn.pack(pady=(12, 2))
        tk.Label(panel, textvariable=self.status_var, font=("Segoe UI", 9),
                 bg=bg, fg=muted, wraplength=180, justify="left").pack()

        tk.Label(panel, text="A=agent  G=goal(+10)\n×=obstacle(−5)  ·=empty(−1)\nNumbers = estimated V(s)",
                 font=("Segoe UI", 8), bg=bg, fg=muted, justify="left").pack(pady=(8, 0))

    def _bind_keys(self):
        self.root.bind("<Up>", lambda _e: self.move("UP"))
        self.root.bind("<Down>", lambda _e: self.move("DOWN"))
        self.root.bind("<Left>", lambda _e: self.move("LEFT"))
        self.root.bind("<Right>", lambda _e: self.move("RIGHT"))
        for key, action in (("w", "UP"), ("s", "DOWN"), ("a", "LEFT"), ("d", "RIGHT"),
                            ("W", "UP"), ("S", "DOWN"), ("A", "LEFT"), ("D", "RIGHT")):
            self.root.bind(key, lambda _e, a=action: self.move(a))
        self.root.bind("r", lambda _e: self.reset())
        self.root.bind("R", lambda _e: self.reset())

    # ---------- Logic ----------
    def refresh_grid(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                pos = (r, c)
                lbl = self.cells[pos]
                value = self.vf.values.get(pos)
                if tuple(self.position) == pos:
                    bg, fg = COLORS["agent"]
                    text = "A"
                elif pos == self.env.goal:
                    bg, fg = COLORS["goal"]
                    text = "G"
                elif pos in self.env.obstacles:
                    bg, fg = COLORS["obstacle"]
                    text = "×"
                else:
                    bg, fg = COLORS["default"]
                    text = f"{value:.2f}" if value is not None else ""
                lbl.config(text=text, bg=bg, fg=fg)
        if self.done:
            self.hint.config(text="Goal reached! Press Reset (R) for a new episode.")
        elif self.total_episodes:
            self.hint.config(text=f"V(s) estimated from {self.total_episodes} episodes.")
        self.state_var.set(f"({self.position[0]}, {self.position[1]})")
        self.action_var.set(self.last_action)
        self.reward_var.set(str(self.reward))
        self.episode_var.set(str(self.episode_no))

    def move(self, action: str):
        if self.done or self.training:
            return
        state, reward, done = self.env.step(action)
        self.position = state
        self.reward = reward
        self.done = done
        self.last_action = action
        self.refresh_grid()

    def reset(self):
        if self.training:
            return
        self.position = self.env.reset()
        self.reward = 0
        self.done = False
        self.last_action = "—"
        self.episode_no += 1
        self.refresh_grid()

    def train(self):
        if self.training:
            return
        self.training = True
        self.train_btn.config(state="disabled", text="Training...")
        self.status_var.set(f"Training {TRAIN_EPISODES} episodes...")
        threading.Thread(target=self._train_worker, daemon=True).start()

    def _train_worker(self):
        try:
            for _ in range(TRAIN_EPISODES):
                episode = generate_episode()
                episode_returns = calculate_returns(episode)
                self.vf.update(episode_returns)
            self.total_episodes += TRAIN_EPISODES
            self.root.after(0, self._train_done, None)
        except Exception as exc:  # pragma: no cover
            self.root.after(0, self._train_done, exc)

    def _train_done(self, error):
        self.training = False
        self.train_btn.config(state="normal", text="Train Agent")
        if error is not None:
            messagebox.showerror("Training failed", str(error))
            self.status_var.set("Training failed.")
        else:
            self.status_var.set(
                f"Added {TRAIN_EPISODES} episodes ({self.total_episodes} total).")
        self.refresh_grid()


def main():
    root = tk.Tk()
    RLLabDesktop(root)
    root.mainloop()


if __name__ == "__main__":
    main()
