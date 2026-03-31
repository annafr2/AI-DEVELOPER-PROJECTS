# PRD — RL Drone Navigation (L49)

## 1. Problem Statement

A drone must learn to fly from a start position to a goal position in a 12x12 grid world.
The drone has no map and no instructions — it must learn by trial and error using
Reinforcement Learning (specifically Q-learning).

## 2. Goal

Train the drone to find an efficient route from `(0,0)` to `(11,11)` while avoiding
buildings and minimizing exposure to wind zones.

## 3. Success Criteria

| Metric | Target |
|--------|--------|
| Goal rate (last 100 episodes) | >= 85% |
| Best path length | <= 25 steps |
| Training episodes | 1500 |
| Files under 150 lines | All Python files |

## 4. Grid Specification

- Size: 12 x 12 cells
- Start: top-left corner (0, 0)
- Goal: bottom-right corner (11, 11)

### Cell Types

| Type | Color | Description |
|------|-------|-------------|
| Free | White | Drone can fly here freely |
| Building | Dark gray | Cannot enter; costs -20 per attempt |
| Wind zone | Light blue | Drone is pushed randomly; costs -5 |
| Start | Green | Where the drone begins each episode |
| Goal | Gold | Target destination (+100 reward) |
| Path | Purple | Cells visited this episode |
| Drone | Orange | Current drone position |

## 5. Reward Structure

| Event | Reward |
|-------|--------|
| Reach the goal | +100 |
| Normal step (free cell) | -1 |
| Enter wind zone | -5 |
| Attempt to enter building | -20 (drone stays in place) |

The -1 per step discourages wandering — the drone is rewarded for finding
the shortest path, not just for eventually arriving.

## 6. Q-Learning Algorithm

- **State**: integer index = `row * 12 + col` (144 total states)
- **Actions**: UP, DOWN, LEFT, RIGHT (4 actions)
- **Q-table**: 144 x 4 matrix initialized to 0
- **Update rule**: `Q[s,a] += alpha * (r + gamma * max(Q[s']) - Q[s,a])`
- **Exploration**: epsilon-greedy, decaying from 1.0 to 0.01 over 1500 episodes

### Hyperparameters

| Parameter | Value | Meaning |
|-----------|-------|---------|
| Alpha (learning rate) | 0.1 | How fast to update Q-values |
| Gamma (discount) | 0.99 | How much future rewards matter |
| Epsilon start | 1.0 | 100% random at start |
| Epsilon min | 0.01 | Always 1% chance of exploring |
| Epsilon decay | 0.997 | Epsilon multiplied by this each episode |

## 7. Wind Zone Behavior

When the drone enters a wind zone:
1. It lands in the wind zone cell
2. It is pushed to a random adjacent cell (not a building, not out of bounds)
3. -5 reward is applied

This models unpredictable wind: the drone cannot reliably cross wind zones.

## 8. Visualization Dashboard

Four panels updated every 20 episodes:

| Panel | Content |
|-------|---------|
| Environment | Grid with current drone path |
| V-Values + Policy | Heatmap of best expected reward per cell + arrows showing best action |
| Reward History | Raw reward per episode + 20-episode rolling average |
| Stats Panel | Epsilon, episode, goal rate, last reward, hyperparameters |

## 9. Technical Constraints

- Each Python file: max 150 lines
- Libraries: numpy, matplotlib only (no RL frameworks)
- Output: PNG saved to `outputs/drone_rl_final.png`

## 10. Out of Scope

- Deep Q-learning (DQN, neural networks)
- Continuous state/action spaces
- 3D visualization
- Multi-agent scenarios
