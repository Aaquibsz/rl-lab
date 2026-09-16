import { useState } from "react";
import {
  RotateCcw,
  Play,
  Loader2,
  ArrowUp,
  ArrowDown,
  ArrowLeft,
  ArrowRight,
} from "lucide-react";

import "./App.css";

const GRID_SIZE = 5;

const API_URL = import.meta.env.VITE_API_URL;

console.log("API_URL is:", API_URL);

const obstacles = [
  [1, 2],
  [2, 2],
];

function App() {
  const [position, setPosition] = useState([0, 0]);
  const [reward, setReward] = useState(0);
  const [episode, setEpisode] = useState(1);
  const [lastAction, setLastAction] = useState("—");
  const [done, setDone] = useState(false);
  const [values, setValues] = useState({});
  const [training, setTraining] = useState(false);
  const [trainStatus, setTrainStatus] = useState("");

  const move = async (action) => {
    if (done) return;

    try {
      const response = await fetch(
        `${API_URL}/step/${action}`,
        { method: "POST" }
      );

      const data = await response.json();

      if (data.error) {
        console.error(data.error);
        return;
      }

      setPosition([...data.state]);
      setReward(data.reward);
      setDone(data.done);
      setLastAction(action);
    } catch (error) {
      console.error("Backend connection error:", error);
    }
  };

  const train = async () => {
    if (training) return;

    setTraining(true);
    setTrainStatus("Training 1000 episodes...");

    try {
      const response = await fetch(`${API_URL}/train`, {
        method: "POST",
      });

      const data = await response.json();

      setValues(data.values || {});

      setTrainStatus(
        `Added ${data.episodes} episodes (${data.total_episodes} total)`
      );
    } catch (error) {
      console.error("Training error:", error);
      setTrainStatus("Training failed.");
    } finally {
      setTraining(false);
    }
  };

  const reset = async () => {
    try {
      const response = await fetch(`${API_URL}/reset`, {
        method: "POST",
      });

      const data = await response.json();

      setPosition([...data.state]);
      setReward(data.reward);
      setDone(data.done);
      setLastAction("—");
      setEpisode((value) => value + 1);
    } catch (error) {
      console.error("Reset error:", error);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <div className="logo">RL LAB</div>
          <p>Interactive Reinforcement Learning Playground</p>
        </div>
        <div className="lecture-badge">DAVID SILVER · LECTURE 1</div>
      </header>

      <main className="main">
        <section className="grid-section">
          <div className="section-title">
            <div>
              <h1>GridWorld</h1>
              <p>
                {done
                  ? "Goal reached."
                  : "Navigate the agent to the goal."}
              </p>
            </div>

            <button className="reset-button" onClick={reset}>
              <RotateCcw size={17} />
              Reset
            </button>
          </div>

          {/* NEW: explains what the numbers mean */}
          {Object.keys(values).length > 0 && (
            <p className="value-explainer">
              Numbers show <strong>estimated V<sup>π</sup>(s)</strong> — the
              expected total discounted return from that state, learned via
              Monte Carlo policy evaluation.
            </p>
          )}

          <div className="grid">
            {Array.from({ length: GRID_SIZE }).map((_, row) =>
              Array.from({ length: GRID_SIZE }).map((_, col) => {
                const isAgent =
                  position[0] === row && position[1] === col;
                const isGoal = row === 4 && col === 4;
                const isObstacle = obstacles.some(
                  ([r, c]) => r === row && c === col
                );
                const value = values[`${row},${col}`];

                return (
                  <div
                    key={`${row}-${col}`}
                    className={`cell ${
                      isAgent
                        ? "agent"
                        : isGoal
                        ? "goal"
                        : isObstacle
                        ? "obstacle"
                        : ""
                    }`}
                  >
                    {isAgent && "A"}
                    {!isAgent && isGoal && "G"}
                    {!isAgent && isObstacle && "×"}
                    {!isAgent && !isObstacle && value !== undefined && (
                      <span className="cell-value">{value}</span>
                    )}
                  </div>
                );
              })
            )}
          </div>

          {/* NEW: legend */}
          <div className="legend">
            <span><span className="legend-swatch agent" /> Agent (A)</span>
            <span><span className="legend-swatch goal" /> Goal (G)</span>
            <span><span className="legend-swatch obstacle" /> Obstacle (×)</span>
            <span><span className="legend-swatch value" /> Estimated V<sup>π</sup>(s)</span>
          </div>

          <div className="controls">
            <button onClick={() => move("UP")}>
              <ArrowUp size={20} />
            </button>
            <div>
              <button onClick={() => move("LEFT")}>
                <ArrowLeft size={20} />
              </button>
              <button onClick={() => move("DOWN")}>
                <ArrowDown size={20} />
              </button>
              <button onClick={() => move("RIGHT")}>
                <ArrowRight size={20} />
              </button>
            </div>
          </div>
        </section>

        <aside className="panel">
          <div className="panel-card">
            <span>Current State</span>
            <strong>({position[0]}, {position[1]})</strong>
          </div>

          <div className="panel-card">
            <span>Last Action</span>
            <strong>{lastAction}</strong>
          </div>

          <div className="panel-card">
            <span>Reward</span>
            <strong
              className={
                reward > 0 ? "positive" : reward < 0 ? "negative" : ""
              }
            >
              {reward}
            </strong>
          </div>

          <div className="panel-card">
            <span>Episode</span>
            <strong>{episode}</strong>
          </div>

          <div className="concept-card">
            <span>RL LOOP</span>
            <div className="rl-flow">
              <div>STATE</div>
              <div className="arrow">↓</div>
              <div>ACTION</div>
              <div className="arrow">↓</div>
              <div>ENVIRONMENT</div>
              <div className="arrow">↓</div>
              <div>REWARD + NEXT STATE</div>
            </div>
          </div>

          {trainStatus && <p className="train-status">{trainStatus}</p>}

          <button
            className="train-button"
            onClick={train}
            disabled={training}
          >
            {training ? (
              <Loader2 size={18} className="spin" />
            ) : (
              <Play size={18} />
            )}
            {training ? "Training..." : "Train Agent"}
          </button>
        </aside>
      </main>
    </div>
  );
}

export default App;