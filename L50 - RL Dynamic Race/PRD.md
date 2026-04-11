# PRD — L50 Dynamic Drone Race: Bellman vs Q-Learning

## Problem Statement

In L49 the drone world was **frozen**: buildings and wind zones never moved.
Real environments don't work that way. A storm can block a path. A bridge can
suddenly appear. A pit can open without warning.

This lesson answers the question: **which algorithm survives best in a world
that keeps changing?**

We pit two drone agents against each other on the same 12×12 grid:

| Drone | Algorithm | Type |
|-------|-----------|------|
| Blue | Q-Learning | Model-free — learns from experience |
| Orange | Bellman (Value Iteration) | Model-based — reads the grid and solves it |

Dynamic events spawn and expire throughout training. We measure who earns the
most cumulative score across 800 episodes.

---

## Goals

1. Implement a **dynamic environment** that randomly adds/removes obstacles and bonuses.
2. Implement a **Bellman (Value Iteration) agent** that re-solves when the world changes.
3. Implement a **Q-Learning agent** (same as L49) that adapts from experience.
4. Show a **real-time competition dashboard** with both grids, reward curves, and a score bar.
5. Save the final result as `outputs/race_final.png`.

---

## Dynamic Events

Every 30 episodes, one new random event spawns on a free cell.
Events disappear after 90 episodes (the world keeps changing).
Maximum 6 active events at once.

| Event | Cell Color | Effect | Reward |
|-------|-----------|--------|--------|
| Pit | Dark red | Drone enters → episode ends immediately | -30 |
| Barrier | Grey | Temporary wall, drone cannot enter | -20 |
| Bridge | Bright green | Bonus crossing | +15 |
| Extra Wind | Light blue | Extra push zone | -5 |

---

## Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-1 | Events spawn every `EVENT_INTERVAL=30` episodes on a random free cell |
| FR-2 | Events expire after `EVENT_LIFETIME=90` episodes |
| FR-3 | Both drones face the **exact same** dynamic events (synchronized) |
| FR-4 | Q-Learning updates its Q-table after every step (model-free) |
| FR-5 | Bellman agent re-runs Value Iteration when the environment fingerprint changes |
| FR-6 | Live dashboard: 2 grids + policy arrows + reward curves + cumulative score bars |
| FR-7 | Console prints every 100 episodes: reward, goal rate, event count, epsilon |
| FR-8 | CLI: `python main.py` (with viz) or `python main.py --no-viz` |
| FR-9 | Final PNG saved to `outputs/race_final.png` |

---

## Non-Functional Requirements

- No RL frameworks (no Gym, no Stable-Baselines, no PyTorch)
- Only `numpy` and `matplotlib`
- Each Python file must stay under 150 lines
- All code and comments in English

---

## Architecture

| File | Role | Lines |
|------|------|-------|
| `config.py` | Single source of truth for all constants | ~60 |
| `environment.py` | `DroneEnv`: grid step logic + dynamic event spawning | ~120 |
| `agent_qlearn.py` | `QLearningAgent`: Q-table + epsilon-greedy + Bellman update | ~45 |
| `agent_bellman.py` | `BellmanAgent`: Value Iteration solver, re-runs on env change | ~105 |
| `train.py` | Dual-agent episode loop, stats collection, viz trigger | ~80 |
| `visualize.py` | 4-panel matplotlib dashboard | ~145 |
| `main.py` | CLI entry point, wires everything | ~80 |

---

## Key Algorithm Difference (why this is interesting)

**Q-Learning** never looks at the grid. It only sees rewards after each step.
When a pit appears, it has to stumble into it at least once before it learns to
avoid it. Slow to adapt, but works even if you never show it the map.

**Bellman (Value Iteration)** reads the grid and solves the optimal policy
mathematically. The moment a new event appears, it re-runs the solver and
immediately knows the best route. But re-solving takes computation time, and it
can only be as good as its model — if the model is wrong, the policy is wrong.

In a **slowly changing** world (EVENT_INTERVAL=30), Bellman has time to re-solve
between changes and usually wins. In a **rapidly changing** world (small interval),
Q-Learning's incremental updates may keep pace better.

---

## Success Criteria

- Both drones reach the goal in the majority of episodes by episode 600.
- Reward curves visibly recover after each dynamic event.
- `race_final.png` clearly shows the winner in the cumulative score bar.
