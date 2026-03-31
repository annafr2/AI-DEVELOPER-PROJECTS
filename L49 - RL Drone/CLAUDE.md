# CLAUDE.md — Developer Guide for L49 RL Drone

## Project Purpose

Q-learning drone navigation in a 12x12 grid with buildings and wind zones.
Used as an educational RL project in the AI Developer Expert course.

## Architecture

| File | Role |
|------|------|
| `config.py` | Single source of truth for all constants |
| `environment.py` | Grid world: step(), reset(), reward logic |
| `agent.py` | Q-table, epsilon-greedy action, Bellman update |
| `train.py` | Episode loop, calls agent + env, feeds visualizer |
| `visualize.py` | 4-panel matplotlib dashboard, owns the figure |
| `main.py` | Wires everything, handles CLI args |

## Key Invariants

- State encoding: `state = row * GRID_SIZE + col`  (0 to 143)
- Action mapping: 0=UP, 1=DOWN, 2=LEFT, 3=RIGHT
- Building cells: drone stays in place, -20 reward (no entry)
- Wind cells: drone enters, then pushed to random valid neighbor, -5 reward
- Q-table shape: `(144, 4)`, initialized to zeros
- Each Python file must stay under 150 lines

## How to Modify

### Add a new trap type (e.g., storm)
1. Add `STORMS = [(r, c), ...]` to `config.py` with its reward
2. Add `CELL_STORM = 7` constant to `environment.py`
3. Handle in `DroneEnv.step()` after the wind check
4. Add color to `CELL_COLORS` in `visualize.py`

### Change grid size
1. Update `GRID_SIZE`, `START`, `GOAL` in `config.py`
2. Update `BUILDINGS` and `WIND_ZONES` coordinates accordingly
3. Everything else is dynamic

### Swap to SARSA (on-policy)
In `train.py`, change `run_episode` to:
- Choose next action before calling `agent.update()`
- Pass next_action to update: `Q[s,a] += alpha * (r + gamma * Q[s', a'] - Q[s,a])`

## Constraints

- No RL frameworks (no Gym, no stable-baselines)
- Only numpy and matplotlib
- All code in English
- Outputs saved to `outputs/` folder
